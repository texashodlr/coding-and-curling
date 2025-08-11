nvcc -std=c++17 -arch=sm_89   main.cu run_kernels.cu  -lcublas -o gemm_bench
sleep 5
./gemm_bench 1
