import numpy as np

def f(x):
    return x**3 + 6*x + 3

# --- Метод 1: Разностный Ньютон ---
def method_diff_newton(x0, h, eps):
    print("\n--- МЕТОД 1: РАЗНОСТНЫЙ НЬЮТОН ---")
    x_curr = x0
    for i in range(1, 20):
        fx = f(x_curr)
        fh = f(x_curr + h)
        x_next = x_curr - (fx * h) / (fh - fx)
        
        delta = abs(x_next - x_curr)
        print(f"Итерация {i}: x = {x_next:.8f}, delta = {delta:.2e}")
        
        if delta < eps:
            return x_next
        x_curr = x_next

# --- Метод 2: Метод хорд ---
def method_chords(a, b, eps):
    print("\n--- МЕТОД 2: МЕТОД ХОРД ---")
    # Проверка неподвижной точки: f(x)*f''(x) > 0
    # f'' = 6x. При x = -1 f(-1)=-4, f''(-1)=-6 -> (-4)*(-6)=24 > 0.
    # Значит 'a' (-1) - неподвижная точка, начинаем итерации с 'b' (0).
    fixed = a
    x_curr = b
    
    for i in range(1, 20):
        fx = f(x_curr)
        fa = f(fixed)
        
        # Формула метода хорд
        x_next = x_curr - (fx * (x_curr - fixed)) / (fx - fa)
        
        delta = abs(x_next - x_curr)
        print(f"Итерация {i}: x = {x_next:.8f}, delta = {delta:.2e}")
        
        if delta < eps:
            return x_next
        x_curr = x_next

# Параметры задачи
eps_high = 1e-6
h_step = 1e-4

# Запуск
res1 = method_diff_newton(x0=-0.5, h=h_step, eps=eps_high)
res2 = method_chords(a=-1.0, b=0.0, eps=eps_high)

print(f"\nРезультат 1: {res1:.7f}")
print(f"Результат 2: {res2:.7f}")