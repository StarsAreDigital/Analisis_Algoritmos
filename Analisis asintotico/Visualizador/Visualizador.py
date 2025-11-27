import tkinter as tk
from tkinter import ttk
import random
import time
import sys

sys.setrecursionlimit(30000)

# Parámetros generales
ANCHO = 800
ALTO = 300
N_BARRAS = 50
VAL_MIN, VAL_MAX = 5, 100
RETARDO_MS = 1  # velocidad de animación


# Algoritmo: Selection Sort
def selection_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_callback(activos=[i, j, min_idx])
            yield
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_callback(activos=[i, min_idx])
        yield
    draw_callback(activos=[])


# Algoritmo: Quick Sort
def partition(data, l, h):
    i = l - 1
    x = data[h]

    for j in range(l, h):
        if data[j] <= x:
            i = i + 1
            data[i], data[j] = data[j], data[i]

    data[i + 1], data[h] = data[h], data[i + 1]
    return i + 1


def quick_sort_steps(data, draw_callback):
    l = 0
    h = len(data) - 1
    stack = [0] * (len(data))

    top = -1

    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    while top >= 0:
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
        p = partition(data, l, h)
        draw_callback(activos=[l, h, p])
        yield
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
    draw_callback(activos=[])


# Algoritmo: Merge Sort
def merge(data, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    arr1 = data[left : left + n1]
    arr2 = data[mid + 1 : mid + 1 + n2]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if arr1[i] <= arr2[j]:
            data[k] = arr1[i]
            i += 1
        else:
            data[k] = arr2[j]
            j += 1
        k += 1
        yield [left + i, mid + j, k]

    while i < n1:
        data[k] = arr1[i]
        i += 1
        k += 1
        yield [left + i, k]

    while j < n2:
        data[k] = arr2[j]
        j += 1
        k += 1
        yield [mid + j, k]


def merge_sort_steps(data, draw_callback):
    n = len(data)

    currSize = 1
    while currSize <= n - 1:
        leftStart = 0
        while leftStart < n - 1:
            mid = min(leftStart + currSize - 1, n - 1)
            rightEnd = min(leftStart + 2 * currSize - 1, n - 1)
            for indexes in merge(data, leftStart, mid, rightEnd):
                draw_callback(activos=indexes)
                yield
            leftStart += 2 * currSize
        currSize = 2 * currSize
    draw_callback(activos=[])


# Algoritmo: Bubble Sort
def bubble_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        for j in range(0, n - 1):
            # draw_callback(activos=[data[j], data[j+1]]); yield
            if data[j] > data[j + 1]:
                aux = data[j]
                data[j] = data[j + 1]
                data[j + 1] = aux

            draw_callback(activos=[j, j + 1])
            yield
    draw_callback(activos=[])


# Función de dibujo
def dibujar_barras(canvas, datos, activos=None):
    canvas.delete("all")
    if not datos:
        return
    n = len(datos)
    margen = 10
    ancho_disp = ANCHO - 2 * margen
    alto_disp = ALTO - 2 * margen
    w = ancho_disp / n
    esc = alto_disp / max(datos)
    for i, v in enumerate(datos):
        x0 = margen + i * w
        x1 = x0 + w * 0.9
        h = v * esc
        y0 = ALTO - margen - h
        y1 = ALTO - margen
        color = "#4e79a7"
        if activos and i in activos:
            color = "#f28e2b"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
    canvas.create_text(6, 6, anchor="nw", text=f"n={len(datos)}", fill="#666")


# Aplicación principal
datos = []
root = tk.Tk()
root.title("Visualizador - Selection Sort")
canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="white")
canvas.pack(padx=10, pady=10)


def generar():
    global datos
    random.seed(time.time())
    n = n_entry.get()
    n = int(n) if n.isdecimal() else 10
    datos = [random.randint(VAL_MIN, VAL_MAX) for _ in range(n)]
    dibujar_barras(canvas, datos)


def mezclar():
    global datos
    random.shuffle(datos)
    dibujar_barras(canvas, datos)


def ordenar_selection():
    if not datos:
        return
    gen = selection_sort_steps(
        datos, lambda activos=None: dibujar_barras(canvas, datos, activos)
    )

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass

    paso()


def ordenar_quick():
    if not datos:
        return
    gen = quick_sort_steps(
        datos, lambda activos=None: dibujar_barras(canvas, datos, activos)
    )

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass

    paso()


def ordenar_merge():
    if not datos:
        return
    gen = merge_sort_steps(
        datos, lambda activos=None: dibujar_barras(canvas, datos, activos)
    )

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass

    paso()


def ordenar_bubble():
    if not datos:
        return
    gen = bubble_sort_steps(
        datos, lambda activos=None: dibujar_barras(canvas, datos, activos)
    )

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass

    paso()


def ordenar():
    if not datos:
        return
    match selected_algo.get():
        case "Selection":
            func = selection_sort_steps
        case "Bubble":
            func = bubble_sort_steps
        case "Quick":
            func = quick_sort_steps
        case "Merge":
            func = merge_sort_steps

    gen = func(datos, lambda activos=None: dibujar_barras(canvas, datos, activos))

    def paso():
        try:
            next(gen)
            delay = int(speed_slider.get())
            root.after(delay, paso)
        except StopIteration:
            pass

    paso()


panel = tk.Frame(root)
panel.pack(pady=6)
tk.Label(panel, text="n:").pack(side="left", padx=5)
n_entry = tk.Entry(panel)
n_entry.pack(side="left", padx=5)
tk.Button(panel, text="Generar", command=generar).pack(side="left", padx=5)
tk.Button(panel, text="Mezclar", command=mezclar).pack(side="left", padx=5)
selected_algo = ttk.Combobox(panel, values=["Selection", "Quick", "Merge", "Bubble"])
selected_algo.pack(side="left", padx=5)
speed_slider = ttk.Scale(panel, from_=5, to=100, orient="horizontal")
speed_slider.pack(side="left", padx=5)
tk.Button(panel, text="Ordenar", command=ordenar).pack(side="left", padx=5)
# tk.Button(panel, text="Ordenar (Selection)", command=ordenar_selection).pack(side="left", padx=5)
# tk.Button(panel, text="Ordenar (Quick)", command=ordenar_quick).pack(side="left", padx=5)
# tk.Button(panel, text="Ordenar (Merge)", command=ordenar_merge).pack(side="left", padx=5)
# tk.Button(panel, text="Ordenar (Bubble)", command=ordenar_bubble).pack(side="left", padx=5)


generar()
root.mainloop()
