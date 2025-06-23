import numpy as np
import matplotlib.pyplot as plt
from math import log
import numpy as np
import matplotlib.pyplot as plt
from math import log
from mpl_toolkits.mplot3d import Axes3D

def plot_optimization_process(history, method_name, constraints):
    """Визуализация процесса оптимизации"""
    history = np.array(history)
    
    # График траектории оптимизации
    plt.figure(figsize=(12, 5))
    
    # 1. Траектория в пространстве переменных
    plt.subplot(1, 2, 1)
    plt.plot(history[:, 0], history[:, 1], 'bo-', label='Траектория')
    plt.scatter(history[0, 0], history[0, 1], c='r', label='Начальная точка')
    plt.scatter(history[-1, 0], history[-1, 1], c='g', label='Конечная точка')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title(f'{method_name}: Траектория оптимизации')
    plt.legend()
    plt.grid(True)
    
    # 2. Изменение значений ограничений
    plt.subplot(1, 2, 2)
    g_values = np.array([[g(x) for g in constraints] for x in history])
    for i in range(len(constraints)):
        plt.plot(g_values[:, i], label=f'g{i+1}(x)')
    plt.axhline(0, color='k', linestyle='--')
    plt.xlabel('Итерация')
    plt.ylabel('Значение ограничения')
    plt.title(f'{method_name}: Ограничения')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # 3. График изменения целевой функции
    plt.figure(figsize=(8, 5))
    f_values = [f(x) for x in history]
    plt.plot(f_values, 'r-', label='Целевая функция')
    plt.xlabel('Итерация')
    plt.ylabel('f(x)')
    plt.title(f'{method_name}: Изменение целевой функции')
    plt.legend()
    plt.grid(True)
    plt.show()

"""
Штрафы
"""
def penalty_method(f, grad_f, constraints, grad_constraints, x0, epsilon=0.05, alpha=0.001, max_iter=1000, max_k=1e6):
    x = np.array(x0, dtype=float)
    k = 1.0
    iter_count = 0
    history = [x.copy()]
    prev_P = float('inf')
    
    while iter_count < max_iter and k < max_k:
        try:
            penalty = 0.0
            grad_penalty = np.zeros_like(x)
            
            for g, grad_g in zip(constraints, grad_constraints):
                violation = max(0.0, -g(x))
                penalty += k * violation    
                
                if violation > 0:
                    grad_penalty += k * (-grad_g(x))
            
            P = f(x) + penalty
            grad_P = grad_f(x) + grad_penalty
            
            x_new = x - alpha * grad_P
            
            # Проверка на числовую стабильность
            if not all(np.isfinite(x_new)):
                raise ValueError("Потеря числовой стабильности")
            
            if iter_count > 0 and abs(P - prev_P) < epsilon:
                break
            
            x = x_new
            k *= 1.5  # Увеличиваем k медленнее
            iter_count += 1
            prev_P = P
            history.append(x.copy())
            
        except (OverflowError, ValueError) as e:
            # При ошибках уменьшаем шаг и сбрасываем k
            alpha *= 0.5
            k = max(1.0, k / 2)
            continue
    
    return x, history

def barrier_method(f, grad_f, constraints, grad_constraints, x0, M=1000.0, epsilon=0.05, alpha=0.001, max_iter=1000):
    """
    Барьеры
    """
    x = np.array(x0, dtype=float)
    iter_count = 0
    history = [x.copy()]
    prev_F = float('inf')
    
    while iter_count < max_iter:
        # Проверка допустимости точки перед вычислением барьера
        valid = all(g(x) > 1e-6 for g in constraints)  # Добавляем небольшой запас
        if not valid:
            if len(history) > 1:
                return history[-2], history
            else:
                raise ValueError("Начальная точка недопустима")
        
        try:
            B = 0.0
            grad_B = np.zeros_like(x)
            
            for g, grad_g in zip(constraints, grad_constraints):
                g_val = g(x)
                B += -log(g_val)
                grad_B += -grad_g(x) / g_val
            
            F = f(x) - M * B
            grad_F = grad_f(x) - M * grad_B
            
            x_new = x - alpha * grad_F
            
            # Проверка, что новая точка допустима
            if all(g(x_new) > 1e-6 for g in constraints):
                if iter_count > 0 and abs(F - prev_F) < epsilon:
                    break
                
                x = x_new
                iter_count += 1
                prev_F = F
                history.append(x.copy())
            else:
                alpha *= 0.5
                
        except (ValueError, OverflowError) as e:
            alpha *= 0.5
            continue
    
    return x, history

# Определение функций и градиентов для задачи из методички
def f(x):
    return 4*x[0] - x[1]**2 - 12

def grad_f(x):
    return np.array([4, -2*x[1]])

def g1(x):
    return 10*x[0] - x[0]**2 + 10*x[1] - x[1]**2 - 34

def grad_g1(x):
    return np.array([10 - 2*x[0], 10 - 2*x[1]])

def g2(x):
    return x[0]

def grad_g2(x):
    return np.array([1, 0])

def g3(x):
    return x[1]

def grad_g3(x):
    return np.array([0, 1])

constraints = [g1, g2, g3]
grad_constraints = [grad_g1, grad_g2, grad_g3]

# Начальная точка
x0 = [2.0, 4.0]

# Параметры
epsilon = 0.05
alpha_penalty = 0.001  # Уменьшенный шаг для штрафного метода
alpha_barrier = 0.001
M = 1000.0

print("Проверка начальной точки:")
print(f"g1(x0) = {g1(x0):.2f} (должно быть >= 0)")
print(f"g2(x0) = {g2(x0):.2f} (должно быть >= 0)")
print(f"g3(x0) = {g3(x0):.2f} (должно быть >= 0)")

print("\nМетод штрафных функций:")
x_penalty, history_penalty = penalty_method(f, grad_f, constraints, grad_constraints, x0, epsilon, alpha_penalty)
print(f"Найденное решение: {x_penalty}")
print(f"Значение функции: {f(x_penalty):.2f}")
print(f"Проверка ограничений: g1={g1(x_penalty):.2f}, g2={g2(x_penalty):.2f}, g3={g3(x_penalty):.2f}")

print("\nМетод барьерных функций:")
x_barrier, history_barrier = barrier_method(f, grad_f, constraints, grad_constraints, x0, M, epsilon, alpha_barrier)
print(f"Найденное решение: {x_barrier}")
print(f"Значение функции: {f(x_barrier):.2f}")
print(f"Проверка ограничений: g1={g1(x_barrier):.2f}, g2={g2(x_barrier):.2f}, g3={g3(x_barrier):.2f}")

# После вызовов методов добавим визуализацию
print("\nВизуализация метода штрафных функций:")
plot_optimization_process(history_penalty, "Метод штрафных функций", constraints)

print("\nВизуализация метода барьерных функций:")
plot_optimization_process(history_barrier, "Метод барьерных функций", constraints)

# Дополнительная 3D визуализация функции с ограничениями
def plot_3d_function():
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Создаем сетку для построения
    x1 = np.linspace(0, 5, 100)
    x2 = np.linspace(0, 5, 100)
    X1, X2 = np.meshgrid(x1, x2)
    Z = f([X1, X2])
    
    # Ограничение g1(x) >= 0
    g1_val = g1([X1, X2])
    Z[g1_val < 0] = np.nan  # Скрываем точки, где ограничение нарушено
    
    # Построение поверхности
    surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.7)
    
    # Траектории оптимизации
    hist_pen = np.array(history_penalty)
    hist_bar = np.array(history_barrier)
    
    ax.plot(hist_pen[:, 0], hist_pen[:, 1], [f(x) for x in hist_pen], 
            'r-', linewidth=2, label='Штрафной метод')
    ax.plot(hist_bar[:, 0], hist_bar[:, 1], [f(x) for x in hist_bar], 
            'b-', linewidth=2, label='Барьерный метод')
    
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x)')
    ax.set_title('3D визуализация функции с ограничениями и траекториями оптимизации')
    plt.legend()
    plt.show()

plot_3d_function()