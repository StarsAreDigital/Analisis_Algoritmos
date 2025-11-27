import math
import numpy as np

from multiply_matrix import multiply_strassen
import tkinter as tk

HEIGHT = 300
WIDTH = 400
ASPECT_RATIO = WIDTH / HEIGHT

fov = 0.6
near = 0.5
far = 100
bottom = near * math.tan(fov / 2)
top = -bottom
right = ASPECT_RATIO * bottom
left = -right

PERSPECTIVE_MATRIX = np.array(
    [[near, 0, 0, 0], [0, near, 0, 0], [0, 0, far + near, -far * near], [0, 0, 1, 0]]
)
ORTOGRAOHIC_MATRIX = np.array(
    [
        [2 / (right - left), 0, 0, -(right + left) / (right - left)],
        [0, 2 / (bottom - top), 0, -(bottom + top) / (bottom - top)],
        [0, 0, 1 / (far - near), -near / (far - near)],
        [0, 0, 0, 1],
    ]
)
PROJECTION_MATRIX = multiply_strassen(ORTOGRAOHIC_MATRIX, PERSPECTIVE_MATRIX)


def affineObj(obj: np.ndarray):
    return np.pad(obj, ((0, 0), (0, 1)), constant_values=1).swapaxes(0, 1)


def translateXYZ(X: float = 0, Y: float = 0, Z: float = 0):
    return np.array([[1, 0, 0, X], [0, 1, 0, Y], [0, 0, 1, Z], [0, 0, 0, 1]])


def scaleXYZ(X: float = 1, Y: float = 1, Z: float = 1):
    return np.array([[X, 0, 0, 0], [0, Y, 0, 0], [0, 0, Z, 0], [0, 0, 0, 1]])


def rotateXYZ(alpha: float = 0, beta: float = 0, gamma: float = 0):
    yaw = np.array(
        [
            [np.cos(alpha), -np.sin(alpha), 0, 0],
            [np.sin(alpha), np.cos(alpha), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    pitch = np.array(
        [
            [np.cos(beta), 0, np.sin(beta), 0],
            [0, 1, 0, 0],
            [-np.sin(beta), 0, np.cos(beta), 0],
            [0, 0, 0, 1],
        ]
    )
    roll = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(gamma), -np.sin(gamma), 0],
            [0, np.sin(gamma), np.cos(gamma), 0],
            [0, 0, 0, 1],
        ]
    )
    return multiply_strassen(roll, multiply_strassen(pitch, yaw))


def toScreenSpace(obj: np.ndarray):
    temp = obj / obj[3]
    temp[3] = obj[3]
    temp[0] = np.interp(temp[0], (-1, 1), (0, WIDTH))
    temp[1] = np.interp(temp[1], (-1, 1), (0, HEIGHT))
    return temp


root = tk.Tk("Projection with matrix mult")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, background="#222222")
canvas.pack()


obj = np.array(
    [
        [0, 0, 0],  # 0
        [0, 0, 1],  # 1
        [0, 1, 0],  # 2
        [0, 1, 1],  # 3
        [1, 0, 0],  # 4
        [1, 0, 1],  # 5
        [1, 1, 0],  # 6
        [1, 1, 1],  # 7
    ]
)
edges = np.array([
    [0, 1],
    [0, 2],
    [0, 4],
    [1, 3],
    [1, 5],
    [2, 3],
    [2, 6],
    [3, 7],
    [4, 5],
    [4, 6],
    [5, 7],
    [6, 7],
])

obj = affineObj(obj)
obj = multiply_strassen(translateXYZ(-0.5, -0.5, 0), obj)
obj = multiply_strassen(rotateXYZ(np.pi / 6, 0, np.pi / 6), obj)
obj = multiply_strassen(translateXYZ(0, 0, 5), obj)
obj = multiply_strassen(PROJECTION_MATRIX, obj)
obj = toScreenSpace(obj)

for pair in edges:
    x0, y0, z0 = obj[0, pair[0]], obj[1, pair[0]], obj[3, pair[0]]
    x1, y1, z1 = obj[0, pair[1]], obj[1, pair[1]], obj[3, pair[1]]
    z = (z0 + z1) / 2
    print(z)
    c = "#%02x0000" % int(np.interp(z, (0.5, 10), (255, 0)))
    print(c)

    canvas.create_line(x0, y0, x1, y1, fill=c)

for vertex in obj.swapaxes(0, 1):
    x0 = vertex[0] - 2
    y0 = vertex[1] - 2
    x1 = vertex[0] + 2
    y1 = vertex[1] + 2
    canvas.create_oval(x0, y0, x1, y1, fill="#ffffff")

root.mainloop()
