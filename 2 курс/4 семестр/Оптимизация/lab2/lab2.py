import numpy as np
from scipy.optimize import minimize_scalar

# Целевая функция (пример для варианта 1 из таблицы 2)
def f(x, A=20, a=1, b=2):
    return A - (x[0]-a)*np.exp(-(x[0]-a)) - (x[1]-b)*np.exp(-(x[1]-b))

# Метод Гаусса-Зейделя (покоординатный спуск)
def gauss_seidel(f, x0, epsilon=1e-6, max_iter=1000):
    """
    Алгоритм метода Гаусса-Зейделя из методички:
    """
    # Шаг 1: Задать точность ε > 0 и стартовую точку x⁰
    x = np.array(x0, dtype=float)
    n = len(x)
    k = 1
    history = [x.copy()]
    
    while True:
        # Шаг 1: Принять y¹ = x⁰
        y = x.copy()
        
        # Шаг 2: Последовательная минимизация по координатам (j=1..n)
        for j in range(n):
            # Шаг 2.1: Создать направление eⱼ
            e = np.eye(n)[j]
            
            # Шаг 2.2: Одномерный поиск min f(y⁽ʲ⁾ + λeⱼ)
            res = minimize_scalar(lambda l: f(y + l*e))
            l = res.x
            
            # Шаг 2.3: Обновить y⁽ʲ⁺¹⁾ = y⁽ʲ⁾ + λⱼeⱼ
            y[j] += l
        
        # Шаг 3: Принять x⁽ᵏ⁺¹⁾ = y⁽ⁿ⁺¹⁾
        x_new = y.copy()
        
        # Шаг 4: Проверка условия остановки ||x⁽ᵏ⁺¹⁾ - x⁽ᵏ⁾|| < ε
        if np.linalg.norm(x_new - x) < epsilon or k >= max_iter:
            break
            
        # Шаг 5: Обновить x⁽ᵏ⁾ и продолжить итерации
        x = x_new.copy()
        history.append(x.copy())
        k += 1
    
    return x_new, f(x_new), history

# Метод наискорейшего спуска
def steepest_descent(f, x0, epsilon=1e-6, max_iter=1000, h=1e-6):
    """
    Алгоритм метода наискорейшего спуска из методички:
    """
    # Шаг 1: Задать ε > 0 и начальную точку x⁰
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    
    for k in range(1, max_iter+1):
        # Шаг 2: Вычислить градиент ∇f(x⁽ᵏ⁾) (численно)
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += h
            x_minus = x.copy()
            x_minus[i] -= h
            grad[i] = (f(x_plus) - f(x_minus)) / (2*h)
        
        # Шаг 3: Проверить условие ||∇f(x⁽ᵏ⁾)|| < ε
        if np.linalg.norm(grad) < epsilon:
            break
            
        # Шаг 4: Определить направление S⁽ᵏ⁾ = -∇f(x⁽ᵏ⁾)
        S = -grad
        
        # Шаг 5: Одномерная минимизация min f(x⁽ᵏ⁾ + λS⁽ᵏ⁾)
        res = minimize_scalar(lambda l: f(x + l*S))
        l = res.x
        
        # Шаг 6: Обновить x⁽ᵏ⁺¹⁾ = x⁽ᵏ⁾ + λS⁽ᵏ⁾
        x = x + l*S
        history.append(x.copy())
    
    return x, f(x), history

# Пример использования
if __name__ == "__main__":
    x0 = [0.0, 0.0]
    epsilon = 1e-6
    
    # Запуск метода Гаусса-Зейделя
    gs_result = gauss_seidel(f, x0, epsilon)
    print("Gauss-Seidel:")
    print(f"Точка минимума: {gs_result[0]}")
    print(f"Значение функции: {gs_result[1]:.6f}")
    
    # Запуск метода наискорейшего спуска
    sd_result = steepest_descent(f, x0, epsilon)
    print("\nSteepest Descent:")
    print(f"Точка минимума: {sd_result[0]}")
    print(f"Значение функции: {sd_result[1]:.6f}")