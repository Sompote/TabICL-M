# Source-aware TabICL-M against the baselines

`tabicl_m_sa` = source-aware stage-4 checkpoint (`checkpoints/tabicl-m-sa/*/step-10000.ckpt`); `tabicl_aware` = first stage-4 checkpoint (3000 steps, value-level parts only); `tabicl_impute` = released TabICLv2 with mean imputation; `tabpfn` = TabPFN v2. Mean over 5 seeds; bold = best in row.

## Leave-one-source-out (held-out synthetic source)

| dataset | condition | `tabicl_impute` | `tabicl_indicator` | `tabicl_patternnorm` | `tabicl_iterimpute` | `tabicl_knnimpute` | `tabicl_aware_zero` | `tabicl_aware` | `tabicl_m_sa` | `tabpfn` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | complete@0.0 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.997 | **0.997** | 0.996 | 0.995 | 0.996 |
| breast_cancer (AUC) | block@0.5 | 0.968 | 0.972 | 0.967 | 0.953 | 0.984 | 0.975 | 0.977 | **0.989** | 0.980 | 0.964 | 0.972 |
| breast_cancer (AUC) | block_shift@0.5 | 0.963 | 0.970 | 0.960 | 0.881 | 0.961 | 0.969 | 0.973 | **0.984** | 0.980 | 0.964 | 0.955 |
| wine (AUC) | complete@0.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 | 0.997 | 0.998 |
| wine (AUC) | block@0.5 | 0.990 | 0.990 | 0.988 | 0.938 | 0.990 | 0.989 | 0.989 | 0.992 | **0.992** | 0.968 | 0.958 |
| wine (AUC) | block_shift@0.5 | 0.914 | 0.923 | **0.971** | 0.807 | 0.870 | 0.905 | 0.905 | 0.932 | 0.927 | 0.897 | 0.806 |
| diabetes (RMSE) | complete@0.0 | 55.79 | 55.79 | **55.79** | 55.79 | 55.79 | 55.79 | 55.90 | 56.06 | 56.20 | 62.92 | 59.55 |
| diabetes (RMSE) | block@0.5 | 66.36 | 66.03 | 66.96 | 71.24 | 66.77 | 66.14 | 64.52 | **63.99** | 65.61 | 79.42 | 73.23 |
| diabetes (RMSE) | block_shift@0.5 | 69.10 | 68.49 | 69.51 | 72.81 | 67.93 | 68.94 | 67.73 | **65.15** | 66.95 | 79.01 | 78.81 |
| credit-g (AUC) | complete@0.0 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.815 | **0.817** | 0.806 | 0.798 | 0.802 |
| credit-g (AUC) | block@0.5 | 0.704 | 0.705 | 0.690 | 0.637 | 0.658 | **0.706** | 0.704 | 0.702 | 0.683 | 0.633 | 0.603 |
| credit-g (AUC) | block_shift@0.5 | 0.683 | 0.677 | 0.680 | 0.652 | 0.682 | 0.680 | 0.673 | **0.683** | 0.665 | 0.637 | 0.624 |
| adult (AUC) | complete@0.0 | 0.912 | 0.912 | 0.908 | 0.912 | 0.912 | 0.912 | 0.912 | 0.913 | **0.916** | 0.897 | 0.896 |
| adult (AUC) | block@0.5 | **0.847** | 0.844 | 0.841 | 0.780 | 0.821 | 0.845 | 0.846 | 0.847 | 0.842 | 0.823 | 0.802 |
| adult (AUC) | block_shift@0.5 | 0.800 | **0.816** | 0.813 | 0.677 | 0.774 | 0.813 | 0.806 | 0.810 | 0.816 | 0.793 | 0.783 |
| boston (RMSE) | complete@0.0 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.72 | 2.73 | **2.70** | 3.23 | 2.82 |
| boston (RMSE) | block@0.5 | 5.84 | 5.84 | 6.15 | 10.22 | 5.89 | 6.05 | 5.98 | **5.48** | 6.29 | 11.48 | 8.03 |
| boston (RMSE) | block_shift@0.5 | 7.08 | 7.16 | 6.88 | 7.91 | 7.54 | 7.00 | 6.81 | **6.72** | 7.20 | 8.64 | 9.49 |

### loso: `tabicl_m_sa` vs `tabicl_impute`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 18 / 2 | +0.0129 |
| wine | AUC | 12 / 6 | +0.0089 |
| diabetes | RMSE | 19 / 1 | +2.0886 |
| credit-g | AUC | 8 / 12 | -0.0005 |
| adult | AUC | 14 / 6 | +0.0078 |
| boston | RMSE | 13 / 7 | +0.4194 |

### loso: `tabicl_m_sa` vs `tabicl_aware`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 17 / 2 | +0.0076 |
| wine | AUC | 14 / 4 | +0.0104 |
| diabetes | RMSE | 14 / 6 | +1.1846 |
| credit-g | AUC | 11 / 9 | +0.0025 |
| adult | AUC | 10 / 10 | +0.0043 |
| boston | RMSE | 15 / 5 | +0.2611 |

### loso: `tabicl_m_sa` vs `tabpfn`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 19 / 1 | +0.0062 |
| wine | AUC | 10 / 8 | +0.0056 |
| diabetes | RMSE | 14 / 6 | +1.2450 |
| credit-g | AUC | 16 / 4 | +0.0139 |
| adult | AUC | 13 / 7 | +0.0042 |
| boston | RMSE | 14 / 6 | +0.6287 |

### loso: `tabicl_m_sa` vs `tabicl_patternnorm`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 17 / 3 | +0.0132 |
| wine | AUC | 10 / 9 | -0.0033 |
| diabetes | RMSE | 16 / 4 | +0.9524 |
| credit-g | AUC | 14 / 6 | +0.0072 |
| adult | AUC | 14 / 6 | -0.0007 |
| boston | RMSE | 13 / 7 | +0.4167 |

### loso: `tabicl_m_sa` vs `tabicl_impute`, block_shift only

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 10 / 0 | +0.0125 |
| wine | AUC | 8 / 2 | +0.0089 |
| diabetes | RMSE | 10 / 0 | +2.4218 |
| credit-g | AUC | 4 / 6 | +0.0005 |
| adult | AUC | 7 / 3 | +0.0147 |
| boston | RMSE | 7 / 3 | +0.5517 |

### loso: 80 % interval coverage / width, regression, block_shift@0.5

|                                    |   coverage80 |   width80 |
|:-----------------------------------|-------------:|----------:|
| ('boston', 'tabicl_aware')         |        0.83  |     1.777 |
| ('boston', 'tabicl_aware_zero')    |        0.865 |     2.017 |
| ('boston', 'tabicl_impute')        |        0.867 |     2.138 |
| ('boston', 'tabicl_indicator')     |        0.863 |     2.149 |
| ('boston', 'tabicl_iterimpute')    |        0.916 |     3.19  |
| ('boston', 'tabicl_knnimpute')     |        0.759 |     1.811 |
| ('boston', 'tabicl_m_sa')          |        0.81  |     1.598 |
| ('boston', 'tabicl_patternnorm')   |        0.824 |     1.668 |
| ('diabetes', 'tabicl_aware')       |        0.787 |     2.184 |
| ('diabetes', 'tabicl_aware_zero')  |        0.819 |     2.327 |
| ('diabetes', 'tabicl_impute')      |        0.827 |     2.361 |
| ('diabetes', 'tabicl_indicator')   |        0.824 |     2.361 |
| ('diabetes', 'tabicl_iterimpute')  |        0.813 |     2.384 |
| ('diabetes', 'tabicl_knnimpute')   |        0.759 |     2.016 |
| ('diabetes', 'tabicl_m_sa')        |        0.818 |     2.24  |
| ('diabetes', 'tabicl_patternnorm') |        0.818 |     2.376 |

## Random split

| dataset | condition | `tabicl_impute` | `tabicl_indicator` | `tabicl_patternnorm` | `tabicl_iterimpute` | `tabicl_knnimpute` | `tabicl_aware_zero` | `tabicl_aware` | `tabicl_m_sa` | `tabpfn` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| breast_cancer (AUC) | complete@0.0 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.996 | 0.997 | **0.997** | 0.996 | 0.995 | 0.996 |
| breast_cancer (AUC) | block@0.5 | 0.995 | 0.996 | **0.996** | 0.994 | 0.994 | 0.995 | 0.995 | 0.996 | 0.995 | 0.991 | 0.993 |
| breast_cancer (AUC) | block_shift@0.5 | **0.994** | 0.994 | 0.994 | 0.994 | 0.991 | 0.994 | 0.994 | 0.994 | 0.994 | 0.987 | 0.990 |
| wine (AUC) | complete@0.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 | 0.997 | 0.998 |
| wine (AUC) | block@0.5 | 0.996 | 0.996 | 0.995 | 0.994 | 0.993 | **0.997** | 0.996 | 0.996 | 0.995 | 0.989 | 0.984 |
| wine (AUC) | block_shift@0.5 | 0.989 | 0.988 | 0.989 | 0.984 | 0.985 | 0.989 | **0.990** | 0.989 | 0.986 | 0.976 | 0.981 |
| diabetes (RMSE) | complete@0.0 | 55.79 | 55.79 | **55.79** | 55.79 | 55.79 | 55.79 | 55.90 | 56.06 | 56.20 | 62.92 | 59.55 |
| diabetes (RMSE) | block@0.5 | 65.34 | 65.37 | 65.46 | 64.95 | 65.89 | 65.12 | 64.87 | **64.76** | 64.93 | 71.66 | 68.76 |
| diabetes (RMSE) | block_shift@0.5 | 64.78 | 64.67 | 65.21 | 64.49 | 66.59 | 65.06 | 64.78 | **64.23** | 64.66 | 74.13 | 69.41 |
| credit-g (AUC) | complete@0.0 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.814 | 0.815 | **0.817** | 0.806 | 0.798 | 0.802 |
| credit-g (AUC) | block@0.5 | 0.722 | 0.723 | 0.726 | 0.721 | 0.705 | 0.721 | 0.723 | 0.721 | **0.731** | 0.698 | 0.695 |
| credit-g (AUC) | block_shift@0.5 | 0.727 | 0.727 | 0.726 | 0.698 | 0.709 | 0.726 | **0.728** | 0.725 | 0.716 | 0.677 | 0.695 |
| adult (AUC) | complete@0.0 | 0.912 | 0.912 | 0.908 | 0.912 | 0.912 | 0.912 | 0.912 | 0.913 | **0.916** | 0.897 | 0.896 |
| adult (AUC) | block@0.5 | 0.865 | 0.851 | 0.864 | 0.839 | 0.853 | 0.866 | 0.868 | 0.869 | **0.869** | 0.850 | 0.853 |
| adult (AUC) | block_shift@0.5 | 0.859 | 0.838 | 0.857 | 0.834 | 0.849 | 0.859 | 0.861 | 0.860 | **0.861** | 0.836 | 0.843 |
| boston (RMSE) | complete@0.0 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.71 | 2.72 | 2.73 | **2.70** | 3.23 | 2.82 |
| boston (RMSE) | block@0.5 | 4.84 | 4.86 | 4.84 | 5.07 | 5.21 | 4.83 | 4.82 | **4.79** | 4.87 | 5.19 | 4.98 |
| boston (RMSE) | block_shift@0.5 | 4.70 | 4.66 | 4.76 | 5.13 | 4.86 | 4.67 | 4.68 | **4.66** | 4.77 | 5.41 | 5.08 |

### random_split: `tabicl_m_sa` vs `tabicl_impute`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 9 / 10 | +0.0001 |
| wine | AUC | 5 / 8 | +0.0002 |
| diabetes | RMSE | 14 / 6 | +0.4158 |
| credit-g | AUC | 11 / 9 | +0.0007 |
| adult | AUC | 14 / 6 | +0.0018 |
| boston | RMSE | 12 / 8 | +0.0503 |

### random_split: `tabicl_m_sa` vs `tabicl_aware`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 10 / 8 | +0.0001 |
| wine | AUC | 4 / 9 | -0.0002 |
| diabetes | RMSE | 9 / 11 | +0.1621 |
| credit-g | AUC | 9 / 11 | +0.0002 |
| adult | AUC | 12 / 8 | +0.0005 |
| boston | RMSE | 10 / 10 | +0.0079 |

### random_split: `tabicl_m_sa` vs `tabpfn`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 14 / 6 | +0.0005 |
| wine | AUC | 13 / 3 | +0.0019 |
| diabetes | RMSE | 14 / 6 | +0.3619 |
| credit-g | AUC | 11 / 9 | +0.0047 |
| adult | AUC | 10 / 10 | -0.0003 |
| boston | RMSE | 16 / 4 | +0.0659 |

### random_split: `tabicl_m_sa` vs `tabicl_patternnorm`, paired over block + block_shift, rates 0.3/0.5, 5 seeds

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 7 / 10 | +0.0002 |
| wine | AUC | 7 / 7 | +0.0005 |
| diabetes | RMSE | 13 / 7 | +0.5290 |
| credit-g | AUC | 11 / 9 | +0.0022 |
| adult | AUC | 15 / 5 | +0.0036 |
| boston | RMSE | 14 / 6 | +0.0480 |

### random_split: `tabicl_m_sa` vs `tabicl_impute`, block_shift only

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 5 / 4 | +0.0003 |
| wine | AUC | 2 / 5 | -0.0003 |
| diabetes | RMSE | 8 / 2 | +0.3889 |
| credit-g | AUC | 5 / 5 | -0.0002 |
| adult | AUC | 7 / 3 | +0.0018 |
| boston | RMSE | 4 / 6 | +0.0174 |

### random_split: 80 % interval coverage / width, regression, block_shift@0.5

|                                    |   coverage80 |   width80 |
|:-----------------------------------|-------------:|----------:|
| ('boston', 'tabicl_aware')         |        0.779 |     1.151 |
| ('boston', 'tabicl_aware_zero')    |        0.771 |     1.135 |
| ('boston', 'tabicl_impute')        |        0.776 |     1.164 |
| ('boston', 'tabicl_indicator')     |        0.779 |     1.169 |
| ('boston', 'tabicl_iterimpute')    |        0.745 |     1.196 |
| ('boston', 'tabicl_knnimpute')     |        0.811 |     1.298 |
| ('boston', 'tabicl_m_sa')          |        0.763 |     1.12  |
| ('boston', 'tabicl_patternnorm')   |        0.778 |     1.173 |
| ('diabetes', 'tabicl_aware')       |        0.767 |     2.014 |
| ('diabetes', 'tabicl_aware_zero')  |        0.758 |     2.013 |
| ('diabetes', 'tabicl_impute')      |        0.785 |     2.049 |
| ('diabetes', 'tabicl_indicator')   |        0.78  |     2.053 |
| ('diabetes', 'tabicl_iterimpute')  |        0.785 |     2.109 |
| ('diabetes', 'tabicl_knnimpute')   |        0.791 |     2.116 |
| ('diabetes', 'tabicl_m_sa')        |        0.783 |     2.016 |
| ('diabetes', 'tabicl_patternnorm') |        0.783 |     2.052 |

## Standard ablation (random split, mcar / mar / mnar / block at 0.5)

| dataset | condition | `tabicl_impute` | `tabicl_aware` | `tabicl_m_sa` | `xgboost` | `catboost` |
|---|---|---|---|---|---|---|
| breast_cancer (AUC) | complete@0.0 | 0.996 | **0.996** | 0.996 | 0.995 | 0.995 |
| breast_cancer (AUC) | mcar@0.5 | 0.989 | 0.990 | **0.991** | 0.987 | 0.980 |
| breast_cancer (AUC) | mar@0.5 | 0.990 | 0.989 | **0.991** | 0.987 | 0.987 |
| breast_cancer (AUC) | mnar@0.5 | 0.990 | 0.992 | **0.992** | 0.986 | 0.990 |
| breast_cancer (AUC) | block@0.5 | 0.994 | 0.994 | 0.994 | 0.990 | 0.991 |
| wine (AUC) | complete@0.0 | 1.000 | **1.000** | 1.000 | 0.996 | 0.997 |
| wine (AUC) | mcar@0.5 | 0.980 | 0.981 | **0.985** | 0.948 | 0.949 |
| wine (AUC) | mar@0.5 | 0.985 | 0.985 | **0.987** | 0.973 | 0.965 |
| wine (AUC) | mnar@0.5 | 0.993 | **0.994** | 0.992 | 0.985 | 0.980 |
| wine (AUC) | block@0.5 | 0.994 | **0.998** | 0.995 | 0.989 | 0.982 |
| diabetes (RMSE) | complete@0.0 | 56.57 | 56.65 | 56.88 | 62.05 | 59.74 |
| diabetes (RMSE) | mcar@0.5 | 65.60 | 65.10 | **64.14** | 69.93 | 69.84 |
| diabetes (RMSE) | mar@0.5 | **61.47** | 61.60 | 61.91 | 67.37 | 63.41 |
| diabetes (RMSE) | mnar@0.5 | 62.69 | 62.59 | 63.52 | 70.99 | 67.63 |
| diabetes (RMSE) | block@0.5 | 64.54 | **63.19** | 64.01 | 69.72 | 66.10 |
| credit-g (AUC) | complete@0.0 | 0.828 | 0.828 | **0.831** | 0.801 | 0.807 |
| credit-g (AUC) | mcar@0.5 | 0.696 | 0.701 | **0.708** | 0.674 | 0.664 |
| credit-g (AUC) | mar@0.5 | 0.725 | 0.724 | 0.726 | 0.679 | 0.664 |
| credit-g (AUC) | mnar@0.5 | **0.760** | 0.759 | — | 0.728 | 0.707 |
| credit-g (AUC) | block@0.5 | **0.729** | 0.729 | 0.724 | 0.691 | 0.692 |
| adult (AUC) | complete@0.0 | 0.912 | 0.912 | **0.912** | 0.897 | 0.896 |
| adult (AUC) | mcar@0.5 | **0.858** | 0.857 | 0.857 | 0.841 | 0.836 |
| adult (AUC) | mar@0.5 | 0.850 | 0.849 | **0.851** | 0.837 | 0.839 |
| adult (AUC) | mnar@0.5 | **0.859** | 0.859 | — | 0.838 | 0.839 |
| adult (AUC) | block@0.5 | 0.866 | 0.865 | **0.871** | 0.849 | 0.855 |
| boston (RMSE) | complete@0.0 | 3.01 | 3.02 | 3.06 | 3.34 | **2.99** |
| boston (RMSE) | mcar@0.5 | 5.90 | 5.68 | **5.52** | 6.04 | 6.17 |
| boston (RMSE) | mar@0.5 | 4.97 | **4.89** | 4.91 | 5.71 | 5.39 |
| boston (RMSE) | mnar@0.5 | 5.08 | **4.98** | 5.30 | 5.09 | 5.16 |
| boston (RMSE) | block@0.5 | 5.08 | 4.80 | 5.04 | 4.89 | **4.67** |

### `tabicl_m_sa` vs `tabicl_impute`, paired over all mechanisms and rates

| dataset | metric | wins / losses | mean gain (AUC up / RMSE down) |
|---|---|---|---|
| breast_cancer | AUC | 18 / 16 | +0.0006 |
| wine | AUC | 17 / 7 | +0.0010 |
| diabetes | RMSE | 24 / 12 | +0.2734 |
| credit-g | AUC | 21 / 10 | +0.0026 |
| adult | AUC | 17 / 14 | +0.0001 |
| boston | RMSE | 26 / 7 | +0.1405 |
