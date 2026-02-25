"""
Пользовательские функции для вычисления метрик качества классификации.
Модуль разработан в рамках Лабораторной работы №2 и используется в Лабораторной работе №3.
"""

import numpy as np


def custom_confusion_matrix(y_true, y_pred):
    """
    Вычисляет матрицу ошибок (confusion matrix).
    
    Parameters
    ----------
    y_true : array-like
        Истинные метки классов.
    y_pred : array-like
        Предсказанные метки классов.
    
    Returns
    -------
    cm : np.ndarray
        Матрица ошибок размером (n_classes, n_classes).
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    classes = np.unique(np.concatenate([y_true, y_pred]))
    n = len(classes)
    class_to_idx = {c: i for i, c in enumerate(classes)}
    cm = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[class_to_idx[t]][class_to_idx[p]] += 1
    return cm


def custom_accuracy(y_true, y_pred):
    """
    Вычисляет долю верно классифицированных объектов (Accuracy).
    
    Accuracy = (TP + TN) / (TP + TN + FP + FN)
    
    Parameters
    ----------
    y_true : array-like
        Истинные метки классов.
    y_pred : array-like
        Предсказанные метки классов.
    
    Returns
    -------
    float
        Значение Accuracy в диапазоне [0, 1].
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.sum(y_true == y_pred) / len(y_true)


def custom_precision(y_true, y_pred, average='macro'):
    """
    Вычисляет точность (Precision) для задачи классификации.
    
    Precision = TP / (TP + FP)
    
    Parameters
    ----------
    y_true : array-like
        Истинные метки классов.
    y_pred : array-like
        Предсказанные метки классов.
    average : str
        Метод усреднения: 'macro' или 'weighted'.
    
    Returns
    -------
    float
        Значение Precision.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    classes = np.unique(y_true)
    precisions = []
    supports = []
    for cls in classes:
        tp = np.sum((y_pred == cls) & (y_true == cls))
        fp = np.sum((y_pred == cls) & (y_true != cls))
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        precisions.append(prec)
        supports.append(np.sum(y_true == cls))
    if average == 'weighted':
        return np.average(precisions, weights=supports)
    return np.mean(precisions)


def custom_recall(y_true, y_pred, average='macro'):
    """
    Вычисляет полноту (Recall) для задачи классификации.
    
    Recall = TP / (TP + FN)
    
    Parameters
    ----------
    y_true : array-like
        Истинные метки классов.
    y_pred : array-like
        Предсказанные метки классов.
    average : str
        Метод усреднения: 'macro' или 'weighted'.
    
    Returns
    -------
    float
        Значение Recall.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    classes = np.unique(y_true)
    recalls = []
    supports = []
    for cls in classes:
        tp = np.sum((y_pred == cls) & (y_true == cls))
        fn = np.sum((y_pred != cls) & (y_true == cls))
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        recalls.append(rec)
        supports.append(np.sum(y_true == cls))
    if average == 'weighted':
        return np.average(recalls, weights=supports)
    return np.mean(recalls)


def custom_f1(y_true, y_pred, average='macro'):
    """
    Вычисляет F1-меру для задачи классификации.
    
    F1 = 2 * Precision * Recall / (Precision + Recall)
    
    Parameters
    ----------
    y_true : array-like
        Истинные метки классов.
    y_pred : array-like
        Предсказанные метки классов.
    average : str
        Метод усреднения: 'macro' или 'weighted'.
    
    Returns
    -------
    float
        Значение F1-меры.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    classes = np.unique(y_true)
    f1_scores = []
    supports = []
    for cls in classes:
        tp = np.sum((y_pred == cls) & (y_true == cls))
        fp = np.sum((y_pred == cls) & (y_true != cls))
        fn = np.sum((y_pred != cls) & (y_true == cls))
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        f1_scores.append(f1)
        supports.append(np.sum(y_true == cls))
    if average == 'weighted':
        return np.average(f1_scores, weights=supports)
    return np.mean(f1_scores)
