
"""
ml_algorithms.py — библиотека алгоритмов машинного обучения.
Содержит: MyKMeans — собственная реализация алгоритма k-means.
"""

import numpy as np


class MyKMeans:
    """
    Собственная реализация алгоритма кластеризации K-Means.
    Поддерживает подсчёт суммы квадратов расстояний (SSE / инерции).

    Параметры
    ---------
    n_clusters   : int   — число кластеров
    max_iter     : int   — максимальное число итераций
    tol          : float — порог сходимости (сдвиг центроидов)
    random_state : int   — фиксация случайности
    """

    def __init__(self, n_clusters=3, max_iter=300, tol=1e-4, random_state=None):
        self.n_clusters       = n_clusters
        self.max_iter         = max_iter
        self.tol              = tol
        self.random_state     = random_state
        self.centroids_       = None
        self.labels_          = None
        self.inertia_         = None
        self.n_iter_          = 0
        self.inertia_history_ = []

    def _init_centroids(self, X):
        rng = np.random.RandomState(self.random_state)
        idx = rng.choice(X.shape[0], size=self.n_clusters, replace=False)
        return X[idx].copy()

    def _assign_clusters(self, X, centroids):
        dists = np.linalg.norm(X[:, np.newaxis, :] - centroids[np.newaxis, :, :], axis=2)
        return np.argmin(dists, axis=1)

    def _compute_inertia(self, X, labels, centroids):
        sse = 0.0
        for k in range(self.n_clusters):
            mask = labels == k
            if mask.any():
                sse += np.sum((X[mask] - centroids[k]) ** 2)
        return sse

    def _update_centroids(self, X, labels):
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            mask = labels == k
            if mask.any():
                centroids[k] = X[mask].mean(axis=0)
            else:
                rng = np.random.RandomState(self.random_state)
                centroids[k] = X[rng.randint(0, X.shape[0])]
        return centroids

    def fit(self, X):
        X = np.array(X, dtype=float)
        centroids = self._init_centroids(X)
        labels    = np.zeros(X.shape[0], dtype=int)
        self.inertia_history_ = []
        for iteration in range(self.max_iter):
            new_labels    = self._assign_clusters(X, centroids)
            new_centroids = self._update_centroids(X, new_labels)
            inertia       = self._compute_inertia(X, new_labels, new_centroids)
            self.inertia_history_.append(inertia)
            shift     = np.linalg.norm(new_centroids - centroids)
            centroids = new_centroids
            labels    = new_labels
            if shift < self.tol:
                self.n_iter_ = iteration + 1
                break
        else:
            self.n_iter_ = self.max_iter
        self.centroids_ = centroids
        self.labels_    = labels
        self.inertia_   = self.inertia_history_[-1]
        return self

    def predict(self, X):
        X = np.array(X, dtype=float)
        return self._assign_clusters(X, self.centroids_)

    def fit_predict(self, X):
        return self.fit(X).labels_
