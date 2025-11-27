import numpy as np
import tkinter as tk


def tsp(costs):
    # Funcion para generar todas las permutaciones de una lista, en este caso de ciudades
    def perms(n, A):
        if n == 1:
            yield A
        else:
            for i in range(n - 1):
                for hp in perms(n - 1, A):
                    yield hp
                j = 0 if (n % 2) == 1 else i
                A[j], A[n - 1] = A[n - 1], A[j]
            for hp in perms(n - 1, A):
                yield hp

    # Se genera una lista de ciudades excepto la ciudad 0
    n = len(costs)
    paths = list(range(1, n))
    best_cost = float("inf")
    best_path = [0]
    # Se realizan las permutaciones de esta lista, agregando que debe iniciar y comenzar en la ciudad 0
    for _path in perms(n - 1, paths):
        path = [0, *_path, 0]
        # Se agregan las longitudes de viajar entre cada ciudad del camino
        length = 0
        for i in range(n):
            length += costs[path[i], path[i + 1]]
        # Se compara la longitud del camino generado con el mejor camino posible, y se toma la menor
        if length < best_cost:
            best_cost = length
            best_path = path
    return best_path, best_cost


if __name__ == "__main__":
    # El conjunto de ciudades es una cantidad aleatoria entre 4 y 8
    # Sus coordenadas se encuentran entre (50, 50) y (150, 150) para poder visualizarlas
    n = np.random.randint(4, 9)
    cities = np.random.randint(50, 150, (n, 2))

    # El costo de viajar entre ciudades se representa mediante la distancia euclideana entre sus coordenadas
    # Se utiliza una matriz de adyacencia para representar las distancias entre cada par de ciudades
    cost = np.zeros((n, n))
    for i in range(n - 1):
        for j in range(i, n):
            i_pos = complex(*cities[i])
            j_pos = complex(*cities[j])
            dist = abs(i_pos - j_pos)
            cost[i, j] = cost[j, i] = dist

    path, distance = tsp(cost)
    print(f"ciudades:\n{cities}")
    print(f"distancia: {distance}")
    print(f"camino tomado: {path}")

    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200, background="black")
    canvas.pack(padx=5, pady=5)

    # Codigo para mostrar visualmente las ciudades y la mejor ruta tomada
    for i in range(len(path) - 1):
        city0 = cities[path[i]]
        city1 = cities[path[i + 1]]
        x0, y0 = city0
        x1, y1 = city1
        canvas.create_line(x0, y0, x1, y1, fill="red")

    for i in range(len(cities)):
        city = cities[i]
        x0, y0 = city - 6
        x1, y1 = city + 6
        canvas.create_oval(x0, y0, x1, y1, fill="white", outline="")
        canvas.create_text(*city, text=str(i))

    root.mainloop()
