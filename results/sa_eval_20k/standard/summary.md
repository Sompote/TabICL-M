# Missingness ablation

## breast_cancer (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 0.995 ± 0.004 | 0.996 ± 0.004 |
| block | 0.30 | 0.996 ± 0.003 | 0.996 ± 0.003 |
| block | 0.50 | 0.994 ± 0.005 | 0.994 ± 0.005 |
| mar | 0.10 | 0.995 ± 0.003 | 0.995 ± 0.004 |
| mar | 0.30 | 0.994 ± 0.004 | 0.994 ± 0.005 |
| mar | 0.50 | 0.991 ± 0.006 | 0.990 ± 0.006 |
| mcar | 0.10 | 0.995 ± 0.005 | 0.993 ± 0.005 |
| mcar | 0.30 | 0.996 ± 0.003 | 0.994 ± 0.005 |
| mcar | 0.50 | 0.991 ± 0.006 | 0.989 ± 0.008 |
| mnar | 0.10 | 0.995 ± 0.003 | 0.995 ± 0.004 |
| mnar | 0.30 | 0.994 ± 0.005 | 0.994 ± 0.005 |
| mnar | 0.50 | 0.993 ± 0.005 | 0.990 ± 0.006 |
| none | 0.00 | 0.996 ± 0.003 | 0.996 ± 0.003 |

## diabetes (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 58.610 ± 2.276 | 58.989 ± 2.427 |
| block | 0.30 | 59.099 ± 0.505 | 59.132 ± 0.339 |
| block | 0.50 | 64.010 ± 2.296 | 64.543 ± 2.868 |
| mar | 0.10 | 58.069 ± 0.843 | 58.649 ± 1.062 |
| mar | 0.30 | 62.139 ± 0.585 | 63.039 ± 0.466 |
| mar | 0.50 | 61.815 ± 0.913 | 61.471 ± 1.962 |
| mcar | 0.10 | 57.829 ± 1.262 | 57.946 ± 1.535 |
| mcar | 0.30 | 61.506 ± 2.257 | 61.835 ± 2.586 |
| mcar | 0.50 | 64.088 ± 2.639 | 65.600 ± 2.519 |
| mnar | 0.10 | 59.167 ± 0.814 | 59.411 ± 0.720 |
| mnar | 0.30 | 60.322 ± 3.470 | 60.398 ± 0.971 |
| mnar | 0.50 | 63.238 ± 2.952 | 62.692 ± 2.811 |
| none | 0.00 | 56.843 ± 0.713 | 56.570 ± 0.936 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 0.76 | 0.78 |
| block | 0.30 | 0.77 | 0.79 |
| block | 0.50 | 0.74 | 0.76 |
| mar | 0.10 | 0.76 | 0.78 |
| mar | 0.30 | 0.77 | 0.75 |
| mar | 0.50 | 0.77 | 0.81 |
| mcar | 0.10 | 0.77 | 0.78 |
| mcar | 0.30 | 0.78 | 0.79 |
| mcar | 0.50 | 0.78 | 0.80 |
| mnar | 0.10 | 0.77 | 0.79 |
| mnar | 0.30 | 0.78 | 0.78 |
| mnar | 0.50 | 0.80 | 0.79 |
| none | 0.00 | 0.75 | 0.76 |

## openml:1590 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 0.907 ± 0.010 | 0.906 ± 0.012 |
| block | 0.30 | 0.908 ± 0.006 | 0.907 ± 0.006 |
| block | 0.50 | 0.870 ± 0.010 | 0.866 ± 0.011 |
| mar | 0.10 | 0.904 ± 0.006 | 0.905 ± 0.010 |
| mar | 0.30 | 0.874 ± 0.004 | 0.877 ± 0.003 |
| mar | 0.50 | 0.851 ± 0.014 | 0.850 ± 0.013 |
| mcar | 0.10 | 0.908 ± 0.003 | 0.906 ± 0.006 |
| mcar | 0.30 | 0.883 ± 0.007 | 0.883 ± 0.007 |
| mcar | 0.50 | 0.856 ± 0.013 | 0.858 ± 0.016 |
| mnar | 0.10 | 0.896 ± 0.014 | 0.900 ± 0.016 |
| mnar | 0.30 | 0.895 | 0.896 ± 0.007 |
| mnar | 0.50 |  | 0.859 ± 0.034 |
| none | 0.00 | 0.912 ± 0.004 | 0.912 ± 0.005 |

## openml:31 (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 0.807 ± 0.012 | 0.804 ± 0.014 |
| block | 0.30 | 0.812 ± 0.014 | 0.804 ± 0.016 |
| block | 0.50 | 0.724 ± 0.036 | 0.729 ± 0.033 |
| mar | 0.10 | 0.814 ± 0.010 | 0.811 ± 0.012 |
| mar | 0.30 | 0.771 ± 0.017 | 0.768 ± 0.015 |
| mar | 0.50 | 0.722 ± 0.059 | 0.725 ± 0.035 |
| mcar | 0.10 | 0.801 ± 0.003 | 0.797 ± 0.003 |
| mcar | 0.30 | 0.758 ± 0.008 | 0.753 ± 0.001 |
| mcar | 0.50 | 0.708 ± 0.007 | 0.696 ± 0.010 |
| mnar | 0.10 | 0.811 ± 0.008 | 0.807 ± 0.018 |
| mnar | 0.30 | 0.739 | 0.770 ± 0.015 |
| mnar | 0.50 |  | 0.760 ± 0.008 |
| none | 0.00 | 0.831 ± 0.007 | 0.828 ± 0.007 |

## openml:531 (regression), rmse mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 3.234 ± 0.266 | 3.225 ± 0.297 |
| block | 0.30 | 3.791 ± 0.530 | 3.876 ± 0.567 |
| block | 0.50 | 5.036 ± 0.747 | 5.082 ± 0.601 |
| mar | 0.10 | 3.419 ± 0.287 | 3.442 ± 0.505 |
| mar | 0.30 | 4.339 ± 0.592 | 4.425 ± 0.599 |
| mar | 0.50 | 4.942 ± 0.430 | 4.971 ± 0.462 |
| mcar | 0.10 | 3.326 ± 0.138 | 3.652 ± 0.274 |
| mcar | 0.30 | 4.407 ± 0.148 | 4.739 ± 0.260 |
| mcar | 0.50 | 5.486 ± 0.328 | 5.904 ± 0.176 |
| mnar | 0.10 | 3.781 ± 0.455 | 3.935 ± 0.413 |
| mnar | 0.30 | 3.612 ± 0.361 | 3.810 ± 0.159 |
| mnar | 0.50 | 5.314 | 5.080 ± 0.640 |
| none | 0.00 | 2.999 ± 0.296 | 3.011 ± 0.346 |

Coverage of the 80 % interval (target 0.80):

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 0.77 | 0.80 |
| block | 0.30 | 0.79 | 0.80 |
| block | 0.50 | 0.74 | 0.76 |
| mar | 0.10 | 0.78 | 0.82 |
| mar | 0.30 | 0.81 | 0.81 |
| mar | 0.50 | 0.79 | 0.79 |
| mcar | 0.10 | 0.80 | 0.83 |
| mcar | 0.30 | 0.84 | 0.82 |
| mcar | 0.50 | 0.80 | 0.80 |
| mnar | 0.10 | 0.80 | 0.84 |
| mnar | 0.30 | 0.82 | 0.78 |
| mnar | 0.50 | 0.83 | 0.80 |
| none | 0.00 | 0.78 | 0.80 |

## wine (classification), auc mean ± std over seeds

| mechanism | rate | tabicl_aware | tabicl_impute |
|---|---|---|---|
| block | 0.10 | 1.000 ± 0.000 | 1.000 ± 0.001 |
| block | 0.30 | 1.000 ± 0.000 | 0.999 ± 0.001 |
| block | 0.50 | 0.995 ± 0.005 | 0.994 ± 0.007 |
| mar | 0.10 | 0.999 ± 0.001 | 1.000 ± 0.000 |
| mar | 0.30 | 0.998 ± 0.002 | 0.996 ± 0.002 |
| mar | 0.50 | 0.987 ± 0.013 | 0.985 ± 0.012 |
| mcar | 0.10 | 0.999 ± 0.001 | 0.999 ± 0.003 |
| mcar | 0.30 | 0.997 ± 0.005 | 0.995 ± 0.007 |
| mcar | 0.50 | 0.986 ± 0.004 | 0.980 ± 0.004 |
| mnar | 0.10 | 0.997 ± 0.005 | 0.997 ± 0.005 |
| mnar | 0.30 | 0.997 ± 0.003 | 0.999 ± 0.001 |
| mnar | 0.50 | 0.992 ± 0.006 | 0.993 ± 0.008 |
| none | 0.00 | 1.000 ± 0.000 | 1.000 ± 0.000 |

## Failed fits

- openml:31 / mnar / 0.3 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:31 / mnar / 0.5 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:31 / mnar / 0.5 / seed 1 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:31 / mnar / 0.3 / seed 2 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:31 / mnar / 0.5 / seed 2 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:1590 / mnar / 0.5 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:1590 / mnar / 0.3 / seed 1 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:1590 / mnar / 0.5 / seed 1 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:1590 / mnar / 0.3 / seed 2 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:1590 / mnar / 0.5 / seed 2 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:531 / mnar / 0.3 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:531 / mnar / 0.5 / seed 0 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.
- openml:531 / mnar / 0.5 / seed 1 / tabicl_aware: BracketError: The algorithm terminated without finding a valid bracket. Consider trying different initial points.