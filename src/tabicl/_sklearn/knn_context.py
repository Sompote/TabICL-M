"""Neighbour-based context for large regression tables.

An in-context learner reads the whole training table as its context. On large
tables with a smooth target that is wasteful: the rows that matter for a test
row are the ones near it in feature space, and a context made of those rows
lets the model resolve fine structure it cannot resolve from a random sample
of the same size (the idea behind LoCalPFN and TabDPT).

:class:`KNNContextRegressor` wraps :class:`~tabicl.TabICLRegressor`. Below
``min_rows`` training rows it behaves exactly like the wrapped estimator. Above,
``predict`` clusters the test rows into groups of about ``test_group_size``,
builds for every group a context of the ``context_size`` training rows nearest
to its members (nearest in a standardised, imputed, ordinal-encoded feature
space) and fits the wrapped estimator on that context. Missing cells are fine:
they are imputed only for the distance computation; the model still sees NaN.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.utils.validation import check_is_fitted

from .regressor import TabICLRegressor


def _to_frame(X) -> pd.DataFrame:
    if isinstance(X, pd.DataFrame):
        return X.reset_index(drop=True)
    return pd.DataFrame(np.asarray(X))


class _DistanceEncoder:
    """Ordinal-encode non-numeric columns, impute NaN with the training mean, standardise."""

    def fit(self, X: pd.DataFrame) -> "_DistanceEncoder":
        self.columns_ = list(X.columns)
        self.categories_: Dict[Any, Dict[Any, int]] = {}
        Z = np.zeros((len(X), len(self.columns_)), dtype=np.float64)
        for j, c in enumerate(self.columns_):
            col = X[c]
            if not pd.api.types.is_numeric_dtype(col):
                cats = {v: i for i, v in enumerate(pd.unique(col.dropna()))}
                self.categories_[c] = cats
                Z[:, j] = col.map(cats).astype(float).to_numpy()
            else:
                Z[:, j] = col.to_numpy(dtype=np.float64)
        self.mean_ = np.nanmean(Z, axis=0)
        self.mean_ = np.where(np.isfinite(self.mean_), self.mean_, 0.0)
        Z = np.where(np.isnan(Z), self.mean_, Z)
        self.std_ = Z.std(axis=0)
        self.std_ = np.where(self.std_ > 1e-12, self.std_, 1.0)
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        Z = np.zeros((len(X), len(self.columns_)), dtype=np.float64)
        for j, c in enumerate(self.columns_):
            col = X[c]
            if c in self.categories_:
                Z[:, j] = col.map(self.categories_[c]).astype(float).to_numpy()
            else:
                Z[:, j] = pd.to_numeric(col, errors="coerce").to_numpy(dtype=np.float64)
        Z = np.where(np.isnan(Z), self.mean_, Z)
        return (Z - self.mean_) / self.std_


class KNNContextRegressor(BaseEstimator, RegressorMixin):
    """TabICL regressor with a nearest-neighbour context on large tables.

    Parameters
    ----------
    base_kwargs : dict, optional
        Keyword arguments of :class:`~tabicl.TabICLRegressor` (``model_path``,
        ``n_estimators``, ``device``, ``random_state``, ...).
    context_size : int, default=2000
        Number of training rows in the context of every test group.
    min_rows : int, default=2500
        Training sizes at or below this use the plain estimator on the whole table.
    test_group_size : int, default=256
        Target number of test rows per group (test rows are clustered with k-means).
    random_state : int, default=0
        Seed of the clustering.
    verbose : bool, default=False
    """

    def __init__(
        self,
        base_kwargs: Optional[Dict[str, Any]] = None,
        context_size: int = 2000,
        min_rows: int = 2500,
        test_group_size: int = 256,
        random_state: int = 0,
        verbose: bool = False,
    ):
        self.base_kwargs = base_kwargs
        self.context_size = context_size
        self.min_rows = min_rows
        self.test_group_size = test_group_size
        self.random_state = random_state
        self.verbose = verbose

    def _make_base(self) -> TabICLRegressor:
        return TabICLRegressor(**(self.base_kwargs or {}))

    def fit(self, X, y) -> "KNNContextRegressor":
        self.X_train_ = _to_frame(X)
        self.y_train_ = np.asarray(y, dtype=np.float64).ravel()
        self.n_features_in_ = self.X_train_.shape[1]
        self.local_ = len(self.y_train_) > self.min_rows
        if self.local_:
            self.encoder_ = _DistanceEncoder().fit(self.X_train_)
            self.Z_train_ = self.encoder_.transform(self.X_train_)
            self.nn_ = NearestNeighbors(n_neighbors=1).fit(self.Z_train_)
            self.base_ = None
        else:
            self.base_ = self._make_base().fit(self.X_train_, self.y_train_)
        return self

    def _context_for(self, Z_group: np.ndarray) -> np.ndarray:
        """Indices of the ``context_size`` training rows nearest to a group of test rows."""
        n_train = len(self.y_train_)
        size = min(self.context_size, n_train)
        k = min(n_train, max(1, math.ceil(2.0 * size / len(Z_group))))
        dist, idx = self.nn_.kneighbors(Z_group, n_neighbors=k)
        # nearest distance of every candidate row to the group
        cand = np.unique(idx.ravel())
        best = np.full(n_train, np.inf)
        np.minimum.at(best, idx.ravel(), dist.ravel())
        if len(cand) > size:
            cand = cand[np.argsort(best[cand])[:size]]
        elif len(cand) < size:
            centroid = Z_group.mean(axis=0, keepdims=True)
            _, more = self.nn_.kneighbors(centroid, n_neighbors=min(n_train, size + len(cand)))
            more = more.ravel()
            more = more[~np.isin(more, cand)][: size - len(cand)]
            cand = np.concatenate([cand, more])
        return np.sort(cand)

    def predict(self, X, output_type="mean", alphas: Optional[list] = None):
        check_is_fitted(self, "local_")
        X = _to_frame(X)
        kw = {"output_type": output_type}
        if alphas is not None:
            kw["alphas"] = alphas
        if not self.local_:
            return self.base_.predict(X, **kw)
        Z_test = self.encoder_.transform(X)
        n_groups = max(1, math.ceil(len(X) / self.test_group_size))
        if n_groups == 1:
            labels = np.zeros(len(X), dtype=int)
        else:
            labels = KMeans(n_clusters=n_groups, n_init=1, random_state=self.random_state).fit_predict(Z_test)
        out = None
        base = self._make_base()
        for g in np.unique(labels):
            members = np.flatnonzero(labels == g)
            ctx = self._context_for(Z_test[members])
            base.fit(self.X_train_.iloc[ctx], self.y_train_[ctx])
            pred = base.predict(X.iloc[members], **kw)
            if isinstance(pred, dict):
                if out is None:
                    out = {k: np.empty((len(X),) + np.asarray(v).shape[1:], dtype=np.float64) for k, v in pred.items()}
                for k, v in pred.items():
                    out[k][members] = v
            else:
                if out is None:
                    out = np.empty((len(X),) + np.asarray(pred).shape[1:], dtype=np.float64)
                out[members] = pred
            if self.verbose:
                print(f"[knn-context] group {g}: {len(members)} test rows, {len(ctx)} context rows")
        return out
