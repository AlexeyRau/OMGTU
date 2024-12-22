import numpy as np
from scipy.linalg import lu
from scipy.stats import chisquare

# 1. Взять свою матрицу из 1.10
# Для примера возьмем матрицу 3x3
A = np.load('matrix_A.npy')
print("Исходная матрица A:")
print(A)

# 2. Получить LU-разложение (LUP-разложение)


P, L, U = lu(A)
print("\nL:")
print(L)
print("\nU:")
print(U)
print("\nP:")
print(P)

# 3. Найти определитель
det_A = np.linalg.det(P) * np.prod(np.diag(L)) * np.prod(np.diag(U))
print("\nОпределитель матрицы:", det_A)

# 4. Сгенерировать две выборки (вектор целых чисел из 100 элементов)
np.random.seed(0)  # Для воспроизводимости
uniform_sample = np.random.randint(0, 100, size=100)  # Равномерное распределение
normal_sample = np.random.normal(loc=50, scale=15, size=100).astype(int)  # Нормальное распределение

print("\nВыборка с равномерным распределением:")
print(uniform_sample)
print("\nВыборка с нормальным распределением:")
print(normal_sample)

# 5. Вычислить статистики для каждой выборки
def calculate_statistics(sample):
    return {
        "Среднее": np.mean(sample),
        "Мода": float(np.argmax(np.bincount(sample))),  # Мода
        "Медиана": np.median(sample),
        "Минимум": np.min(sample),
        "Максимум": np.max(sample),
        "Стандартное отклонение": np.std(sample)
    }

uniform_stats = calculate_statistics(uniform_sample)
normal_stats = calculate_statistics(normal_sample)

print("\nСтатистики для равномерной выборки:")
for key, value in uniform_stats.items():
    print(f"{key}: {value}")

print("\nСтатистики для нормальной выборки:")
for key, value in normal_stats.items():
    print(f"{key}: {value}")

# Шаг 6: Вычисляем p-value для нулевой гипотезы "Распределение выборки не равномерное"
# Используем критерий хи-квадрат
uniform_counts = np.bincount(uniform_sample)
normal_counts = np.bincount(normal_sample)

chi2_uniform, p_uniform = chisquare(uniform_counts)
chi2_normal, p_normal = chisquare(normal_counts)

print("\nРезультаты теста хи-квадрат для равномерной выборки:")
print(f"Хи-квадрат статистика: {chi2_uniform}, p-value: {p_uniform}")

print("\nРезультаты теста хи-квадрат для нормальной выборки:")
print(f"Хи-квадрат статистика: {chi2_normal}, p-value: {p_normal}")
