import math

def f(x):
    return 2 * x ** 2 - 1.5 * math.sqrt(x)

def left_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def right_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(1, n + 1))


def trapeze(f, a, b, n):
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    s += sum(f(a + i * h) for i in range(1, n))
    return h * s


def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        coeff = 4 if i % 2 != 0 else 2
        s += coeff * f(a + i * h)
    return h * s / 3

def runge_error(I_n, I_2n, p):
    return abs(I_2n - I_n) / (2 ** p - 1)


def integrate_with_runge(method, f, a, b, n_start, eps, p):
    n = n_start
    I_n = method(f, a, b, n)
    iterations = []
    while True:
        I_2n = method(f, a, b, n * 2)
        delta = runge_error(I_n, I_2n, p)
        iterations.append((n, I_n, n * 2, I_2n, delta))
        if delta < eps:
            return I_2n, n * 2, iterations
        n *= 2
        I_n = I_2n


def print_nodes_table(f, a, b, n):
    h = (b - a) / n
    print(f"\n{'i':>4}  {'x_i':>10}  {'f(x_i)':>12}")
    print("-" * 32)
    for i in range(n + 1):
        xi = a + i * h
        print(f"{i:>4}  {xi:>10.4f}  {f(xi):>12.6f}")

def main():
    a = 1
    b = 4
    n = 6
    eps = 1e-4

    methods = [
        (left_rectangles, 1, "Левые прямоугольники  "),
        (right_rectangles, 1, "Правые прямоугольники "),
        (trapeze, 2, "Трапеции              "),
        (simpson, 4, "Парабол (Симпсона)    "),
    ]

    print("=" * 60)
    print("   ЧИСЛЕННОЕ ИНТЕГРИРОВАНИЕ")
    print(f"   ∫(2x²−1.5√x)dx от {a} до {b},  n={n},  ε={eps}")
    print("=" * 60)

    print_nodes_table(f, a, b, n)

    print(f"\n{'Метод':<26}  {'I (n=' + str(n) + ')':>14}")
    print("-" * 44)
    for method, _, name in methods:
        I = method(f, a, b, n)
        print(f"{name}  {I:>14.6f}")

    print("\n" + "=" * 60)
    print("   УТОЧНЕНИЕ ПО ФОРМУЛЕ РУНГЕ")
    print("=" * 60)

    for method, p, name in methods:
        print(f"\n{name.strip()}  (p={p})")
        print(f"  {'n':>6}  {'I_n':>12}  {'2n':>6}  {'I_2n':>12}  {'Δ':>12}")
        print("  " + "-" * 60)
        result, n_final, iters = integrate_with_runge(method, f, a, b, n, eps, p)
        for (ni, Ini, n2i, I2ni, delta) in iters:
            ok = "✓" if delta < eps else ""
            print(f"  {ni:>6}  {Ini:>12.6f}  {n2i:>6}  {I2ni:>12.6f}  {delta:>12.8f}  {ok}")
        print(f"  Результат: I ≈ {result:.6f}  (при n={n_final})")

    print("\n" + "=" * 60)
    print("Готово.")


if __name__ == "__main__":
    main()