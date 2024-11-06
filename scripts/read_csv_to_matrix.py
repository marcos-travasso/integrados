import numpy as np

a = np.loadtxt('../Dados/a.csv', delimiter=';').reshape(1, 10)
M = np.loadtxt('../Dados/M.csv', delimiter=';').reshape(10, 10)
N = np.loadtxt('../Dados/N.csv', delimiter=';').reshape(10, 10)

result = M @ a
# result = a @ M
# result = M @ N
print(result)
