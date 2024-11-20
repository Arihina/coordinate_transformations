from pprint import pprint

import operations

k = 4
f = 60  # в градусах
By = operations.stretching('oy', k)
pprint(By)
Gz = operations.axis_rotation('oz', f)
pprint(Gz)
Axy = operations.projection('oz')
pprint(Axy)
T = operations.multiply_matrices(operations.multiply_matrices(By, Gz), Axy)
print("Матрица преобразований")
pprint(T)
