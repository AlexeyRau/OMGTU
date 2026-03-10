import numpy as np

class CustomKMeans:
    """
    Собственная реализация алгоритма K-Means с подсчётом суммы квадратов
    расстояний между точками и соответствующими центроидами (инерция).
    """

    def __init__(self, n_clusters=3, max_iter=300, tol=1e-4, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids_ = None
        self.labels_ = None
        self.inertia_ = None

    def _init_centroids(self, X):
        rng = np.random.RandomState(self.random_state)
        indices = rng.choice(len(X), self.n_clusters, replace=False)
        return X[indices].copy()

    def _assign_labels(self, X, centroids):
        # Евклидово расстояние до каждого центроида
        dists = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)  # (n, k)
        return np.argmin(dists, axis=1)

    def _update_centroids(self, X, labels):
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            mask = labels == k
            if mask.sum() > 0:
                centroids[k] = X[mask].mean(axis=0)
        return centroids

    def _compute_inertia(self, X, labels, centroids):
        total = 0.0
        for k in range(self.n_clusters):
            mask = labels == k
            if mask.sum() > 0:
                diff = X[mask] - centroids[k]
                total += (diff ** 2).sum()
        return total

    def fit(self, X):
        X = np.array(X, dtype=float)
        centroids = self._init_centroids(X)

        for _ in range(self.max_iter):
            labels = self._assign_labels(X, centroids)
            new_centroids = self._update_centroids(X, labels)
            shift = np.linalg.norm(new_centroids - centroids)
            centroids = new_centroids
            if shift < self.tol:
                break

        self.centroids_ = centroids
        self.labels_ = labels
        self.inertia_ = self._compute_inertia(X, labels, centroids)
        return self

    def predict(self, X):
        X = np.array(X, dtype=float)
        return self._assign_labels(X, self.centroids_)

    def fit_predict(self, X):
        return self.fit(X).labels_
