#pragma once

#include <cstdio>
#include <cstdlib>
#include <cublas_v2.h>
#include <cuda_runtime.h>

/*

Matrix Sizes
MxK * KxN = MxN

*/

// Given a 4096x4096 * 4096x4096 = 4096

__global__ void sgemm_naive (int M, int N, int K, float alpha, const float *A, const float *B, float beta, float *C){
    
    // Compute the position in C that this thread is responsible for
    const uint x = blockIdx.x * blockDim.x + threadIdx.x;
    const uint y = blockIdx.y * blockDim.y + threadIdx.y;


    // The full grid 'C' is filled with as many blocks as possible into the grid as necessary to span all of 'C'
    // Block dims are 32(x),32(y),1(z)
    // So a Grid of M=N=K=4096 is (4096/32) ---> Grid(128(x),128(y),1)
    // Threads: row of A is 'K' and col of B is 'K'
    // When we don't have a matrix that isn't divisible by the size of the block
    /*
        Then we'll have to launch extra blocks to process the remainder, that remainder
        is called tile quantization and appears when mapping a fixed size volume across a variable sized input.

        Fore each of 4096x4096 entries of 'C' we have to perform a Dot-Prod of the two vectors
        of size 4096 involving a multiply and add at each step. Multiply then Add which is two FLOPs
        Thus total flops = 2*4096^3 + 4096^2 = 137GFLOPs
            --> AxB each of the 4096^2 outputs is a dot product of length 'n' so multiplications:
                    --> n^2 * n = n^3
                    --> So total flops = Multiplications n^3 + additions n^2 = 2n^3
                    --> So generally in a total flop world we're thinking about 2n^3
        and Total data to read: 3*4096^2 * 4B (Float=4B)
            --> We have to read A, B, C (3 matrices) each n^2 elements 4B/element
            --> 3*n^2*4B = 201MB
        and Total data to store: 4096^2 * 4B
            --> Since we write one n^2 output matrix (either overwriting C or D)
            --> n^2*4B = 67MB
    
    */
    // If statement is necesary to make things work under tile quantization
    if (x < M && y < N){
        float tmp = 0.0;
        for (int i = 0; i < K; ++i){
            tmp += A[x*K+i] * B[i*N+y];
        }
        C[x*N+y] = alpha*tmp+beta*C[x*N+y];
    }
}


/*
Considering we're operating an Nvidia RTX 4070
1. 15.6 TFLOPs/s of FP32
2. 256GB/s
3. 4608 CUDA Cores
4. 8188MiB of GDDR6.

Looking to ours we've got projected 137GFLOPs --> 100*(0.137/15.6)=.00878205s 
                                    268MB --> 268MB/256GB/s = .00105s
                                    Net net --> Compute is ~10x Memory xfer
                                    So we're compute bound!

*/