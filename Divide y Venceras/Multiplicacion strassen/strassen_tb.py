from multiply_matrix import multiply_strassen
import numpy as np

if __name__ == "__main__":
    n, m, q = np.random.randint(1, 10, 3)
    mat1 = np.random.randint(-100, 100 + 1, (n, m))
    mat2 = np.random.randint(-100, 100 + 1, (m, q))
    print("A:")
    print(mat1)
    print("B:")
    print(mat2)
    print("A * B:")
    print(multiply_strassen(mat1, mat2))
