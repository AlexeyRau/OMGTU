from itertools import cycle
import numpy as np

C = np.array([
    [40, 36, 9, 20],
    [26, 11, 22, 26],
    [6, 3, 12, 3],
    [5, 37, 33, 26]
])

a = np.array([24, 42, 23, 36])
b = np.array([35, 29, 21, 35])

total_supply = np.sum(a)
total_demand = np.sum(b)

if total_supply > total_demand:
    print("Открытая модель. Добавляем фиктивный магазин.")
    b = np.append(b, total_supply - total_demand)
    C = np.hstack((C, np.zeros((C.shape[0], 1))))
    print(f"{total_supply} - {total_demand} = {b[len(b)-1]}, b{len(b)} = {b[len(b)-1]}")
elif total_supply < total_demand:
    print("Открытая модель. Добавляем фиктивный склад.")
    a = np.append(a, total_demand - total_supply)
    C = np.vstack((C, np.zeros((C.shape[1],))))
    print(f"{total_demand} - {total_supply} = {a[len(a)-1]}, a{len(a)} = {a[len(a)-1]}")
else:
    print("Закрытая модель.")

def north_west_corner(a, b):
    m, n = len(a), len(b)
    X = np.zeros((m, n))
    i, j = 0, 0
    
    while i < m and j < n:
        if a[i] < b[j]:
            X[i, j] = a[i]
            b[j] -= a[i]
            print(f"{i+j}-я итерация:")
            print(X)
            i += 1
        else:
            X[i, j] = b[j]
            a[i] -= b[j]
            print(f"{i+j}-я итерация:")
            print(X)
            j += 1
    print("------------------------")
    return X

def calculate_potentials(X, C):
    m, n = X.shape
    u = np.full(m, np.nan)
    v = np.full(n, np.nan)
    u[0] = 0

    basis_cells = [(i, j) for i in range(m) for j in range(n) if X[i, j] > 0]
    
    while basis_cells:
        for i, j in basis_cells:
            if not np.isnan(u[i]) and np.isnan(v[j]):
                v[j] = C[i, j] - u[i]
                basis_cells.remove((i, j))
            elif not np.isnan(v[j]) and np.isnan(u[i]):
                u[i] = C[i, j] - v[j]
                basis_cells.remove((i, j))
    
    return u, v

u, v = calculate_potentials(X, C)
print("Потенциалы u:", u)
print("Потенциалы v:", v)

def find_entering_cell(X, C, u, v):
    max_diff = 0
    entering_cell = None
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i, j] == 0:
                diff = u[i] + v[j] - C[i, j]
                if diff > max_diff:
                    max_diff = diff
                    entering_cell = (i, j)
    
    return entering_cell

entering_cell = find_entering_cell(X, C, u, v)

print(f"Начальная точка: {entering_cell}")

def find_cycle(X, entering_cell):
    m, n = X.shape
    i0, j0 = entering_cell
    path = [(i0, j0)]
    visited = set()

    def dfs(i, j, step):
        if (i, j) == (i0, j0) and step > 0:
            return True

        if step % 2 == 0:
            for j_next in range(n):
                if j_next != j and (X[i, j_next] > 0 or (i, j_next) == (i0, j0)):
                    if (i, j_next) not in visited:
                        visited.add((i, j_next))
                        path.append((i, j_next))
                        if dfs(i, j_next, step + 1):
                            return True
                        path.pop()
                        visited.remove((i, j_next))
        else:
            for i_next in range(m):
                if i_next != i and (X[i_next, j] > 0 or (i_next, j) == (i0, j0)):
                    if (i_next, j) not in visited:
                        visited.add((i_next, j))
                        path.append((i_next, j))
                        if dfs(i_next, j, step + 1):
                            return True
                        path.pop()
                        visited.remove((i_next, j))
        return False

    dfs(i0, j0, 0)
    
    if len(path) > 1 and path[-1] == path[0]:
        path.pop()
    
    return path

def redistribute_supplies(X, cycle):
    min_value = float('inf')
    for idx, (i, j) in enumerate(cycle):
        if idx % 2 == 1:
            if X[i, j] < min_value:
                min_value = X[i, j]

    if min_value == float('inf'):
        return X

    for idx, (i, j) in enumerate(cycle):
        if idx % 2 == 1:
            X[i, j] -= min_value
        else:
            X[i, j] += min_value

    return X