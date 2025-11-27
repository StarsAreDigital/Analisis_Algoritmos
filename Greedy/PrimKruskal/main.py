import tkinter as tk
from prim import prim
from kruskal import kruskal
from physics import setup_physics
import numpy as np

if __name__ == "__main__":
    verts = int(input())
    edges = int(input())
    graph = np.full((verts, verts), None)
    for _ in range(edges):
        a, b, w = input().split()
        a = int(a)
        b = int(b)
        w = float(w)
        graph[a, b] = w
        graph[b, a] = w

    prim_mst = prim(graph, 0)
    kruskal_mst = kruskal(graph)

    prim_physics = setup_physics(verts, graph, prim_mst)
    kruskal_physics = setup_physics(verts, graph, kruskal_mst)

    root = tk.Tk()
    prim_canvas = tk.Canvas(root, width=600, height=400, background="#000000")
    prim_canvas.pack(padx=5, pady=5)
    kruskal_canvas = tk.Canvas(root, width=600, height=400, background="#000000")
    kruskal_canvas.pack(padx=5, pady=5)

    prim_physics.draw(prim_canvas)
    prim_canvas.create_text(10, 20, text="Prim", fill="#666666", anchor="w", font="24")
    kruskal_physics.draw(kruskal_canvas)
    kruskal_canvas.create_text(
        10, 20, text="Kruskal", fill="#666666", anchor="w", font="24"
    )
    root.mainloop()
