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

/*
    Recap: Warps are groups of 32 threads, assigned to a warp scheduler
        which is the physical core that executes the instructions. Four Warp Sched/MultiProc
    
        With multi-dim blocks the threadIds are counted thusly:
         threadId = threadIdx.x+blockDim.x*threadIdx.y+blockDim.y*threadIdx.z)

*/