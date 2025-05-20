import numpy as np

def zoiten_method(
    x0, 
    F, 
    grad_F, 
    constraints, 
    constraint_types, 
    max_iter=10, 
    tol=1e-6
):
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    
    for _ in range(max_iter):
        gradient = grad_F(x)
        print(f"Текущая точка: {x}, Градиент: {gradient}")
        
        # Шаг 1: Движение вдоль градиента
        direction = gradient
        alpha_min, alpha_max = 0.0, 1.0
        
        for _ in range(100):
            alpha = (alpha_min + alpha_max) / 2
            x_test = x + alpha * direction
            if is_feasible(x_test, constraints, constraint_types, tol):
                alpha_min = alpha
            else:
                alpha_max = alpha
            if (alpha_max - alpha_min) < tol:
                break
        
        x_new = x + alpha_min * direction
        
        # Шаг 2: Проверка активных ограничений
        active = get_active_constraints(x_new, constraints, constraint_types, tol)
        
        if active:
            S = get_tangent_direction(active[0]["gradient"])
            alpha = find_alpha_along_boundary(x_new, S, F, constraints, constraint_types, tol)
            x_new = x_new + alpha * S
        
        x = x_new
        history.append(x.copy())
        
        # Условие остановки
        if active and np.dot(grad_F(x), S) < tol:
            print("Максимум найден.")
            break
    
    return x, history

# Вспомогательные функции
def is_feasible(x, constraints, constraint_types, tol):
    for i, (constraint, c_type) in enumerate(zip(constraints, constraint_types)):
        value = constraint(x)
        if c_type == 'leq' and value > tol:
            return False
        if c_type == 'geq' and value < -tol:
            return False
    return True

def get_active_constraints(x, constraints, constraint_types, tol):
    active = []
    for i, (constraint, c_type) in enumerate(zip(constraints, constraint_types)):
        value = constraint(x)
        if abs(value) < tol:
            active.append({
                "gradient": grad_constraint(x, i),
                "type": c_type
            })
    return active

def grad_constraint(x, constraint_index):
    if constraint_index == 0:  # 2x1 + x2 <= 5
        return np.array([2, 1], dtype=float)
    elif constraint_index == 1:  # 2x1 + x2 >= 2
        return np.array([2, 1], dtype=float)
    elif constraint_index == 2:  # x1 >= 0
        return np.array([-1, 0], dtype=float)
    elif constraint_index == 3:  # x2 >= 0
        return np.array([0, -1], dtype=float)
    else:
        raise ValueError("Неверный индекс ограничения")

def get_tangent_direction(normal):
    S = np.array([normal[1], -normal[0]])
    return S / np.linalg.norm(S)

def find_alpha_along_boundary(x_start, direction, F, constraints, constraint_types, tol):
    alpha_min, alpha_max = 0.0, 1.0
    for _ in range(100):
        alpha = (alpha_min + alpha_max) / 2
        x_test = x_start + alpha * direction
        if is_feasible(x_test, constraints, constraint_types, tol):
            alpha_min = alpha
        else:
            alpha_max = alpha
        if (alpha_max - alpha_min) < tol:
            break
    return alpha_min

# Определение целевой функции и ограничений (пример из методички)
def F(x):
    return -6*x[0]**2 - x[1]**2 + 2*x[0]*x[1] + 10*x[1]

def grad_F(x):
    return np.array([-12*x[0] + 2*x[1], -2*x[1] + 2*x[0] + 10])

def constraint1(x):
    return 2*x[0] + x[1] - 5  # 2x1 + x2 <= 5

def constraint2(x):
    return 2 - (2*x[0] + x[1])  # 2x1 + x2 >= 2

def constraint3(x):
    return -x[0]  # x1 >= 0

def constraint4(x):
    return -x[1]  # x2 >= 0

constraints = [constraint1, constraint2, constraint3, constraint4]
constraint_types = ['leq', 'leq', 'leq', 'leq']

# Запуск метода
x_opt, history = zoiten_method(
    x0=[0, 4], 
    F=F, 
    grad_F=grad_F, 
    constraints=constraints, 
    constraint_types=constraint_types
)

print("Оптимальная точка:", x_opt)
print("Значение F:", F(x_opt))