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
