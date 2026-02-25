"""
Пользовательская реализация алгоритма kNN для задачи классификации.
Реализован в стиле Scikit-learn (методы fit / predict).
"""

import numpy as np
from collections import Counter


class CustomKNNClassifier:
    """
    Классификатор на основе алгоритма k ближайших соседей (kNN).
    
    Реализован в соответствии с интерфейсом Scikit-learn:
    методы fit() и predict() аналогичны sklearn.neighbors.KNeighborsClassifier.
    
    Parameters
    ----------
    n_neighbors : int, default=5
        Количество ближайших соседей k.
    metric : str, default='euclidean'
        Метрика расстояния: 'euclidean', 'manhattan', 'chebyshev', 'minkowski'.
    p : int, default=2
        Степень для метрики Минковского (используется при metric='minkowski').
    weights : str, default='uniform'
        Схема взвешивания: 'uniform' — все соседи равноправны,
        'distance' — вес обратно пропорционален расстоянию.
    """

    def __init__(self, n_neighbors=5, metric='euclidean', p=2, weights='uniform'):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.p = p
        self.weights = weights
        self.X_train_ = None
        self.y_train_ = None

    # ------------------------------------------------------------------
    # Вычисление расстояний
    # ------------------------------------------------------------------

    def _euclidean(self, a, b):
        """Евклидово расстояние: sqrt(sum((a - b)^2))."""
        return np.sqrt(np.sum((a - b) ** 2, axis=1))

    def _manhattan(self, a, b):
        """Манхэттенское расстояние: sum(|a - b|)."""
        return np.sum(np.abs(a - b), axis=1)

    def _chebyshev(self, a, b):
        """Расстояние Чебышёва: max(|a - b|)."""
        return np.max(np.abs(a - b), axis=1)

    def _minkowski(self, a, b, p):
        """Расстояние Минковского: (sum(|a - b|^p))^(1/p)."""
        return np.sum(np.abs(a - b) ** p, axis=1) ** (1 / p)

    def _compute_distances(self, X, x_query):
        """
        Вычисляет расстояния от x_query до всех точек в X.
        
        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)
        x_query : np.ndarray, shape (n_features,)
        
        Returns
        -------
        distances : np.ndarray, shape (n_samples,)
        """
        x_query = x_query.reshape(1, -1)
        diff = X - x_query  # broadcasting
        if self.metric == 'euclidean':
            return self._euclidean(X, x_query)
        elif self.metric == 'manhattan':
            return self._manhattan(X, x_query)
        elif self.metric == 'chebyshev':
            return self._chebyshev(X, x_query)
        elif self.metric == 'minkowski':
            return self._minkowski(X, x_query, self.p)
        else:
            raise ValueError(f"Неизвестная метрика: {self.metric}. "
                             "Допустимые значения: 'euclidean', 'manhattan', 'chebyshev', 'minkowski'.")

    # ------------------------------------------------------------------
    # Основные методы (sklearn-совместимый интерфейс)
    # ------------------------------------------------------------------

    def fit(self, X, y):
        """
        Обучение модели — сохранение обучающей выборки.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Матрица признаков обучающей выборки.
        y : array-like, shape (n_samples,)
            Вектор меток классов обучающей выборки.
        
        Returns
        -------
        self
        """
        self.X_train_ = np.array(X)
        self.y_train_ = np.array(y)
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        """
        Предсказание классов для новых объектов.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Матрица признаков тестовой выборки.
        
        Returns
        -------
        y_pred : np.ndarray, shape (n_samples,)
            Предсказанные метки классов.
        """
        X = np.array(X)
        return np.array([self._predict_single(x) for x in X])

    def _predict_single(self, x):
        """
        Предсказание класса для одного объекта.
        
        Алгоритм:
        1. Вычислить расстояния от x до всех точек обучающей выборки.
        2. Выбрать k ближайших соседей.
        3. Определить класс голосованием (или взвешенным голосованием).
        
        Parameters
        ----------
        x : np.ndarray, shape (n_features,)
        
        Returns
        -------
        predicted_class : scalar
        """
        distances = self._compute_distances(self.X_train_, x)
        k_nearest_idx = np.argsort(distances)[:self.n_neighbors]
        k_nearest_labels = self.y_train_[k_nearest_idx]
        k_nearest_distances = distances[k_nearest_idx]

        if self.weights == 'uniform':
            # Простое голосование: класс с наибольшим числом голосов
            return Counter(k_nearest_labels).most_common(1)[0][0]
        elif self.weights == 'distance':
            # Взвешенное голосование: вес = 1/расстояние
            weight_dict = {}
            for label, dist in zip(k_nearest_labels, k_nearest_distances):
                w = 1.0 / (dist + 1e-10)
                weight_dict[label] = weight_dict.get(label, 0) + w
            return max(weight_dict, key=weight_dict.get)
        else:
            raise ValueError("weights должен быть 'uniform' или 'distance'.")

    def score(self, X, y):
        """
        Вычисляет Accuracy на переданных данных.
        
        Parameters
        ----------
        X : array-like
        y : array-like
        
        Returns
        -------
        float : Accuracy.
        """
        y_pred = self.predict(X)
        return np.mean(np.array(y_pred) == np.array(y))

    def get_params(self, deep=True):
        """Возвращает гиперпараметры (для совместимости с GridSearchCV)."""
        return {
            'n_neighbors': self.n_neighbors,
            'metric': self.metric,
            'p': self.p,
            'weights': self.weights,
        }

    def set_params(self, **params):
        """Устанавливает гиперпараметры (для совместимости с GridSearchCV)."""
        for key, value in params.items():
            setattr(self, key, value)
        return self
