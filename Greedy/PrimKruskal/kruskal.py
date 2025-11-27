import numpy as np
from minheap import heap_insert, heap_top, heap_delete_min


def find(v, i):
    if v[i] == i:
        return i
    return find(v, v[i])


def union(v, i, j):
    i_rep = find(v, i)
    j_rep = find(v, j)
    v[i_rep] = j_rep


def kruskal(graph: np.ndarray):
    n = graph.shape[0]
    edges = []
    parent = np.arange(n)
    for i in range(0, n - 1):
        for j in range(i, n):
            w = graph[i, j]
            if w is None:
                continue
            heap_insert(edges, (w, (i, j)))

    mst = set()
    total_weight = 0
    while len(mst) < n - 1:
        w, verts = heap_top(edges)
        heap_delete_min(edges)
        i, j = verts
        i_rep = find(parent, i)
        j_rep = find(parent, j)
        if i_rep == j_rep:
            continue
        mst.add(verts)
        total_weight += w
        union(parent, i, j)
    return mst

if __name__ == "__main__":
    from physics import setup_physics
    import tkinter as tk

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

    mst = kruskal(graph)

    physics = setup_physics(verts, graph, mst)

    root = tk.Tk()
    canvas = tk.Canvas(root, width=600, height=400, background="#000000")
    canvas.pack(padx=5, pady=5)

    def tick():
        physics.update()
        physics.draw(canvas)
        root.after(10, tick)

    root.after(10, tick)
    root.mainloop()
