import numpy as np

print("Создание массива my_array:")
my_array = np.arange(10, 70, 2)
print(my_array)
print("")

print("Преобразование массива my_array в матрицу A:")
A = my_array.reshape(6, 5)
print(A)
print("")

print("Транспонирование матрицы A:")
A = A.transpose()
print(A)
print("")

print("Умножение всех элементов матрицы на 2.5 и вычитание из каждого элемента 5:")
A = A * 2.5 - 5
print(A)
print("")

print("Создание матрицы B")
B = np.random.uniform(0, 10, (6, 3))
print(B)
print("")

print("Вектор a из сумм по всем строкам матрицы A")
a = A.sum(axis=1)
print(a)
print("")

print("Вектор b из сумм по всем столбцам матрицы B")
b = B.sum(axis=0)
print(b)
print("")

print("Произведение матриц A и B")
C = np.dot(A, B)
print(C)
print("")

print("Матрица A без третьего столбца")
A = np.delete(A, 2, axis=1)
print(A)
print("")

print("Матрица B плюс три столбца из случайных чисел")
B = np.hstack((B, np.random.uniform(10, 20, (6, 3))))
print(B)
print("")

print("Определитель матрицы A:")
detA = np.linalg.det(A)
print(detA)
print("")
print("Определитель матрицы B:")
detB = np.linalg.det(B)
print(detB)
print("")

print("Обратная матрица A:")
if detA != 0:
    inv_A = np.linalg.inv(A)
else:
    inv_A = None
print(inv_A)
print("")

print("Обратная матрица B:")
if detB != 0:
    inv_B = np.linalg.inv(B)
else:
    inv_B = None
print(inv_B)
print("")

print("A в 6 степени")
A_power_6 = np.linalg.matrix_power(A, 6)
print(A_power_6)
print("")

print("B в 14 степени")
B_power_14 = np.linalg.matrix_power(B, 14)
print(B_power_14)
print("")

a = 12
b = 8
variant = a % b
print(f"Мой вариант: {variant}")
print("")

print("Решение системы уравнений:")
A = np.array([[2.3, 0, -3.4, -12],
              [2.6, 8.4, 0, -6], 
              [1.3, 4.5, -17, 2], 
              [1.8, 0, 15, 16]])

B = np.array([-14, 0.4, -3.6, 17.4])

res = np.linalg.solve(A, B)

print("x1 =", res[0])
print("x2 =", res[1])
print("x3 =", res[2])
print("x4 =", res[3])
np.save('matrix_A.npy', A)