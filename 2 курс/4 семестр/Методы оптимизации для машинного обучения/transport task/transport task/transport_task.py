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
    print(f"{total_supply} - {total_demand} = {b[len(b)-1]}, b{len(b)} = {b[len(b)-1]}")
elif total_supply < total_demand:
    print("Открытая модель. Добавляем фиктивный склад.")
    a = np.append(a, total_demand - total_supply)
    print(f"{total_demand} - {total_supply} = {a}, a{len(a)} = {a[len(a)-1]}")
else:
    print("Закрытая модель.")