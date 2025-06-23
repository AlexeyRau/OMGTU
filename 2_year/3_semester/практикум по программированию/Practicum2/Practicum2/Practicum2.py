import numpy as np
import scipy.misc as misc
import scipy.integrate as integrate
import sympy as sp
from scipy.optimize import minimize

#Поиск первой и второй производной в точке x0
def y(x):
    return 2 / (np.sin(x) + 4)
x0 = 2
first_derivative = misc.derivative(y, x0)
second_derivative = misc.derivative(y, x0, n=2)
print("")
print(f'Первая производная в точке x0={x0}: {first_derivative}')
print(f'Вторая производная в точке x0={x0}: {second_derivative}')
print("")

#Символьные представления первой и второй производных
x = sp.symbols('x')
y = 2 / (sp.sin(x) + 4)
first_derivative_sym = sp.diff(y, x)
second_derivative_sym = sp.diff(first_derivative_sym, x)
print(f'Первая производная: {first_derivative_sym}')
print(f'Вторая производная: {second_derivative_sym}')
print("")

#Вычисление определённого интеграла методом прямоугольников
a = 3
b = 6
n = 1000#Количество прямоугольников
def y(x):
    return 2 / (np.sin(x) + 4)

def rectangle_method(func, a, b, n):
    h = (b - a) / n #Шаг
    integral = 0.0
    
    for i in range(n):
        x = a + i * h #x i-е(Точка левая граница подынтеграла)
        integral += func(x) * h #Сумма значений интегралов каждого отрезка(сумма площадей прямоугольников)
    
    return integral

result = rectangle_method(y, a, b, n)
print(f'Результат интегрирования в пределах ({a},{b}): {result}')
print("")

#Вывод неопределённого интеграла с помощью sympy
y = 2 / (sp.sin(x) + 4)
indefinite_integral = sp.integrate(y, x)
print(f'Неопределённый интеграл: {indefinite_integral}')
print("")

#Решение задачи нелинейной оптимизации
def objective(x):
    return (x[0] - 4)**2 + (x[1] - 2)**2

# Ограничения
def constraint1(x):
    return 4*x[0] + 2*x[1] - 11
def constraint2(x):
    return -2*x[0] - 7

constraints = ({'type': 'ineq', 'fun': constraint1},
               {'type': 'ineq', 'fun': constraint2})

# Ограничения на переменные (x1 >= 0 и x2 >= 0)
bounds = ((0, None), (0, None))

# Начальная точка для оптимизации
x0 = np.array([0, 0])

# Решение задачи оптимизации
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# Проверка успешности
if result.success:
    print(f"Оптимальное значение: {result.fun}")
    print(f"Оптимальные решения: x1 = {result.x[0]}, x2 = {result.x[1]}")
else:
    print("Оптимизация не удалась:", result.message)
    
print(result)