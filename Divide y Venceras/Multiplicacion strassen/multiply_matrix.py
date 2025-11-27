import math
import time

import numpy as np
from matplotlib import pyplot as plt


def nextPow2(n: int):
    return int(math.pow(2, math.ceil(math.log2(n))))


def resizeMat(mat: np.ndarray, rows: int, cols: int):
    pad_width = ((0, rows - mat.shape[0]), (0, cols - mat.shape[1]))
    return np.pad(mat, pad_width)


def strassen(mat1: np.ndarray, mat2: np.ndarray):
    n = mat1.shape[0]
    res = np.zeros((n, n))
    if n == 1:
        res[0][0] = mat1[0][0] * mat2[0][0]
        return res
    if not np.any(mat1) or not np.any(mat2):
        return res

    h = n // 2
    a11 = mat1[:h, :h]
    a12 = mat1[:h, h:]
    a21 = mat1[h:, :h]
    a22 = mat1[h:, h:]

    b11 = mat2[:h, :h]
    b12 = mat2[:h, h:]
    b21 = mat2[h:, :h]
    b22 = mat2[h:, h:]

    m1 = strassen((a11 + a22), (b11 + b22))
    m2 = strassen((a21 + a22), b11)
    m3 = strassen(a11, (b12 - b22))
    m4 = strassen(a22, (b21 - b11))
    m5 = strassen((a11 + a12), b22)
    m6 = strassen((a21 - a11), (b11 + b12))
    m7 = strassen((a12 - a22), (b21 + b22))

    c11 = m1 + m4 - m5 + m7
    c12 = m3 + m5
    c21 = m2 + m4
    c22 = m1 - m2 + m3 + m6

    res = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

    return res


def multiply_strassen(mat1: np.ndarray, mat2: np.ndarray):
    n = mat1.shape[0]
    m = mat1.shape[1]
    q = mat2.shape[1]
    size = nextPow2(max(n, m, q))

    mat1_pad = resizeMat(mat1, size, size)
    mat2_pad = resizeMat(mat2, size, size)

    res_pad = strassen(mat1_pad, mat2_pad)
    res = res_pad[:n, :q]

    return res


def multiply_brute_force(mat1: np.ndarray, mat2: np.ndarray):
    n = mat1.shape[0]
    m = mat1.shape[1]
    q = mat2.shape[1]

    res = np.zeros((n, q))
    for i in range(n):
        for j in range(q):
            for k in range(m):
                res[i][j] += mat1[i][k] * mat2[k][j]
    return res


def hybrid_strassen(mat1: np.ndarray, mat2: np.ndarray):
    N0 = 1024
    n = mat1.shape[0]
    if n < N0:
        return multiply_brute_force(mat1, mat2)
    return strassen(mat1, mat2)


def multiply_hybrid(mat1: np.ndarray, mat2: np.ndarray):
    n = mat1.shape[0]
    m = mat1.shape[1]
    q = mat2.shape[1]
    size = nextPow2(max(n, m, q))

    mat1_pad = resizeMat(mat1, size, size)
    mat2_pad = resizeMat(mat2, size, size)

    res_pad = hybrid_strassen(mat1_pad, mat2_pad)
    res = res_pad[:n, :q]

    return res


if __name__ == "__main__":
    N = 100
    x = list(range(1, N + 1))
    times_strassen = []
    times_brute_force = []
    times_hybrid = []
    for i in x:
        print(i)
        mat1 = np.random.randint(-N, N + 1, (i, i))
        mat2 = np.random.randint(-N, N + 1, (i, i))

        # start = time.perf_counter()
        # _ = multiply_strassen(mat1, mat2)
        # end = time.perf_counter()
        # times_strassen.append(end - start)

        start = time.perf_counter()
        _ = multiply_brute_force(mat1, mat2)
        end = time.perf_counter()
        times_brute_force.append(end - start)

        start = time.perf_counter()
        _ = multiply_hybrid(mat1, mat2)
        end = time.perf_counter()
        times_hybrid.append(end - start)

    ax = plt.axes()
    # ax.plot(x, times_strassen, "r")
    ax.plot(x, times_brute_force, "g")
    ax.plot(x, times_hybrid, "b")
    plt.show()
