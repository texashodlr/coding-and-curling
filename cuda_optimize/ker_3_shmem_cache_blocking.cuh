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
    // 1. Beginning with resultant matrix (&C) init for the thread block
    const uint cRow = blockIdx.x;
    const uint cCol = blockIdx.y;

    // Allocate buffer for current block in fast shared mem
    // shared mem is /shared/ between all threads in a block
    // 2. An array of 32*32 float (4B) so ends up being 2*4096B shared across the thread block
    //  because everything being done is within the thread block (shared)
    // shared memory is block scoped! So this thread block is generating 8192B of shared memory

    __shared__ float As[BLOCKSIZE*BLOCKSIZE];
    __shared__ float Bs[BLOCKSIZE*BLOCKSIZE];

    // the inner row and col that we're accessing in this thread
    // 3. threadCol = :1024 % 32 == :32
    //    threadRow = :1024 / 32 == :32
    // Because the block is one dimensional and 1024 threads we only concern ourselves
    // with threadIdx.x but then have to account for the cols/rows with translation of threads to that.
    const uint threadCol = threadIdx.x % BLOCKSIZE;
    const uint threadRow = threadIdx.x / BLOCKSIZE;

    // Advance pointers to the starting positions
    // 4. In theory A points to the top left of the block of the cRow'th
    //              B points to the 'top' right of the cCol'th
    //              C points to the cRow'th's cCol'th
    // A ends up being the vertical bounds, B the horizontal bounds, C the actual point

    A += cRow * BLOCKSIZE * K;                  // row=cRow, col=0
    B += cCol * BLOCKSIZE;                      // row=0, col=cCol
    C += cRow * BLOCKSIZE * N +cCol * BLOCKSIZE;// row=cRow, col=cCol

    float tmp = 0.0;
    // The outer loop of this bkIdx for loop advances A along the columns and B
    // along the rows until we have fully calculated the result in C
    // Remembering that K is the same value as M and N
    // We increment bkIdx by (32)
    for (int bkIdx = 0; bkIdx < K; bkIdx += BLOCKSIZE){
        // Have each thread load one of the elements in A & B
        // from gmem into shmem
        // make the threadCol(=threadIdx.x) the consecutive index
        // to allow gmem access coal
        As[threadRow * BLOCKSIZE + threadCol] = A[threadRow*K + threadCol]; // BY k
        Bs[threadRow * BLOCKSIZE + threadCol] = B[threadRow*N + threadCol]; // BY n

        // block threads in this block until cache is fully populated 
        __syncthreads();

        // Once the sync'ng is finished we can advance A and B (pointers)
        // Onto the next chunk
        A += BLOCKSIZE;
        B += BLOCKSIZE * N;

        // Execute the dotproduct on the currently cached block
        // Which is the items currently loaded into the cache (As and Bs)
        // This iterates BLOCKSIZE (32) times via dotIdx.
        // So for Row 2, Col 1 it might look like:
        //      As[2*32+:32] * Bs[:32*32 + 1] thus you're summing all of that into tmp
        for (int dotIdx = 0; dotIdx < BLOCKSIZE; ++dotIdx){
            tmp += As[threadRow * BLOCKSIZE + dotIdx] * Bs[dotIdx * BLOCKSIZE + threadCol];
        }

        // Need to sync again at the end to avoid faster threads/race conditions
        // Fetching the next block into the cache block before slower threads are done
        __syncthreads();
    }
    // Therefore C's idx of MxK * KxN == MxN
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

Our 4070 has a 48KB of shmem, and inside this kernel we're only using 8KB so we've still got 6x
    more capacity to load into shmem, our 4070 has 36 SMs, which caps out at 100KB of shared mem.
    But increasing per-block SHMEM then necessarily decreases the number of blocks we can host on the SM.
    So increasing blocks to utilize 48KB would leave at most room for another block so 2 Blocks/SM at that rate.
    Decreasing occupancy (ratio of max possible number of warps per SM (which is 1024 threads/32 th./warp)).
    High occupancy allows us to hide the high latency of our operations by having a bigger pool of issuable instructions avail.
    There are three main limits to keeping more active blocks loaded on an SM
        1. Register count
        2. Warp count
        3. SMEM Cap.

We obtain these device stats:
    Running kernel 4 on device 0.
Device ID: 0
    Name: NVIDIA GeForce RTX 4070 Laptop GPU
    Compute Capability: 8.9
    memoryBusWidth: 128
    maxThreadsPerBlock: 1024
    maxThreadsPerMultiProcessor: 1536
    maxRegsPerBlock: 65536
    maxRegsPerMultiProcessor: 65536
    totalGlobalMem: 8187MB
    sharedMemPerBlock: 48KB
    sharedMemPerMultiprocessor: 100KB
    totalConstMem: 64KB
    multiProcessorCount: 36
    Warp Size: 32

Our kernel assumes:
    1. 37 Registers/thread
    2. 8192B SMEM per block
    3.  1024 threads per block

With shared memory: 8192B/block + 1024B of CUDA runtime shmem/block gives
    9216B/block with 100KB/9218B == 11 Block upper limit per SM.

With threads: 1024 threads per block && 1536 threads per SM upper limit of 1  Block per SM.

With register: 37 Regs/th * 32th per warp == 1184 regs/warp
    Register allocation granularity is 256/warp so 256*5 = 1280 reg/warp (96 wasted?)
    1024 threads/32 == 32 warps per block so 32 warps * 1280 regs = 40960/ block which is under
        the 65K reg/block and SM.

So the real limiter here in this kernel is our threads per block and regsiter per thread
    We have one block per SM with a max of 48 active warps (1536/32) but only use 32 so 32/48 = 66% occupancy
The inner most loop in PTX is basically just loads
    ###
    ld.shared.f32 %f91, [%r8+3456];
    ld.shared.f32 %f92, [%r7+108];
    fma.rn.f32    %f93, %f92, %f91, %f90
    ###
Which is bad considering that loading is going to be massively latnency inducing!
    We spend most of the time loading not FMA'ng!

Warp stalling then occurs via MOI (memory in/out) insn queue. (ShMEM insns).

So rather then each thread loading a shmeme, can we reduce the number of shmem loads?
...Yes, by using our registers instead!
*/