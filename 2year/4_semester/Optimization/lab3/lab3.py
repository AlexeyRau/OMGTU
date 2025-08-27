import numpy as np
from scipy.optimize import minimize, minimize_scalar

class LinearConstraint:
    def __init__(self, a, b, description=""):
        self.a = np.array(a)
        self.b = b
        self.description = description

def zoutendijk_method(f, grad_f, constraints, x0, tol=1e-6, max_iter=100, verbose=True):
    x = np.array(x0, dtype=float)
    n = len(x0)
    
    if verbose:
        print("="*60)
        print("НАЧАЛО РЕШЕНИЯ МЕТОДОМ ЗОЙТЕНДЕЙКА")
        print(f"Начальная точка: x0 = {x}")
        print(f"Значение функции: F(x0) = {f(x):.6f}")
        print("="*60)
    
    for iter in range(max_iter):
        if verbose:
            print(f"\n{'='*20} ИТЕРАЦИЯ {iter+1} {'='*20}")
            print(f"Текущая точка: x = {x}")
            print(f"F(x) = {f(x):.6f}")
        
        # 1. Вычисляем градиент
        grad = grad_f(x)
        if verbose:
            print(f"Градиент: ∇F(x) = {grad}")
            print(f"Длина градиента: ||∇F(x)|| = {np.linalg.norm(grad):.6f}")
        
        # 2. Определяем активные ограничения
        active_indices = []
        active_constraints = []
        for i, constr in enumerate(constraints):
            g_val = np.dot(constr.a, x) - constr.b
            if -tol <= g_val <= tol:
                active_indices.append(i)
                active_constraints.append(constr)
        
        if verbose:
            print("\nАктивные ограничения:")
            for i in active_indices:
                constr = constraints[i]
                print(f" - {constr.description}: {constr.a}·x = {constr.b}")
        
        # 3. Находим направление движения
        def objective(d):
            return -np.dot(d, grad)
        
        d0 = grad / np.linalg.norm(grad) if np.linalg.norm(grad) > tol else np.zeros(n)
        
        constraints_opt = []
        for i in active_indices:
            a_i = constraints[i].a
            constraints_opt.append({
                'type': 'ineq',
                'fun': lambda d, a_i=a_i: -np.dot(a_i, d)
            })
        constraints_opt.append({
            'type': 'ineq',
            'fun': lambda d: 1 - np.linalg.norm(d)
        })
        
        res = minimize(objective, d0, method='SLSQP', constraints=constraints_opt, options={'ftol': tol})
        if not res.success:
            if verbose:
                print("\nОШИБКА: Не удалось найти направление движения!")
            break
        
        d = res.x
        beta = np.dot(d, grad)
        
        if verbose:
            print(f"\nНайденное направление: d = {d}")
            print(f"Проекция градиента на направление: β = ∇F·d = {beta:.6f}")
        
        # 4. Проверка условия останова
        if beta <= tol:
            if verbose:
                print("\nУСЛОВИЕ ОСТАНОВА: Нет улучшающего направления (β ≤ tol)")
            break
        
        # 5. Находим максимальный шаг
        alpha_max = float('inf')
        limiting_constraint = None
        for constr in constraints:
            a_dot_d = np.dot(constr.a, d)
            g_val = np.dot(constr.a, x) - constr.b
            
            if a_dot_d > tol:  # Ограничение может быть нарушено
                alpha_candidate = -g_val / a_dot_d
                if alpha_candidate < alpha_max:
                    alpha_max = alpha_candidate
                    limiting_constraint = constr
        
        if verbose:
            print(f"\nМаксимальный шаг: α_max = {alpha_max:.6f}", end=" ")
            if limiting_constraint:
                print(f"(ограничено: {limiting_constraint.description})")
            else:
                print()
        
        if alpha_max <= tol:
            if verbose:
                print("\nОСТАНОВ: Недопустимое направление (α_max ≤ tol)")
            break
        
        # 6. Одномерная оптимизация
        def f_alpha(alpha):
            return -f(x + alpha * d)
        
        res_alpha = minimize_scalar(f_alpha, bounds=(0, alpha_max), method='bounded')
        if not res_alpha.success:
            if verbose:
                print("\nОШИБКА: Не удалось найти оптимальный шаг!")
            break
        
        alpha_opt = res_alpha.x
        x_new = x + alpha_opt * d
        
        if verbose:
            print(f"Оптимальный шаг: α_opt = {alpha_opt:.6f}")
            print(f"Новая точка: x_new = {x_new}")
            print(f"Значение функции в новой точке: F(x_new) = {f(x_new):.6f}")
        
        # 7. Обновление точки
        x = x_new
    
    if verbose:
        print("\n" + "="*60)
        print("РЕЗУЛЬТАТ:")
        print(f"Оптимальная точка: x = {x}")
        print(f"Максимальное значение функции: F(x) = {f(x):.6f}")
        print("="*60)
    
    return x, f(x)


# Данные для задачи из примера 1

def f(x):
    x1, x2 = x
    return -x1**2 + x1*x2 - 2*x2**2 + 4*x1 + 6*x2

def grad_f(x):
    x1, x2 = x
    return np.array([
        -2*x1 + x2 + 4,   # ∂f/∂x1
        x1 - 4*x2 + 6     # ∂f/∂x2
    ])

constraints = [
    LinearConstraint([1, 1], 4, "x₁ + x₂ ≤ 4"),        # x1 + x2 <= 4
    LinearConstraint([-1, -2], -2, "x₁ + 2x₂ ≥ 2"),    # -x1 -2x2 <= -2 → x1 + 2x2 >= 2
    LinearConstraint([-1, 0], 0, "x₁ ≥ 0"),            # -x1 <= 0 → x1 >= 0
    LinearConstraint([0, -1], 0, "x₂ ≥ 0")             # -x2 <= 0 → x2 >= 0
]

x0 = np.array([3.0, 1.0])

# Запуск метода
print("Задача 1")
x_opt, f_opt = zoutendijk_method(f, grad_f, constraints, x0, tol=1e-4)

# Проверка с ожидаемым результатом
expected_point = np.array([2.25, 1.75])
expected_value = 12.25

print("\nПроверка с примером:")
print(f"Расчетная точка: {x_opt}")
print(f"Ожидаемая точка: ({2.25:.6f}, {1.75:.6f})")
print(f"Расчетное значение функции: {f_opt:.6f}")
print(f"Ожидаемое значение: {expected_value:.6f}")
print(f"Разница: {abs(f_opt - expected_value):.6f}")



# Данные для задачи из примера 2
def f(x):
    x1, x2 = x
    return -6*x1**2 - x2**2 + 2*x1*x2 + 10*x2

def grad_f(x):
    x1, x2 = x
    return np.array([
        -12*x1 + 2*x2,
        -2*x2 + 2*x1 + 10
    ])

# Ограничения с описаниями для вывода
constraints = [
    LinearConstraint([2, 1], 5, "2x₁ + x₂ ≤ 5"),
    LinearConstraint([-2, -1], -2, "2x₁ + x₂ ≥ 2"),
    LinearConstraint([-1, 0], 0, "x₁ ≥ 0"),
    LinearConstraint([0, -1], 0, "x₂ ≥ 0")
]

x0 = np.array([0.0, 4.0])

# Запуск метода
print("Задача 2")
x_opt, f_opt = zoutendijk_method(f, grad_f, constraints, x0, tol=1e-4)

# Проверка с ожидаемым результатом
expected_point = np.array([5/14, 30/7])
expected_value = 375/14

print("\nПроверка с примером:")
print(f"Расчетная точка: {x_opt}")
print(f"Ожидаемая точка: ({5/14:.6f}, {30/7:.6f})")
print(f"Расчетное значение функции: {f_opt:.6f}")
print(f"Ожидаемое значение: {expected_value:.6f}")
print(f"Разница: {abs(f_opt - expected_value):.6f}")