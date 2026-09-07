# Missingness ablation

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 59.114 ± 2.843 | 59.503 ± 2.879 | 59.141 ± 2.899 | 59.137 ± 2.888 | 59.118 ± 2.840 |
| block | 0.50 | 64.716 ± 3.998 | 65.527 ± 4.184 | 64.685 ± 3.937 | 64.668 ± 3.952 | 64.696 ± 4.014 |
| block_shift | 0.30 | 58.938 ± 0.711 | 59.389 ± 0.351 | 58.966 ± 0.764 | 58.982 ± 0.788 | 58.956 ± 0.741 |
| block_shift | 0.50 | 64.148 ± 3.378 | 64.466 ± 3.985 | 64.231 ± 3.420 | 64.237 ± 3.448 | 64.159 ± 3.396 |
| none | 0.00 | 56.017 ± 3.526 | 56.213 ± 3.770 | 56.058 ± 3.544 | 56.077 ± 3.556 | 56.042 ± 3.546 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |
| block | 0.50 | 0.76 | 0.76 | 0.76 | 0.76 | 0.76 |
| block_shift | 0.30 | 0.79 | 0.79 | 0.80 | 0.80 | 0.79 |
| block_shift | 0.50 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 |
| none | 0.00 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |

## openml:189 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.181 ± 0.017 | 0.182 ± 0.018 | 0.187 ± 0.013 | 0.181 ± 0.017 | 0.181 ± 0.017 |
| block | 0.50 | 0.226 ± 0.009 | 0.227 ± 0.008 | 0.226 ± 0.009 | 0.226 ± 0.009 | 0.226 ± 0.009 |
| block_shift | 0.30 | 0.190 ± 0.012 | 0.190 ± 0.012 | 0.189 ± 0.012 | 0.189 ± 0.012 | 0.189 ± 0.012 |
| block_shift | 0.50 | 0.221 ± 0.007 | 0.222 ± 0.006 | 0.221 ± 0.007 | 0.221 ± 0.007 | 0.221 ± 0.007 |
| none | 0.00 | 0.076 ± 0.002 | 0.076 ± 0.002 | 0.075 ± 0.002 | 0.075 ± 0.002 | 0.076 ± 0.002 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| block | 0.50 | 0.81 | 0.81 | 0.81 | 0.81 | 0.81 |
| block_shift | 0.30 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| block_shift | 0.50 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| none | 0.00 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |

## openml:42225 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 980.377 ± 171.073 | 992.040 ± 166.599 | 977.116 ± 175.658 | 978.107 ± 171.100 | 980.535 ± 167.588 |
| block | 0.50 | 1214.415 ± 82.048 | 1233.445 ± 86.712 | 1214.177 ± 80.842 | 1211.412 ± 84.481 | 1212.760 ± 85.116 |
| block_shift | 0.30 | 1158.916 ± 225.271 | 1178.119 ± 238.019 | 1152.616 ± 224.539 | 1148.057 ± 223.950 | 1152.906 ± 224.604 |
| block_shift | 0.50 | 1114.001 ± 156.714 | 1130.054 ± 172.143 | 1112.568 ± 153.893 | 1110.906 ± 150.341 | 1112.571 ± 153.100 |
| none | 0.00 | 621.501 ± 74.491 | 627.886 ± 77.745 | 616.624 ± 69.360 | 615.471 ± 71.583 | 619.299 ± 75.081 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| block | 0.50 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| block_shift | 0.30 | 0.78 | 0.78 | 0.79 | 0.79 | 0.78 |
| block_shift | 0.50 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| none | 0.00 | 0.80 | 0.80 | 0.81 | 0.81 | 0.80 |

## openml:44970 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 1.000 ± 0.068 | 1.003 ± 0.070 | 0.999 ± 0.068 | 0.999 ± 0.068 | 0.999 ± 0.068 |
| block | 0.50 | 1.102 ± 0.051 | 1.109 ± 0.051 | 1.102 ± 0.051 | 1.102 ± 0.050 | 1.102 ± 0.050 |
| block_shift | 0.30 | 1.031 ± 0.031 | 1.038 ± 0.035 | 1.030 ± 0.031 | 1.030 ± 0.030 | 1.031 ± 0.030 |
| block_shift | 0.50 | 1.102 ± 0.058 | 1.108 ± 0.061 | 1.101 ± 0.058 | 1.101 ± 0.057 | 1.101 ± 0.058 |
| none | 0.00 | 0.840 ± 0.015 | 0.844 ± 0.013 | 0.839 ± 0.014 | 0.839 ± 0.014 | 0.840 ± 0.015 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 |
| block | 0.50 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| block_shift | 0.30 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |
| block_shift | 0.50 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| none | 0.00 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |

## openml:507 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.133 ± 0.006 | 0.134 ± 0.006 | 0.134 ± 0.006 | 0.134 ± 0.006 | 0.133 ± 0.006 |
| block | 0.50 | 0.155 ± 0.013 | 0.156 ± 0.014 | 0.155 ± 0.013 | 0.155 ± 0.013 | 0.155 ± 0.013 |
| block_shift | 0.30 | 0.160 ± 0.013 | 0.160 ± 0.013 | 0.160 ± 0.013 | 0.160 ± 0.013 | 0.160 ± 0.013 |
| block_shift | 0.50 | 0.169 ± 0.008 | 0.169 ± 0.008 | 0.169 ± 0.008 | 0.169 ± 0.008 | 0.169 ± 0.008 |
| none | 0.00 | 0.108 ± 0.012 | 0.108 ± 0.012 | 0.108 ± 0.012 | 0.108 ± 0.012 | 0.108 ± 0.012 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.78 | 0.78 | 0.77 | 0.77 | 0.78 |
| block | 0.50 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| block_shift | 0.30 | 0.77 | 0.77 | 0.78 | 0.78 | 0.77 |
| block_shift | 0.50 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 |
| none | 0.00 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 3.653 ± 0.496 | 3.679 ± 0.555 | 3.626 ± 0.485 | 3.615 ± 0.470 | 3.640 ± 0.484 |
| block | 0.50 | 4.770 ± 0.649 | 4.797 ± 0.668 | 4.764 ± 0.648 | 4.756 ± 0.647 | 4.763 ± 0.647 |
| block_shift | 0.30 | 4.369 ± 0.620 | 4.513 ± 0.654 | 4.377 ± 0.626 | 4.378 ± 0.622 | 4.368 ± 0.620 |
| block_shift | 0.50 | 4.616 ± 0.840 | 4.663 ± 0.924 | 4.599 ± 0.968 | 4.605 ± 0.844 | 4.615 ± 0.847 |
| none | 0.00 | 2.697 ± 0.477 | 2.697 ± 0.496 | 2.683 ± 0.468 | 2.681 ± 0.462 | 2.693 ± 0.468 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.79 | 0.79 | 0.79 | 0.79 | 0.79 |
| block | 0.50 | 0.76 | 0.76 | 0.75 | 0.75 | 0.76 |
| block_shift | 0.30 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| block_shift | 0.50 | 0.76 | 0.76 | 0.77 | 0.77 | 0.76 |
| none | 0.00 | 0.77 | 0.77 | 0.78 | 0.78 | 0.77 |

## openml:560 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 3.715 ± 0.657 | 3.748 ± 0.632 | 3.717 ± 0.651 | 3.715 ± 0.660 | 3.713 ± 0.665 |
| block | 0.50 | 4.026 ± 0.877 | 4.043 ± 0.861 | 4.029 ± 0.893 | 4.032 ± 0.890 | 4.028 ± 0.872 |
| block_shift | 0.30 | 3.464 ± 0.650 | 3.480 ± 0.661 | 3.461 ± 0.642 | 3.459 ± 0.644 | 3.462 ± 0.652 |
| block_shift | 0.50 | 3.738 ± 1.162 | 3.770 ± 1.139 | 3.751 ± 1.167 | 3.733 ± 1.171 | 3.721 ± 1.167 |
| none | 0.00 | 1.622 ± 0.556 | 1.680 ± 0.619 | 1.621 ± 0.560 | 1.622 ± 0.575 | 1.623 ± 0.571 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_aware_med | tabicl_aware_n32 | tabicl_aware_n32_ypow | tabicl_aware_ypow |
|---|---|---|---|---|---|---|
| block | 0.30 | 0.77 | 0.77 | 0.78 | 0.78 | 0.77 |
| block | 0.50 | 0.81 | 0.81 | 0.82 | 0.82 | 0.81 |
| block_shift | 0.30 | 0.72 | 0.72 | 0.72 | 0.72 | 0.72 |
| block_shift | 0.50 | 0.72 | 0.72 | 0.72 | 0.72 | 0.72 |
| none | 0.00 | 0.87 | 0.87 | 0.88 | 0.88 | 0.87 |

## Failed fits

- openml:531 / block_shift / 0.5 / seed 3 / tabicl_aware_n32: OutOfMemoryError: CUDA out of memory. Tried to allocate 144.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 140.62 MiB is free. Including non-PyTorch memory, this process has 1022.00 MiB memory in use. Process 101557 has 30.21 GiB memory in use. Of the allocated memory 287.59 MiB is allocated by PyTorch, and 140.41 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)
- openml:189 / block / 0.3 / seed 2 / tabicl_aware_n32: OutOfMemoryError: CUDA out of memory. Tried to allocate 142.00 MiB. GPU 0 has a total capacity of 31.36 GiB of which 102.62 MiB is free. Including non-PyTorch memory, this process has 1.58 GiB memory in use. Process 101557 has 29.66 GiB memory in use. Of the allocated memory 921.41 MiB is allocated by PyTorch, and 102.59 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)