import matplotlib.pyplot as plt
import numpy as np

# Данные
x_i = [20, 30, 40, 50]
y_bar_i = [3.8, 8/3, 221/35, 87/11]  # Групповые средние

# Регрессия Y на X
x_range = np.linspace(15, 55, 100)
y_yx = 0.026 + 0.154 * x_range  # y = 1.576 + 0.1536x

# Регрессия X на Y
y_range = np.linspace(1, 10, 100)
x_xy = 19.493 + 3.032 * y_range  # x = 22.53 + 3.032y

# Построение
plt.figure(figsize=(12, 8))

# Точки групповых средних
plt.scatter(x_i, y_bar_i, s=100, c='red', label='Групповые средние $(x_i, \overline{y}_i)$')

# Регрессия Y на X
plt.plot(x_range, y_yx, 'b-', lw=2, label='Регрессия $Y$ на $X$: $y = 0,154x + 0,026$')

# Регрессия X на Y
plt.plot(x_xy, y_range, 'g--', lw=2, label='Регрессия $X$ на $Y$: $x = 3,032y + 19,493$')

# Общее среднее
mean_x = 36.6
mean_y = 5.6
plt.scatter(mean_x, mean_y, s=150, marker='*', c='purple', label=f'Общее среднее $({mean_x:.1f}, {mean_y:.1f})$')

# Настройки
plt.title('Линии регрессии', fontsize=16)
plt.xlabel('$X$', fontsize=14)
plt.ylabel('$Y$', fontsize=14)
plt.grid(True, ls='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(np.arange(15, 56, 5))
plt.yticks(np.arange(1, 11, 1))
plt.xlim(15, 55)
plt.ylim(1, 10)

plt.show()