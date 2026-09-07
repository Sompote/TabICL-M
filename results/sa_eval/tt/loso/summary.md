# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 0.991 ± 0.004 | 0.989 ± 0.006 | 0.988 ± 0.009 |
| block | 0.50 | 0.989 ± 0.007 | 0.987 ± 0.006 | 0.986 ± 0.006 |
| block_shift | 0.30 | 0.987 ± 0.002 | 0.986 ± 0.003 | 0.984 ± 0.005 |
| block_shift | 0.50 | 0.983 ± 0.012 | 0.980 ± 0.010 | 0.983 ± 0.012 |
| none | 0.00 | 0.996 ± 0.003 | 0.996 ± 0.003 | 0.997 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 64.201 ± 3.472 | 63.937 ± 2.679 | 62.966 ± 3.358 |
| block | 0.50 | 64.814 ± 2.757 | 64.899 ± 3.076 | 64.366 ± 3.347 |
| block_shift | 0.30 | 66.797 ± 9.616 | 67.481 ± 10.315 | 67.000 ± 9.031 |
| block_shift | 0.50 | 67.041 ± 5.100 | 68.414 ± 6.624 | 67.451 ± 6.358 |
| none | 0.00 | 56.231 ± 3.702 | 56.231 ± 3.702 | 56.065 ± 3.550 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 0.80 | 0.80 | 0.75 |
| block | 0.50 | 0.80 | 0.81 | 0.79 |
| block_shift | 0.30 | 0.75 | 0.73 | 0.71 |
| block_shift | 0.50 | 0.82 | 0.80 | 0.78 |
| none | 0.00 | 0.80 | 0.80 | 0.78 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 0.865 ± 0.024 | 0.861 ± 0.028 | 0.866 ± 0.029 |
| block | 0.50 | 0.844 ± 0.032 | 0.841 ± 0.029 | 0.841 ± 0.032 |
| block_shift | 0.30 | 0.855 ± 0.032 | 0.854 ± 0.039 | 0.846 ± 0.049 |
| block_shift | 0.50 | 0.811 ± 0.046 | 0.808 ± 0.045 | 0.799 ± 0.059 |
| none | 0.00 | 0.913 ± 0.003 | 0.913 ± 0.003 | 0.912 ± 0.003 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 0.728 ± 0.032 | 0.720 ± 0.042 | 0.726 ± 0.048 |
| block | 0.50 | 0.695 ± 0.076 | 0.704 ± 0.089 | 0.698 ± 0.082 |
| block_shift | 0.30 | 0.691 ± 0.074 | 0.671 ± 0.070 | 0.707 ± 0.076 |
| block_shift | 0.50 | 0.685 ± 0.074 | 0.676 ± 0.090 | 0.675 ± 0.096 |
| none | 0.00 | 0.814 ± 0.024 | 0.814 ± 0.024 | 0.817 ± 0.024 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 5.597 ± 0.992 | 5.555 ± 0.811 | 5.295 ± 0.791 |
| block | 0.50 | 6.289 ± 0.593 | 6.728 ± 0.784 | 6.023 ± 0.622 |
| block_shift | 0.30 | 5.671 ± 0.439 | 6.039 ± 0.614 | 5.908 ± 0.504 |
| block_shift | 0.50 | 7.418 ± 1.221 | 7.201 ± 1.213 | 6.765 ± 1.222 |
| none | 0.00 | 2.734 ± 0.483 | 2.734 ± 0.483 | 2.730 ± 0.500 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 0.80 | 0.69 | 0.71 |
| block | 0.50 | 0.79 | 0.68 | 0.74 |
| block_shift | 0.30 | 0.83 | 0.76 | 0.74 |
| block_shift | 0.50 | 0.76 | 0.73 | 0.77 |
| none | 0.00 | 0.79 | 0.79 | 0.79 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware_ewt | tabicl_aware_ewt_si | tabicl_aware_si |
|---|---|---|---|---|
| block | 0.30 | 0.995 ± 0.006 | 0.996 ± 0.005 | 0.994 ± 0.007 |
| block | 0.50 | 0.992 ± 0.008 | 0.991 ± 0.008 | 0.989 ± 0.011 |
| block_shift | 0.30 | 0.988 ± 0.009 | 0.986 ± 0.012 | 0.988 ± 0.010 |
| block_shift | 0.50 | 0.945 ± 0.044 | 0.917 ± 0.047 | 0.910 ± 0.064 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 |

## Failed fits

- diabetes / block / 0.3 / seed 2 / tabicl_aware_ewt_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 20.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 18.62 MiB is free. Process 73820 has 30.58 GiB memory in use. Including non-PyTorch memory, this process has 764.00 MiB memory in use. Of the allocated memory 165.30 MiB is allocated by PyTorch, and 4.70 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:31 / block / 0.5 / seed 0 / tabicl_aware_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 294.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 82.62 MiB is free. Process 73820 has 30.29 GiB memory in use. Including non-PyTorch memory, this process has 994.00 MiB memory in use. Of the allocated memory 352.57 MiB is allocated by PyTorch, and 47.43 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:31 / block / 0.5 / seed 0 / tabicl_aware_ewt_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 74.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 8.62 MiB is free. Process 73820 has 30.29 GiB memory in use. Including non-PyTorch memory, this process has 1.04 GiB memory in use. Of the allocated memory 346.66 MiB is allocated by PyTorch, and 127.34 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:31 / block_shift / 0.3 / seed 0 / tabicl_aware_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 158.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 116.62 MiB is free. Process 73820 has 30.35 GiB memory in use. Including non-PyTorch memory, this process has 904.00 MiB memory in use. Of the allocated memory 279.21 MiB is allocated by PyTorch, and 30.79 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:31 / block_shift / 0.3 / seed 3 / tabicl_aware_ewt_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 94.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 80.62 MiB is free. Process 73820 has 30.21 GiB memory in use. Including non-PyTorch memory, this process has 1.05 GiB memory in use. Of the allocated memory 424.04 MiB is allocated by PyTorch, and 57.96 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:1590 / block / 0.3 / seed 2 / tabicl_aware_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 176.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 20.62 MiB is free. Process 73820 has 29.55 GiB memory in use. Including non-PyTorch memory, this process has 1.77 GiB memory in use. Of the allocated memory 902.21 MiB is allocated by PyTorch, and 315.79 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:1590 / block / 0.3 / seed 2 / tabicl_aware_ewt_si: OutOfMemoryError: CUDA out of memory. Tried to allocate 176.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 20.62 MiB is free. Process 73820 has 29.55 GiB memory in use. Including non-PyTorch memory, this process has 1.77 GiB memory in use. Of the allocated memory 814.32 MiB is allocated by PyTorch, and 403.68 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)