# Prereqs
- Nvidia Drivers, and CUDA Toolkit
- CUDA visible gpu per nodes
- pwdless across all nodes so MPI can launch ranks
- OpenMPI/MPICH for RHEL
`sudo apt-get install -y openmpi-bin libopenmpi-dev git build-essential`

# Build nccl-tests 
- Build once the copy across all nodes
- `git clone https://github.com/NVIDIA/nccl-tests.git`
- `cd nccl-tests`
- `make MPI=1 -j`
-- binaries output will be in ./build/

# Hostfile from launching host
- create `hosts.txt` in head node:
    =====================
	node01 slots=1
	node02 slots=1
	...
	node38 slots=1
    =====================

# Recommended nccl env
- Set the following on the head node:
`export NCCL_DEBUG=INFO`
`export NCCL_IB_DISABLE=1                 # force TCP (no RoCE/IB)`
`export NCCL_SOCKET_IFNAME=eno1           # your data NIC (e.g., eth0, bond0)`
`export NCCL_NET_GDR_LEVEL=0              # no GPUDirect RDMA over TCP`
`# Optional TCP tuning (can help on higher-speed NICs)`
`export NCCL_NSOCKS_PERTHREAD=4`
`export NCCL_SOCKET_NTHREADS=2`
`# Optional: fix algo/proto for repeatability (ring + simple good for large msgs)`
`# export NCCL_ALGO=Ring`
`# export NCCL_PROTO=Simple`

# Run all-reduce across 20 nodes
- This launches XX MPI Ranks one per host using gpu 0
- `-b 64M -e 64M -f 2` tests a single 64 MiB message (good quick check)
- `-g 1` = 1 GPU per process (per node)
`cd nccl-tests`
`mpirun -np 20 \
  --hostfile hosts.txt \
  --map-by ppr:1:node \
  -x NCCL_DEBUG -x NCCL_IB_DISABLE -x NCCL_SOCKET_IFNAME -x NCCL_NET_GDR_LEVEL \
  -x NCCL_NSOCKS_PERTHREAD -x NCCL_SOCKET_NTHREADS \
  -x CUDA_VISIBLE_DEVICES=0 \
  --mca btl ^openib \
 ./build/all_reduce_perf -b 64M -e 64M -f 2 -g 1`

- If Wrong NIC chosen → set `NCCL_SOCKET_IFNAME=<iface>` and confirm with `NCCL_DEBUG=INFO` logs.
- ` --mca btl ^openib` tells OpenMPI not to touch Infiniband verbs.
- If you want to be explicit TCP-only: `add --mca pml ob1 --mca btl tcp,self.`
- If your NIC name differs, change `NCCL_SOCKET_IFNAME.`

# Other nccl tests
- # 1 MiB to 256 MiB, power-of-two steps
`mpirun -np 20 --hostfile hosts.txt --map-by ppr:1:node -x NCCL_* -x CUDA_VISIBLE_DEVICES=0 --mca btl ^openib \
  ./build/all_reduce_perf -b 1M -e 256M -f 2 -g 1`

`./build/all_gather_perf   -b 4M  -e 64M  -f 2 -g 1`

`./build/broadcast_perf    -b 4M  -e 64M  -f 2 -g 1`

`./build/reduce_scatter_perf -b 4M -e 64M -f 2 -g 1`

