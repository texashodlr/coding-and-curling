export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
nvcc -std=c++17 -arch=sm_89   main.cu run_kernels.cu  -lcublas -o gemm_bench
sleep 5
echo 'Running Naive GEMM!\n'
sleep 1
./gemm_bench 1
sleep 1
echo 'Running GEMM with Global Memory Coalescing!\n'
./gemm_bench 2
sleep 1

