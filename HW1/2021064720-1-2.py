import numpy as np

M = np.arange(2, 27)
print(M)

M = M.reshape(5, 5)
print(M)

M[1:4, 1:4] = 0
print(M)

M = M @ M
print(M)

v = M[0]
print(np.sqrt(v @ v))
