import math

def f(x, y):
    return math.sin(x + 1) - y - 1

def g(x, y):
    return 2 * x + math.cos(y) - 2

def phi_x(y):
    return 1 - 0.5 * math.cos(y)

def phi_y(x):
    return math.sin(x + 1) - 1

def get_derivatives(x, y):
    return {
        'df_dx': math.cos(x + 1),
        'df_dy': -1,
        'dg_dx': 2,
        'dg_dy': -math.sin(y)
    }

def method_jacobi(x, y, eps):
    iters = 0
    while True:
        x_new = phi_x(y)
        y_new = phi_y(x)
        if max(abs(x_new - x), abs(y_new - y)) < eps:
            return x_new, y_new, iters
        x, y = x_new, y_new
        iters += 1

def method_seidel(x, y, eps):
    iters = 0
    while True:
        x_old, y_old = x, y
        x = phi_x(y)
        y = phi_y(x)
        if max(abs(x - x_old), abs(y - y_old)) < eps:
            return x, y, iters
        iters += 1

def method_newton(x, y, eps):
    iters = 0
    while True:
        d = get_derivatives(x, y)
        f_val = f(x, y)
        g_val = g(x, y)
        
        det = d['df_dx'] * d['dg_dy'] - d['df_dy'] * d['dg_dx']
        dx = (-f_val * d['dg_dy'] - (-g_val * d['df_dy'])) / det
        dy = (d['df_dx'] * (-g_val) - d['dg_dx'] * (-f_val)) / det
        
        x += dx
        y += dy
        iters += 1
        if max(abs(dx), abs(dy)) < eps:
            return x, y, iters

def method_steepest_descent(x, y, eps):
    iters = 0
    alpha_start = 1.0
    while True:
        d = get_derivatives(x, y)
        fv, gv = f(x, y), g(x, y)
        
        grad_x = 2 * fv * d['df_dx'] + 2 * gv * d['dg_dx']
        grad_y = 2 * fv * d['df_dy'] + 2 * gv * d['dg_dy']
        
        alpha = alpha_start
        phi_old = fv**2 + gv**2
        while True:
            x_n, y_n = x - alpha * grad_x, y - alpha * grad_y
            if (f(x_n, y_n)**2 + g(x_n, y_n)**2) < phi_old:
                break
            alpha /= 2
            if alpha < 1e-12: return x, y, iters
            
        if max(abs(x_n - x), abs(y_n - y)) < eps:
            return x_n, y_n, iters
        x, y = x_n, y_n
        iters += 1

X0, Y0 = 0.5, 0.5
EPS = 0.001

results = {
    "Якоби (п. 4.1)": method_jacobi(X0, Y0, EPS),
    "Зейдель (п. 4.2)": method_seidel(X0, Y0, EPS),
    "Ньютон (п. 4.3)": method_newton(X0, Y0, EPS),
    "Спуск (Доп)": method_steepest_descent(X0, Y0, EPS)
}

print(f"{'Метод':<20} | {'x':<10} | {'y':<10} | {'Ит.':<5}")
print("-" * 55)
for name, res in results.items():
    print(f"{name:<20} | {res[0]:.6f} | {res[1]:.6f} | {res[2]:<5}")