import tkinter as tk

import numpy as np


class Node:
    def __init__(
        self,
        pos: tuple[float, float],
        vel: tuple[float, float],
        maxvel: float = 10,
        m: float = 10,
        f=0.1,
        col="#ffffff",
    ):
        self.pos = complex(*pos)
        self.vel = complex(*vel)
        self.maxvel = maxvel
        self.m = m
        self.f = f
        self.col = col

    def update(self):
        if abs(self.vel) > self.maxvel:
            self.vel = self.vel / abs(self.vel) * self.maxvel
        self.vel *= 1 - self.f

        self.pos += self.vel

    def draw(self, canvas: tk.Canvas):
        x = self.pos.real
        y = self.pos.imag
        r = self.m
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        canvas.create_oval(x0, y0, x1, y1, fill=self.col, outline="")


class Spring:
    def __init__(
        self, a: Node, b: Node, k: float, c: float, r: float, name="", col="#ffffff"
    ):
        self.a = a
        self.b = b
        self.k = k
        self.r = r
        self.c = c
        self.col = col
        self.name = name
        self.last_disp = 0

    def update(self):
        dx = self.a.pos - self.b.pos
        dv = self.a.vel - self.b.vel
        mag = abs(dx)
        if mag == 0:
            self.b.pos += complex(0.00001, 0.00001)
            dx = self.b.pos - self.a.pos
            mag = abs(dx)
        atob = dx / mag

        disp = mag - self.r
        a_force = -self.k * disp * atob - dv * self.c
        a_accel = a_force / self.a.m
        b_accel = -a_accel

        self.a.vel += a_accel
        self.b.vel += b_accel

    def draw(self, canvas: tk.Canvas):
        a = self.a.pos
        b = self.b.pos
        x0, y0 = a.real, a.imag
        x1, y1 = b.real, b.imag
        xm = (x0 + x1) / 2
        ym = (y0 + y1) / 2
        canvas.create_line(x0, y0, x1, y1, fill=self.col)
        t = canvas.create_text(xm, ym, text=self.name, fill="#ffffff")
        b = canvas.create_rectangle(canvas.bbox(t), fill="#000000")
        canvas.tag_lower(b, t)


class Physics:
    def __init__(self, bounds: tuple[tuple[float, float], tuple[float, float]]):
        self.objs = []
        self.bounds = bounds

    def createNode(
        self,
        pos: tuple[float, float],
        vel: tuple[float, float],
        maxvel: float = 10,
        m: float = 10,
        f=0.1,
        col="#ffffff",
    ):
        node = Node(pos, vel, maxvel, m, f, col)
        self.objs.append(node)
        return node

    def createSpring(
        self,
        a: Node,
        b: Node,
        k: float = 0.1,
        c: float = 0.01,
        r: float = 20,
        name="",
        col="#ffffff",
    ):
        spring = Spring(a, b, k, c, r, name, col)
        self.objs.append(spring)
        return spring

    def update(self):
        for obj in self.objs:
            obj.update()

    def draw(self, canvas: tk.Canvas):
        canvas.delete("all")
        for obj in self.objs:
            obj.draw(canvas)


def setup_physics(verts, graph, mst, w=600, h=400):
    physics = Physics(bounds=((0, w), (0, h)))
    nodes = []
    for i in range(verts):
        pos = complex(1, 0)
        angle = 2 * np.pi * i / verts
        pos *= complex(np.cos(angle), np.sin(angle))
        x, y = pos.real * 100 + w / 2, pos.imag * 100 + h / 2
        node = physics.createNode(
            (x, y), (0, 0)
        )
        nodes.append(node)
    for i in range(verts):
        for j in range(i + 1, verts):
            w = graph[i, j]
            if w is None:
                continue
            if (i, j) in mst or (j, i) in mst:
                color = "#ff0000"
            else:
                color = "#333333"
            physics.createSpring(nodes[i], nodes[j], r=w * 20, name=str(w), col=color)
    return physics


if __name__ == "__main__":
    root = tk.Tk()
    physics = Physics(bounds=((0, 600), (0, 400)))
    nodes = []
    nodes.append(physics.createNode((20, 20), (0, 0), col="#ff0000"))
    nodes.append(physics.createNode((80, 80), (0, 0), col="#00ff00"))
    nodes.append(physics.createNode((100, 40), (0, 0), col="#0000ff"))
    physics.createSpring(nodes[0], nodes[1], 0.1, 0.01, 60, name="1")
    physics.createSpring(nodes[1], nodes[2], 0.1, 0.01, 80, name="2")
    physics.createSpring(nodes[0], nodes[2], 0.1, 0.01, 100, name="3")

    canvas = tk.Canvas(root, width=600, height=400, background="#000000")
    canvas.pack(padx=5, pady=5)

    def tick():
        physics.update()
        physics.draw(canvas)
        root.after(10, tick)

    root.after(10, tick)
    root.mainloop()
