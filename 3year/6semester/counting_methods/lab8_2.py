import numpy as np
from scipy.linalg import solve

a = 0.8
b = 1.1
h = 0.1
n = int((b - a)/h) + 1

x = np.arange(a, b + h/2, h)
N = len(x) - 1

A = np.zeros((N+1, N+1))
d = np.zeros(N+1)

p = lambda x: 2/x
q = lambda x: -3
f = lambda x: 2

A[0, 0] = -1/h
A[0, 1] = 1/h
d[0] = 1.5

A[N, N-1] = -1/h
A[N, N]   = 1/h
d[N] = 3

for k in range(1, N):
    xk = x[k]
    A[k, k-1] = 1/h**2 - p(xk)/(2*h)
    A[k, k]   = -2/h**2 + q(xk)
    A[k, k+1] = 1/h**2 + p(xk)/(2*h)
    d[k] = f(xk)

y = solve(A, d)

print("x\t\ty")
for xi, yi in zip(x, y):
    print(f"{xi:.2f}\t\t{yi:.6f}")