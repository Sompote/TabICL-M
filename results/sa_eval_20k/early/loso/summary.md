# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.992 ± 0.002 |
| block | 0.50 | 0.989 ± 0.007 |
| block_shift | 0.30 | 0.986 ± 0.003 |
| block_shift | 0.50 | 0.985 ± 0.010 |
| none | 0.00 | 0.997 ± 0.003 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.869 ± 0.031 |
| block | 0.50 | 0.847 ± 0.034 |
| block_shift | 0.30 | 0.856 ± 0.044 |
| block_shift | 0.50 | 0.815 ± 0.042 |
| none | 0.00 | 0.913 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.719 ± 0.040 |
| block | 0.50 | 0.701 ± 0.081 |
| block_shift | 0.30 | 0.702 ± 0.067 |
| block_shift | 0.50 | 0.685 ± 0.089 |
| none | 0.00 | 0.817 ± 0.024 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware |
|---|---|---|
| block | 0.30 | 0.997 ± 0.004 |
| block | 0.50 | 0.992 ± 0.008 |
| block_shift | 0.30 | 0.989 ± 0.007 |
| block_shift | 0.50 | 0.941 ± 0.052 |
| none | 0.00 | 1.000 ± 0.000 |

## Failed fits

- breast_cancer / block / 0.3 / seed 3 / tabicl_aware: OutOfMemoryError: CUDA out of memory. Tried to allocate 20.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 2.62 MiB is free. Process 81034 has 30.57 GiB memory in use. Including non-PyTorch memory, this process has 784.00 MiB memory in use. Of the allocated memory 179.69 MiB is allocated by PyTorch, and 12.31 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:31 / block / 0.3 / seed 0 / tabicl_aware: OutOfMemoryError: CUDA out of memory. Tried to allocate 16.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 16.62 MiB is free. Process 81034 has 30.53 GiB memory in use. Including non-PyTorch memory, this process has 818.00 MiB memory in use. Of the allocated memory 205.80 MiB is allocated by PyTorch, and 20.20 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:1590 / block / 0.3 / seed 2 / tabicl_aware: OutOfMemoryError: CUDA out of memory. Tried to allocate 88.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 88.62 MiB is free. Process 81034 has 29.91 GiB memory in use. Including non-PyTorch memory, this process has 1.34 GiB memory in use. Of the allocated memory 573.20 MiB is allocated by PyTorch, and 206.80 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)