#pragma once

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cublas_v2.h>
#include <cuda_runtime.h>

#define CEIL_DIV(M, N) (((M) + (N)-1) / (N))

template <const int BLOCKSIZE>
__global__ void sgemm_shared_mem_block(int M, int N, int K, float alpha, const float *A, const float *B, float beta, float *C){
    
    // Output block in resultant matrix C we want to compute in
    // this thread block
    const uint cRow = blockIdx.x;
    const uint cCol = blockIdx.y;

    // Allocate buffer for current block in fast shared mem
    // shared mem is /shared/ between all threads in a block
    __shared__ float As[BLOCKSIZE*BLOCKSIZE];
    __shared__ float Bs[BLOCKSIZE*BLOCKSIZE];

    // the inner row and col that we're accessing in this thread
    const uint threadCol = threadIdx.x % BLOCKSIZE;
    const uint threadRow = threadIdx.x / BLOCKSIZE;

    // Advance pointers to the starting positions

    A += cRow * BLOCKSIZE * K;                  // row=cRow, col=0
    B += cCol * BLOCKSIZE;                      // row=0, col=cCol
    C += cRow * BLOCKSIZE * N +cCol * BLOCKSIZE;// row=cRow, col=cCol

    float tmp = 0.0;
    for (int bkIdx = 0; bkIdx < K; bkIdx += BLOCKSIZE){
        // have each thread load one of the elements in A & B
        // make the threadCol(=threadIdx.x) the consecutive index
        // to allow gmem access coal
        As[threadRow * BLOCKSIZE + threadCol] = A[threadRow*K + threadCol];
        Bs[threadRow * BLOCKSIZE + threadCol] = B[threadRow*N + threadCol];

        // block threads in this block until cache is fully populated 
        __syncthreads();
        A += BLOCKSIZE;
        B += BLOCKSIZE * N;

        // Execute the dotproduct on the currently cached block
        for (int dotIdx = 0; dotIdx < BLOCKSIZE; ++dotIdx){
            tmp += As[threadRow * BLOCKSIZE + dotIdx] * Bs[dotIdx * BLOCKSIZE + threadCol];
        }

        //need to sync again at the end to avoid faster threads/racing
        // fetching the next block into the cache block before slower threads are done
        __syncthreads();

    }
    C[threadRow * N + threadCol] = alpha * tmp + beta * C[threadRow * N + threadCol];
}

/*
SMEM Kernel notes:
    Generally we can assume a SMEM cache per SM which is then sub-partitioned
    among the threadblocks allowing cross thread communications which with my 4070 we've got
    around 48KiB to work with per threadblock -- so within the 32 thread, thread/block/ we can share about 48KiB worth of information
    Bandwidth: GMEM ~ > 500GB/s, SHMEM > 12,080GB/s!

    Thus for this kernel we /win/ by loading a chunk of Matrix A and B from global into shmem then
        performing as much work as possible on the two chunks with each thread being
        assigned one entry of C
        We'll move the chunks along the cols of A and the rows of B performing partial sums on C
            until the result is computed.

        So Matrix &A (32x32) of MxK and Matrix &B (32x32) KxN, A governs C's row and B governs C's Col.


*/