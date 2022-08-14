# GPU Architecture
GPUs have progressed from the first fixed-function architectures, to programmable
shader stages and now unified shader execution units.
Today's GPUs can execute many shader instantiations and programs in parallel,
independently of the shader stage. This is also what opened the door to a wide
variety of general purpose GPU computing (GPGPU).

## Processor Architecture
In order to leverage the data-parallel nature of the graphics processing pipeline,
large scale SIMT architectures are used.
Processors consist of multiple cores with a shared fetch/decode stage and
execution context.
Multiple SIMT processors are combined into larger complexes, which may be
repeated multiple times.
The GTX 1080 for example contains 20 "Streaming Multiprocessors",
each of which contains four 32-times-parallel SIMT processors,
resulting in a total of 2560 cores in the GPU.

## Thread Execution
Threads are executed in *warps* of 32 threads each. This matches the size of one
SIMT processor.

## Thread Divergence
Since all threads on the same SIMT processor execute the same instructions,
special attention has to be paid to conditional branching.

### Predicated instructions
Using this method:

* All threads execute the predicate
* All threads execute both branches

The thread then selects one of the results based on the predicate.

This is only viable if the branch is small, otherwise the performance cost of
executing both branches is too high.

### Voting
This approach allows the threads to vote which branch to execute.
If all threads vote for the same branch, the other branch is not executed.

Thus, care has to be taken to avoid big branches that diverge within the same
warp.

## Memory
Accessing memory introduces latency, for example on the order of 100 cycles.
The bandwidth between the processor and memory is also limited.
Stalling the processor while waiting for memory worsens utilization.

GPUs implement a memory hierarchy similar to CPUs:

The memory closest to the cores are registers, shared memory and L1 cache.
For example, the GTX 1080 features

* 256KB registers
* 96KB shared memory
* 48KB L1 cache

The cache works without explicit user control and exploits spacial and temporal
locality of data accesses.
A typical cache line size is 32 bytes, and transfer between memory and cache
happens for entire cache lines only.
Efficient usage of the cache, and proper alignment of data to cache lines are
imperative for optimal performance, the performance benefit usually originates
in reduced memory bandwidth requirements, which is often the bottleneck for
processing speed.

The GPU hides memory latency by oversubscribing the SM with warps, and executing
other warps while some wait for memory.
On the GTX 1080, each SM can be assigned 64 active warps, while it's only able
to execute four warps in parallel.

Switching between warps is fast, and is not comparable to a context switch on
the CPU.
This does however mean that the number of warps per SM (GPU occupancy) is also
limited by the total register usage.

### Shared Memory
Shared memory is fast memory close to the cores, with the restriction that it
is local to one streaming multiprocessor.
The usual use case is to explicitly move a hot region of memory to shared memory
before computation.

# Compute Shader
> **_TODO:_** Compute Shader

# Cuda
> **_TODO:_** CUDA

## Synchronization
## Concurrency: Streams
