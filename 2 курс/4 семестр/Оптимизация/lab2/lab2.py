import numpy as np
from scipy.optimize import minimize_scalar

def gauss_seidel(f, x0, epsilon, max_iter=1000):
    
    n = len(x0)
    x_current = np.array(x0)
    y = x_current.copy() # Принять y¹ = x¹
    k = 1
    
    for _ in range(max_iter):
        j = 0                 
        while j < n:
            # Базисный вектор e_{j+1}
            direction = np.zeros(n)
            direction[j] = 1.0
            
            # Одномерная минимизация
            def func(lam):
                return f(y + lam * direction)
            
            res = minimize_scalar(func)
            lambda_opt = res.x
            
            # Обновление y
            y += lambda_opt * direction
            j += 1             # j = j+1
            
            # Выход при достижении предела итераций
            if j >= n: 
                break

        # Проверка условия останова
        x_next = y.copy()
        if np.linalg.norm(x_next - x_current) < epsilon:
            return x_next
        
        # Подготовка к новой итерации (п.3 алгоритма)
        x_current = x_next.copy()
        y = x_current.copy()   # y¹ = x^{k+1}
        k += 1

    print("Достигнут лимит итераций")
    return x_current

def steepest_descent(f, grad_f, x0, epsilon=1e-6, max_iter=1000):
    
    x_current = np.array(x0, dtype=float)
    k = 1
    
    for _ in range(max_iter):
        # Вычисление нормы градиента
        gradient = grad_f(x_current)
        grad_norm = np.linalg.norm(gradient)
        
        # Проверка условия останова
        if grad_norm < epsilon:
            print(f"Сходимость достигнута на итерации {k}")
            return x_current
        
        # Определение направления спуска
        S = -gradient  # Направление наискорейшего спуска
        
        # Одномерная минимизация
        def line_search(lam):
            return f(x_current + lam * S)
        
        res = minimize_scalar(line_search)
        lambda_opt = res.x
        
        # Обновление точки
        x_next = x_current + lambda_opt * S
        
        # Подготовка к следующей итерации
        x_current = x_next.copy()
        k += 1

    print("Достигнут максимальный лимит итераций")
    return x_current


if __name__ == "__main__":
    def test_function(x, A=20, a=1, b=2):
        return A - (x[0]-a)*np.exp(-(x[0]-a)) - (x[1]-b)*np.exp(-(x[1]-b))
    
    def test_gradient(x, a=1, b=2):
        dx0 = -np.exp(-(x[0]-a)) * (1 - (x[0]-a))
        dx1 = -np.exp(-(x[1]-b)) * (1 - (x[1]-b))
        return np.array([dx0, dx1])
    
    x0 = np.array([0.0, 0.0])
    epsilon = 1e-6
    
    result = gauss_seidel(test_function, x0, epsilon)
    print("метод Гаусса-Зейделя:")
    print(f"Оптимальная точка: {result}")
    print(f"Значение функции: {test_function(result)}")
    print("------------------------------------------------------")
    result = steepest_descent(test_function, test_gradient, x0, epsilon)
    print("метод наискорейшего спуска:")
    print(f"Оптимальная точка: {result}")
    print(f"Значение функции: {test_function(result)}")