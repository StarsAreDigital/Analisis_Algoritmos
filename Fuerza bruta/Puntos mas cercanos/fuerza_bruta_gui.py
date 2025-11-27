import math
import random
import tkinter as tk

ANCHO = 600
ALTO = 400
MARGEN = 50
RADIO = 2
MIN_POINT = 0
MAX_POINT = 40
N = 5


class Point:
    x = 0
    y = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def dist(a: Point, b: Point):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.sqrt(dx * dx + dy * dy)


def lerp(low: float, high: float, t: float):
    return low + (high - low) * t


def get_points():
    global entries
    return [Point(float(x.get()), float(y.get())) for x, y in entries]


def draw_points():
    global entries, canvas
    canvas.delete("all")

    points = get_points()

    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    dx = max_x - min_x
    dy = max_y - min_y
    scaling = max(dx, dy)

    for i, point in enumerate(points, 1):
        px = lerp(MARGEN, ANCHO - 2 * MARGEN, (point.x - min_x) / scaling)
        py = lerp(ALTO - 2 * MARGEN, MARGEN, (point.y - min_y) / scaling)
        canvas.create_oval(px - RADIO, py - RADIO, px + RADIO, py + RADIO)
        canvas.create_text(px + 3 * RADIO, py + 3 * RADIO, text=f"P{i}")


def find_closest_points():
    global entries, canvas

    points = get_points()

    draw_points()

    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    dx = max_x - min_x
    dy = max_y - min_y
    scaling = max(dx, dy)

    min_dist = float("Inf")
    closest_points = (None, None)
    indexes = (None, None)
    found = False
    for i, a in enumerate(points, 1):
        for j, b in enumerate(points, 1):
            if i >= j:
                continue
            d = dist(a, b)
            if d < min_dist:
                min_dist = d
                closest_points = (a, b)
                indexes = (i, j)
                found = True
    if not found:
        return

    a, b = closest_points

    a_dx = (a.x - min_x) / scaling
    a_x = lerp(MARGEN, ANCHO - 2 * MARGEN, a_dx)

    a_dy = (a.y - min_y) / scaling
    a_y = lerp(ALTO - 2 * MARGEN, MARGEN, a_dy)

    b_dx = (b.x - min_x) / scaling
    b_x = lerp(MARGEN, ANCHO - 2 * MARGEN, b_dx)

    b_dy = (b.y - min_y) / scaling
    b_y = lerp(ALTO - 2 * MARGEN, MARGEN, b_dy)

    canvas.create_text(
        ANCHO / 2,
        MARGEN / 2,
        text=f"Los puntos mas cercanos son P{indexes[0]} a P{indexes[1]} (d = {round(min_dist, 4)})",
    )
    canvas.create_line(a_x, a_y, b_x, b_y, fill="red")


def clear_entries():
    global entries
    for entry in entries:
        x = entry[0]
        x_len = len(x.get())
        y = entry[1]
        y_len = len(y.get())

        x.delete(0, x_len)
        y.delete(0, y_len)


def generate():
    global entries
    clear_entries()
    for entry in entries:
        x = entry[0]
        y = entry[1]

        x.insert(0, random.randint(MIN_POINT, MAX_POINT))
        y.insert(0, random.randint(MIN_POINT, MAX_POINT))


root = tk.Tk()
panel = tk.Frame(root)
panel.pack(padx=6, pady=6)

input_panel = tk.Frame(panel)
input_panel.pack(padx=6, pady=6)

points_panel = tk.Frame(input_panel)
points_panel.pack(side="left", padx=6, pady=6)

points_labels_panel = tk.Frame(points_panel)
points_labels_panel.pack(side="top", pady=6)

entries: list[tuple[tk.Entry, tk.Entry]] = []
generate()
for i in range(N):
    temp_panel = tk.Frame(points_panel)
    temp_panel.pack(pady=6)

    tk.Label(temp_panel, text=f"P{i + 1}").pack(side="left", padx=6)
    x_entry = tk.Entry(temp_panel)
    x_entry.pack(side="left", padx=6)
    y_entry = tk.Entry(temp_panel)
    y_entry.pack(side="left", padx=6)
    entries.append((x_entry, y_entry))

buttons_panel = tk.Frame(input_panel)
buttons_panel.pack(side="left", padx=6, pady=6)

tk.Button(buttons_panel, text="Generar", command=generate).pack(pady=6)
tk.Button(buttons_panel, text="Limpiar", command=clear_entries).pack(pady=6)
tk.Button(buttons_panel, text="Calcular", command=find_closest_points).pack(pady=6)

canvas = tk.Canvas(panel, width=ANCHO, height=ALTO, bg="white")
canvas.pack(padx=6, pady=6)

root.mainloop()
