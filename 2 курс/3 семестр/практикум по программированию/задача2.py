import numpy as np
import scipy.misc as misc
import scipy.integrate as integrate
import sympy as sp

def y(x):
    return 2 / (np.sin(x) + 4)
x0 = 2
first_derivative = misc.derivative(y, x0)
second_derivative = misc.derivative(y, x0, n=2)
print("")
print(f'Первая производная в точке x0={x0}: {first_derivative}')
print(f'Вторая производная в точке x0={x0}: {second_derivative}')
print("")

x = sp.symbols('x')
y = 2 / (sp.sin(x) + 4)
first_derivative_sym = sp.diff(y, x)
second_derivative_sym = sp.diff(first_derivative_sym, x)
print(f'Первая производная: {first_derivative_sym}')
print(f'Вторая производная: {second_derivative_sym}')
print("")

a = 3
b = 6
def y(x):
    return 2 / (np.sin(x) + 4)
integral, error = integrate.quad(y, a, b)
print(f'Результат интегрирования в пределах ({a},{b}): {integral}')
print("")

y = 2 / (sp.sin(x) + 4)
indefinite_integral = sp.integrate(y, x)
print(f'Неопределённый интеграл: {indefinite_integral}')
print("")

# Целевая функция
def objective(x):
    return (x[0] - 4)**2 + (x[1] - 2)**2

# Ограничения
constraints = (
    {'type': 'ineq', 'fun': lambda x: 4*x[0] + 2*x[1] - 11},
    {'type': 'ineq', 'fun': lambda x: -2*x[0] - 7},
)

# Ограничения на переменные (x1 >= 0 и x2 >= 0)
bounds = [(0, None), (0, None)]

# Начальная точка для оптимизации
initial_guess = [0, 0]

# Решение задачи оптимизации
result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

# Проверка успешности
if result.success:
    optimized_x = result.x
    optimized_value = result.fun
    print(f"Оптимальное значение: {optimized_value}")
    print(f"Оптимальные решения: x1 = {optimized_x[0]}, x2 = {optimized_x[1]}")
else:
    print("Оптимизация не удалась:", result.message)
