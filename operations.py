import math


def multiply_matrices(matrix1: list[list], matrix2: list[list]) -> list[list]:
    new_matrix = []
    row = []
    count_row = len(matrix1)
    count_column1 = len(matrix1[0])
    count_column2 = len(matrix2[0])
    expr = 0
    for k in range(count_row):
        for i in range(count_column2):
            for j in range(count_column1):
                expr += matrix1[k][j] * matrix2[j][i]
            row.append(expr)
            expr = 0
        new_matrix.append(row)
        row = []
    return new_matrix


# матрица поворота вокруг оси
def get_axis_rotation_matrix(axis: str, f: float) -> list[list]:
    try:
        matrixOX = [[1, 0, 0], [0, math.cos(f), math.sin(f) * -1], [0, math.sin(f), math.cos(f)]]
        matrixOY = [[math.cos(f), 0, math.sin(f)], [0, 1, 0], [-1 * math.sin(f), 0, math.cos(f)]]
        matrixOZ = [[math.cos(f), -1 * math.sin(f), 0], [math.sin(f), math.cos(f), 0], [0, 0, 1]]
        axes = {"ox": matrixOX, "oy": matrixOY, "oz": matrixOZ}
        return axes[axis.lower()]
    except KeyError:
        print("Параметр оси указан неверно")


# гомотетия (растяжение)
def stretching(axis: str, k: float, matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]) -> list[list]:
    axes = {"ox": 0, "oy": 1, "oz": 2}
    print(k)
    try:
        index = axes[axis.lower()]
        for i in range(len(matrix)):
            matrix[index][i] *= k
    except KeyError:
        print("Параметр оси указан неверно")
    except IndexError:
        print("Матрица не содержит указанной оси")
    return matrix


# поворот относительно оси
def axis_rotation(axis: str, f: float, matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]) -> list[list]:
    f = math.radians(f)  # перевод градусов в радианы
    # матрицы поворота
    matrixOX = [[1, 0, 0], [0, round(math.cos(f), 3), round(math.sin(f), 3) * -1], [0, round(math.sin(f), 3), round(math.cos(f), 3)]]
    matrixOY = [[round(math.cos(f), 3), 0, round(math.sin(f), 3)], [0, 1, 0], [-1 * round(math.sin(f), 3), 0, round(math.cos(f), 3)]]
    matrixOZ = [[round(math.cos(f), 3), -1 * round(math.sin(f), 3), 0], [round(math.sin(f), 3), round(math.cos(f), 3), 0], [0, 0, 1]]
    axes = {"ox": matrixOX, "oy": matrixOY, "oz": matrixOZ}
    try:
        axis = axes[axis.lower()]
        matrix = multiply_matrices(axis, matrix)
    except KeyError:
        print("Параметр оси неверно указан")
    except IndexError:
        print("Матрица не содержит указанной оси")
    return matrix


# проекция на плоскость
def projection(axis: str, matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]) -> list[list]:
    # занулить строку
    axes = {"ox": 0, "oy": 1, "oz": 2}
    try:
        index = axes[axis.lower()]
        for i in range(len(matrix)):
            matrix[index][i] = 0
    except KeyError:
        print("Параметр оси указан неверно")
    except IndexError:
        print("Матрица не содержит указанной оси")
    return matrix
