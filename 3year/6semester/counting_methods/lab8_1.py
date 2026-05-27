import numpy as np

def f(x, y):
    return y - 5 * x + 1

def euler_method(f, x0, y0, h, b):
    x = np.arange(x0, b + h/2, h)
    y = np.zeros(len(x))
    y[0] = y0
    for i in range(1, len(x)):
        y[i] = y[i-1] + h * f(x[i-1], y[i-1])
    return x, y

def modified_euler_method(f, x0, y0, h, b):
    x = np.arange(x0, b + h/2, h)
    y = np.zeros(len(x))
    y[0] = y0
    for i in range(1, len(x)):
        y_tilde = y[i-1] + h * f(x[i-1], y[i-1])
        y[i] = y[i-1] + (h / 2) * (f(x[i-1], y[i-1]) + f(x[i], y_tilde))
    return x, y

def runge_kutta_4(f, x0, y0, h, b):
    x = np.arange(x0, b + h/2, h)
    y = np.zeros(len(x))
    y[0] = y0
    for i in range(1, len(x)):
        k0 = h * f(x[i-1], y[i-1])
        k1 = h * f(x[i-1] + h/2, y[i-1] + k0/2)
        k2 = h * f(x[i-1] + h/2, y[i-1] + k1/2)
        k3 = h * f(x[i-1] + h, y[i-1] + k2)
        y[i] = y[i-1] + (k0 + 2*k1 + 2*k2 + k3) / 6
    return x, y

x0 = 0.0
y0 = 2.0
h = 0.8
b = 3.2

print(f"y' = y - 5x + 1,  y({x0}) = {y0},  x ∈ [{x0}; {b}],  h = {h}\n")

x_e, y_e = euler_method(f, x0, y0, h, b)
print("Метод Эйлера:")
print("x\t\ty")
for xi, yi in zip(x_e, y_e):
    print(f"{xi:.1f}\t\t{yi:.6f}")

print("\nМодифицированный метод Эйлера:")
x_me, y_me = modified_euler_method(f, x0, y0, h, b)
print("x\t\ty")
for xi, yi in zip(x_me, y_me):
    print(f"{xi:.1f}\t\t{yi:.6f}")

print("\nМетод Рунге-Кутта 4-го порядка:")
x_rk, y_rk = runge_kutta_4(f, x0, y0, h, b)
print("x\t\ty")
for xi, yi in zip(x_rk, y_rk):
    print(f"{xi:.1f}\t\t{yi:.6f}")