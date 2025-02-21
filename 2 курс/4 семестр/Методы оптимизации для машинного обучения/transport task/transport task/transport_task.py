import numpy as np

# Матрица стоимости
C = np.array([
    [40, 36, 9, 20],
    [26, 11, 22, 26],
    [6, 3, 12, 3],
    [5, 37, 33, 26]
])
# Вектор ai
a = np.array([24, 42, 23, 36])
# Вектор bj
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

# Построение начальной таблицы
X = north_west_corner(a.copy(), b.copy())
print("Начальная транспортная таблица:")
print(X)

