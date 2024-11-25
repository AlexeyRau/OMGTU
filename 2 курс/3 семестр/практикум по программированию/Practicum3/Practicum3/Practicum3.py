import numpy as np
from scipy import stats
from scipy.linalg import lu

# 1. Взять свою матрицу из 1.10
# Для примера возьмем матрицу 3x3
A = np.array([[2.3, 0, -3.4, -12],
              [2.6, 8.4, 0, -6],
              [1.3, 4.5, -17, 2],
              [1.8, 0, 15, 16]])
print("Исходная матрица A:")
print(A)

# 2. Получить LU-разложение (LUP-разложение)


P, L, U = lu(A)
print("\nL:")
print(L)
print("\nU:")
print(U)
print("\nP (перестановочная матрица):")
print(P)

# 3. Найти определитель
det = np.linalg.det(P) * np.prod(np.diag(L)) * np.prod(np.diag(U))
print("\nОпределитель матрицы:", det)

# 4. Сгенерировать две выборки (вектор целых чисел из 100 элементов)
np.random.seed(0)  # Для воспроизводимости
uniform_sample = np.random.randint(0, 100, size=100)  # Равномерное распределение
normal_sample = np.random.normal(loc=50, scale=15, size=100).astype(int)  # Нормальное распределение

print("\nВыборка с равномерным распределением:")
print(uniform_sample)
print("\nВыборка с нормальным распределением:")
print(normal_sample)

# 5. Вычислить для каждой из выборок
def compute_statistics(sample):
    mean = np.mean(sample)
    mode = stats.mode(sample).mode[0]
    median = np.median(sample)
    minimum = np.min(sample)
    maximum = np.max(sample)
    std_dev = np.std(sample)
    
    return mean, mode, median, minimum, maximum, std_dev

uniform_stats = compute_statistics(uniform_sample)
normal_stats = compute_statistics(normal_sample)

print("\nСтатистика для выборки с равномерным распределением:")
print(f"Среднее: {uniform_stats[0]}")
print(f"Мода: {uniform_stats[1]}")
print(f"Медиана: {uniform_stats[2]}")
print(f"Минимум: {uniform_stats[3]}")
print(f"Максимум: {uniform_stats[4]}")
print(f"Стандартное отклонение: {uniform_stats[5]}")

print("\nСтатистика для выборки с нормальным распределением:")
print(f"Среднее: {normal_stats[0]}")
print(f"Мода: {normal_stats[1]}")
print(f"Медиана: {normal_stats[2]}")
print(f"Минимум: {normal_stats[3]}")
print(f"Максимум: {normal_stats[4]}")
print(f"Стандартное отклонение: {normal_stats[5]}")

# 6. Вычислить значение p-value для нулевой гипотезы
# Для этого используем тест хи-квадрат
chi2_stat, p_value = stats.chisquare(uniform_sample)
print("\nЗначение p-value для нулевой гипотезы (равномерное распределение):", p_value)

