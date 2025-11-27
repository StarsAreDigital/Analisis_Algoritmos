import numpy as np
from minheap import heap_insert, heap_top, heap_delete_min


def prim(graph: np.ndarray, starting: int):
    n = graph.shape[0]
    visited = {starting}
    total_weight = 0
    mst = set()
    heap = []
    for i in range(n):
        if graph[starting, i] is None:
            continue
        heap_insert(heap, (graph[starting, i], (starting, i)))

    while len(visited) < n:
        w, verts = heap_top(heap)
        heap_delete_min(heap)
        to = verts[1]
        if to in visited:
            continue
        mst.add(verts)
        visited.add(to)
        total_weight += w
        for i in range(n):
            if graph[to, i] is not None:
                heap_insert(heap, (graph[to, i], (to, i)))

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

    mst = prim(graph, 0)

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
