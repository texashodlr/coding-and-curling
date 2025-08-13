#pragma once

#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cublas_v2.h>
#include <cuda_runtime.h>

template <const uint BLOCKSIZE>
__global__ void sgemm_global_mem_coalesce(int M, int N, int K, float alpha, const float *A, const float *B, float beta, float *C){
    const int cRow = blockIdx.x * BLOCKSIZE + (threadIdx.x / BLOCKSIZE);
    const int cCol = blockIdx.y * BLOCKSIZE + (threadIdx.x % BLOCKSIZE);

    if (cRow < M && cCol < N){
        float tmp = 0.0;
        for (int i=0; i < K; ++i){
            tmp += A[cRow*K+i]*B[i*N+cCol];
        }
        C[cRow*N+cCol] = alpha*tmp + beta*C[cRow*N+cCol];
    }
}

__global__ void sgemm_global_mem_coalesce_varied(int DIM, int M, int N, int K, float alpha, const float *A, const float *B, float beta, float *C){
    const int cRow = blockIdx.x * DIM + (threadIdx.x / DIM);
    const int cCol = blockIdx.y * DIM + (threadIdx.x % DIM);

    if (cRow < M && cCol < N){
        float tmp = 0.0;
        for (int i=0; i < K; ++i){
            tmp += A[cRow*K+i]*B[i*N+cCol];
        }
        C[cRow*N+cCol] = alpha*tmp + beta*C[cRow*N+cCol];
    }
}

/*
    Recap: Warps are groups of 32 threads, assigned to a warp scheduler
        which is the physical core that executes the instructions. Four Warp Sched/MultiProc
    
        With multi-dim blocks the threadIds are counted thusly:
         threadId = threadIdx.x+blockDim.x*threadIdx.y+blockDim.y*threadIdx.z)

    Important to consider when we think in three dimensional threadblock space
        So an X/Y/Z block could have (with threads)
            threadIdx.x,y,z: 0,0,0 && 1,0,0 ...... 0,1,0 etc.

    Moving away from the naive kernel (just inefficiently throwing cycles at a kernel)
        to now trying to sequentially align memory accesses which is where we see greater flop util
    
    In this kernel we've done global memory coalescing in an effort to reach our aforementioned peak bandwidth

    Per the article the GPU support 32B, 64B, 128B memory accesses so take a 32b float loaded from
    gmem and 32*4B (32 th) = 128B in a single transaction which assumes that we load consecutively
        and with aligned accesses
        Otherwise the GPU will waste bandwidth and execute a lot of haphazard loads
    
    Our previous kernel (naive) was really a brute-force thread centric-model where we just enabled
        concurrent accesses of the threads 
    
    Reformatting our approach to gmem coal we must change how we assign positions of the result matrix C
        to the threads.
    
    ## Matrix Memory Layout ##
    Matrix A:  NxN --> consecutive in memory is walking down row k (of n), left to right from col 0 -> N-1
        These are consecutive accesses and don't (theoretically incur bandwidth issues)
    Matrix B: NxN --> Non-consecutive in memory is walking down col k (of N) top to bottom
        accessing a unique row element holding the col constant --> This isn't efficient.
        This method produces an element in C.
    
    ## Naive ##
    In the naive model we have our threads access non-consecutive values that cannot coalesce
    All threads access the same repeat column values in B and produce blocks down a column of C
    But there's no benefit as the resultant C all has non consecutive solutions/accesse.

    So maybe you hold the row constant in A and walk different columns in B?

    ## Gmem coal
    A: All threads access the same values within warp broadcast
    B: All threads access consecutive (cols left to right) values thusly enabling coalescing.
    C: Resultant C matrix then has produced blocks across resultant Row N (left to right) and we
        /win/ when the resultant blocks go left to right successfully in coalesced memory!
    
    This is all implemented merely chaning the assignment of threads and that logic.

     // NAIVE //
    const uint x = blockIdx.x * blockDim.x + threadIdx.x;
    const uint y = blockIdx.y * blockDim.y + threadIdx.y;

    // GMEM //
    const int x = blockIdx.x * BLOCKSIZE + (threadIdx.x / BLOCKSIZE);
    const int y = blockIdx.y * BLOCKSIZE + (threadIdx.x % BLOCKSIZE);
        This comes with a blockDim of 1D 32x32 instead of a psuedo 3D 32x32x1

    Which we can oscilate the size

*/