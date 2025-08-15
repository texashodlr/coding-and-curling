#pragma once

#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cublas_v2.h>
#include <cuda_runtime.h>

#define CEIL_DIV(M, N) (((M) + (N)-1) / (N))
template <const int BM, const int BN, const int BK, const int TM>
__global__ void sgemm1DBlocktiling(int M, int N, int K, float alpha,
                                   const float *A, const float *B, float beta,
                                   float *C) {
  // If we flip x and y here we get ~30% less performance for large matrices.
  // The current, 30% faster configuration ensures that blocks with sequential
  // blockIDs access columns of B sequentially, while sharing the same row of A.
  // The slower configuration would share columns of A, but access into B would
  // be non-sequential. So the faster configuration has better spatial locality
  // and hence a greater L2 hit rate.
  const uint cRow = blockIdx.y;
  const uint cCol = blockIdx.x;

  // each warp will calculate 32*TM elements, with 32 being the columnar dim.
  const int threadCol = threadIdx.x % BN;
  const int threadRow = threadIdx.x / BN;

  // allocate space for the current blocktile in SMEM
  __shared__ float As[BM * BK];
  __shared__ float Bs[BK * BN];

  // Move blocktile to beginning of A's row and B's column
  A += cRow * BM * K;
  B += cCol * BN;
  C += cRow * BM * N + cCol * BN;

  // todo: adjust this to each thread to load multiple entries and
  // better exploit the cache sizes
  assert(BM * BK == blockDim.x);
  assert(BN * BK == blockDim.x);
  const uint innerColA = threadIdx.x % BK; // warp-level GMEM coalescing
  const uint innerRowA = threadIdx.x / BK;
  const uint innerColB = threadIdx.x % BN; // warp-level GMEM coalescing
  const uint innerRowB = threadIdx.x / BN;

  // allocate thread-local cache for results in registerfile
  float threadResults[TM] = {0.0};

  // outer loop over block tiles
  for (uint bkIdx = 0; bkIdx < K; bkIdx += BK) {
    // populate the SMEM caches
    As[innerRowA * BK + innerColA] = A[innerRowA * K + innerColA];
    Bs[innerRowB * BN + innerColB] = B[innerRowB * N + innerColB];
    __syncthreads();

    // advance blocktile
    A += BK;
    B += BK * N;

    // calculate per-thread results
    for (uint dotIdx = 0; dotIdx < BK; ++dotIdx) {
      // we make the dotproduct loop the outside loop, which facilitates
      // reuse of the Bs entry, which we can cache in a tmp var.
      float tmpB = Bs[dotIdx * BN + threadCol];
      for (uint resIdx = 0; resIdx < TM; ++resIdx) {
        threadResults[resIdx] +=
            As[(threadRow * TM + resIdx) * BK + dotIdx] * tmpB;
      }
    }
    __syncthreads();
  }

  // write out the results
  for (uint resIdx = 0; resIdx < TM; ++resIdx) {
    C[(threadRow * TM + resIdx) * N + threadCol] =
        alpha * threadResults[resIdx] +
        beta * C[(threadRow * TM + resIdx) * N + threadCol];
  }
}

/*
This kernel differs from #3 in that it adds a new inner loop for calculating multiple C
    entries per thread.
Now using a SMEM cache size of BM*BK + BN*BK = 64*8 + 64*8 = 1024 floats for
    a total of 4KB per block.

So in our paradigm of matrices: 
    1. A = MxK
    2. B = KxN
    3. C = MxN
    SMEM Cache is loaded with BMxBK and BNxBK which calculates: BMxBN

    Each thread calculates a column of results v. a single result as in Ker 3.
    Previously memory accesses looked like:
        GMEM: k/32 iterations of the outer loop * 2 loads
        SHMEM: k/32 iterations of outer loop * BLOCKSIZE (=32) * 2 loads
        Memory accesses per result: K/16 GMEM, K*2 SMEM
            --> 4096/16, 4096*2: 256+8192
    
    New Kernel: 
        GMEM: k/8 iterations of outerloop * 2 Loads
        SHMEM: K/8 iterations of the outer loop * BK(=8)*(1+TM(=8))
        Memory accesses per result: K/32 GMEM, K*9/8 SMEM
            --> 4096/32, 4096*9/8 = 128 + 4608

    So with the new kernel, 4736 loads v 8448 loads

    In terms of compiler optimizations if don't cache tmp results of B in Btmp
    then we instead end up with this:
    for(uint resIdx = 0; resIdx < TM; ++resIdx){
        for(uint dotIdx = 0; dotIdx < BK; ++dotIdx){
            threadResults[resIdx] +=
                As[(threadRow * TM + resIdx) * BK + dotIdx] * Bs[dotIdx * BN + threadCol];
        }
    }

    The above has /no adverse/ effect on performance because the compiler unrolls
        both loops and then eliminates the repeated SMEM loads of the Bs entries thus
        we end up with the same amount of SMEM accesses as our optimized CUDA code.

        When the PTX is compiled to SASS the SMEM loads from Bs are vectorized!

    The actual optimization here is just doing more math per thread, from 1 result/thr to 4/thr
    1 result needs 7 loads from A and B and 1 load&store to C (15L,1S)

    4 results needs 14 loads from A (2 rows) 14 loads from B (2 rows)
        and 4 loads and 4 stores to C
        so per result (4) we've got 8 loads and 1 store
    For the immediate future we'll optimize arithmetic intensity while still being memory bound.
*/