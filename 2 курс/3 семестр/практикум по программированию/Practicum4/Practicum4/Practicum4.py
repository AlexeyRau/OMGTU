import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Пункт 1: Вычисление значений функции на отрезке
def f(x):
    return 2 / (np.sin(x) + 4)

a = 3
b = 6
n = 100  # Количество точек разбиения
x = np.linspace(a, b, n)
y = f(x)
print("Значения функции на отрезке [3, 6]:")
print(y)

# Пункт 2: Построение графика функции
plt.figure(figsize=(8, 6))
plt.plot(x, y, label="y = 2 / (sin(x) + 4)")
plt.title("График функции", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("y", fontsize=14)
plt.legend(fontsize=12)
plt.show()

# Пункт 3: Точечный график функции
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color=(0.8, 0.2, 0.5), marker='.', label="y = 2 / (sin(x) + 4)")
plt.title("Точечный график функции", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("y", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

# Шаг 4: Построение гистограмм для равномерного и нормального распределений
np.random.seed(0)  # Для воспроизводимости
uniform_sample = np.random.randint(0, 100, size=100)  # Равномерное распределение
normal_sample = np.random.normal(loc=50, scale=15, size=100).astype(int)  # Нормальное распределение

print("\nВыборка с равномерным распределением:")
print(uniform_sample)
print("\nВыборка с нормальным распределением:")
print(normal_sample)

# Построение гистограмм
plt.figure(figsize=(12, 6))

# Гистограмма для равномерного распределения
plt.subplot(1, 2, 1)
plt.hist(uniform_sample, bins=15, color='blue')
plt.title("Равномерное распределение", fontsize=14)
plt.xlabel("Значения", fontsize=12)
plt.ylabel("Частота", fontsize=12)

# Гистограмма для нормального распределения
plt.subplot(1, 2, 2)
plt.hist(normal_sample, bins=50, color='red')
plt.title("Нормальное распределение", fontsize=14)
plt.xlabel("Значения", fontsize=12)
plt.ylabel("Частота", fontsize=12)

plt.tight_layout()
plt.show()

# 5. Генерация выборки из равномерного распределения
np.random.seed(0)  # Для воспроизводимости
uniform_sample = np.random.randint(1, 5, size=50)  # Выборка из целых чисел от 1 до 4

# Подсчет количества вхождений каждого числа
unique_values, counts = np.unique(uniform_sample, return_counts=True)

print("Выборка из равномерного распределения:")
print(uniform_sample)

# Построение круговой диаграммы
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.pie(counts, labels=unique_values, autopct='%1.1f%%', colors=['blue', 'green', 'orange', 'red'])
plt.title("Круговая диаграмма", fontsize=14)

# Построение столбчатой диаграммы
plt.subplot(1, 2, 2)
plt.bar(unique_values, counts, color=['blue', 'green', 'orange', 'red'])
plt.title("Столбчатая диаграмма", fontsize=14)
plt.xlabel("Числа", fontsize=12)
plt.ylabel("Количество повторений", fontsize=12)
plt.xticks(unique_values)

plt.tight_layout()
plt.show()

# 6. Трёхмерный график
# Определение функции
def f(x1, x2):
    return (x1 - 4)**2 + (x2 - 2)**2

# Разбиение отрезков для x1 и x2
x1 = np.linspace(0, 8, 100)  # Отрезок для x1
x2 = np.linspace(0, 4, 100)  # Отрезок для x2
X1, X2 = np.meshgrid(x1, x2)  # Создание сетки
Z = f(X1, X2)  # Вычисление значений функции

# Построение трехмерного графика
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Построение поверхности
ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)

# Установка параметров графика
ax.set_title("Трехмерный график функции (x1 - 4)^2 + (x2 - 2)^2", fontsize=14)
ax.set_xlabel("x1", fontsize=12)
ax.set_ylabel("x2", fontsize=12)
ax.set_zlabel("f(x1, x2)", fontsize=12)

plt.show()

# 7. Подграфики
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# Левая верхняя часть: График функции из пункта 2
axs[0, 0].plot(x, y, label="y = 2 / (sin(x) + 4)")
axs[0, 0].set_title("График функции", fontsize=14)
axs[0, 0].set_xlabel("x", fontsize=12)
axs[0, 0].set_ylabel("y", fontsize=12)
axs[0, 0].legend(fontsize=10)

# Правая верхняя часть: Точечный график из пункта 3
axs[0, 1].scatter(x, y, color=(0.8, 0.2, 0.5), marker='.', label="y = 2 / (sin(x) + 4)")
axs[0, 1].set_title("Точечный график функции", fontsize=14)
axs[0, 1].set_xlabel("x", fontsize=12)
axs[0, 1].set_ylabel("y", fontsize=12)
axs[0, 1].legend(fontsize=10)
axs[0, 1].grid(True)

# Левая нижняя часть: Круговая диаграмма из пункта 5
axs[1, 0].pie(counts, labels=unique_values, autopct='%1.1f%%', colors=['blue', 'green', 'orange', 'red'])
axs[1, 0].set_title("Круговая диаграмма", fontsize=14)

# Правая нижняя часть: Трехмерный график из пункта 6
ax = fig.add_subplot(2, 2, 4, projection='3d')
ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
ax.set_title("Трехмерный график функции", fontsize=14)
ax.set_xlabel("x1", fontsize=12)
ax.set_ylabel("x2", fontsize=12)
ax.set_zlabel("f(x1, x2)", fontsize=12)

# Установка общего заголовка для сетки
fig.suptitle("Сетка из 4 графиков", fontsize=18)

# Установка цвета фона для любого графика (например, для левого верхнего)
axs[0, 0].set_facecolor('lightgray')

plt.tight_layout()
plt.show()

# 8. Использование различных стилей оформления графиков

# Проверка доступных стилей
print("Доступные стили:", plt.style.available)

# Список стилей для проверки
styles = ['ggplot', 'dark_background', 'classic']  # Выберите доступные стили

# Функция для отображения сетки графиков с заданным стилем
def plot_with_style(style):
    plt.style.use(style)
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))

    # Левая верхняя часть: График функции из пункта 2
    axs[0, 0].plot(x, y, label="y = 2 / (sin(x) + 4)")
    axs[0, 0].set_title("График функции", fontsize=14)
    axs[0, 0].set_xlabel("x", fontsize=12)
    axs[0, 0].set_ylabel("y", fontsize=12)
    axs[0, 0].legend(fontsize=10)

    # Правая верхняя часть: Точечный график из пункта 3
    axs[0, 1].scatter(x, y, color=(0.8, 0.2, 0.5), marker='.', label="y = 2 / (sin(x) + 4)")
    axs[0, 1].set_title("Точечный график функции", fontsize=14)
    axs[0, 1].set_xlabel("x", fontsize=12)
    axs[0, 1].set_ylabel("y", fontsize=12)
    axs[0, 1].legend(fontsize=10)
    axs[0, 1].grid(True)

    # Левая нижняя часть: Круговая диаграмма из пункта 5
    axs[1, 0].pie(counts, labels=unique_values, autopct='%1.1f%%', colors=['blue', 'green', 'orange', 'red'])
    axs[1, 0].set_title("Круговая диаграмма", fontsize=14)

    # Правая нижняя часть: Трехмерный график из пункта 6
    ax = fig.add_subplot(2, 2, 4, projection='3d')
    ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
    ax.set_title("Трехмерный график функции", fontsize=14)
    ax.set_xlabel("x1", fontsize=12)
    ax.set_ylabel("x2", fontsize=12)
    ax.set_zlabel("f(x1, x2)", fontsize=12)

    # Установка общего заголовка для сетки
    fig.suptitle(f"Сетка из 4 графиков (Стиль: {style})", fontsize=18)

    # Установка цвета фона для любого графика (например, для левого верхнего)
    axs[0, 0].set_facecolor('lightgray')

    plt.tight_layout()
    plt.show()

# Применение каждого стиля
for style in styles:
    plot_with_style(style)