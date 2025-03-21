import math

def dichotomy_method(f, a, b, epsilon):
    while abs(b - a) > 2 * epsilon:
        x1 = (a + b) / 2 - epsilon / 2
        x2 = (a + b) / 2 + epsilon / 2
        if f(x1) > f(x2):
            a = x1
        else:
            b = x2
    x_min = (a + b) / 2
    return x_min, f(x_min)

def fibonacci_method(f, a, b, epsilon):
    def generate_fibonacci(n):
        fib = [1, 1]
        while fib[-1] < n:
            fib.append(fib[-1] + fib[-2])
        return fib

    fib = generate_fibonacci((b - a) / epsilon)
    n = len(fib) - 1

    x1 = a + (fib[n - 2] / fib[n]) * (b - a)
    x2 = a + (fib[n - 1] / fib[n]) * (b - a)
    f1, f2 = f(x1), f(x2)

    for k in range(1, n):
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (fib[n - k - 1] / fib[n - k]) * (b - a)
            f2 = f(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (fib[n - k - 2] / fib[n - k]) * (b - a)
            f1 = f(x1)

    x_min = (a + b) / 2
    return x_min, f(x_min)

def golden_section_method(f, a, b, epsilon):
    tau = (3 - 5 ** 0.5) / 2
    x1 = a + tau * (b - a)
    x2 = b - tau * (b - a)
    f1, f2 = f(x1), f(x2)

    while abs(b - a) > epsilon:
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - tau * (b - a)
            f2 = f(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + tau * (b - a)
            f1 = f(x1)

    x_min = (a + b) / 2
    return x_min, f(x_min)

def f(x):
    return x**4 / math.log(x)

a = 1.1
b = 1.5
epsilon = 0.001

x_min_dichotomy, f_min_dichotomy = dichotomy_method(f, a, b, epsilon)
print(f"Метод дихотомии: x_min = {x_min_dichotomy}, f_min = {f_min_dichotomy}")

x_min_fibonacci, f_min_fibonacci = fibonacci_method(f, a, b, epsilon)
print(f"Метод Фибоначчи: x_min = {x_min_fibonacci}, f_min = {f_min_fibonacci}")

x_min_golden, f_min_golden = golden_section_method(f, a, b, epsilon)
print(f"Метод золотого сечения: x_min = {x_min_golden}, f_min = {f_min_golden}")