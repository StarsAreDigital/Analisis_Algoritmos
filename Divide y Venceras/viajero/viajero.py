nodos = {
    'a': {'b': 2, 'c': 5, 'd': 7},
    'b': {'a': 2, 'c': 8, 'd': 3},
    'c': {'a': 5, 'b': 8, 'd': 1},
    'd': {'a': 7, 'b': 3, 'c': 1}
}

def recorridos_desde(inicial):
    visitados = set()
    caminos = []
    def _recorrer(actual, camino):
        visitados.add(actual)
        
        if len(camino) == len(nodos): # Si ya recorriste todos agrega el camino
            caminos.append(camino.copy())
        else:
            for nodo in nodos[actual].keys():
                if nodo in visitados:
                    continue # recorre los siguientes nodos sin visitar
                _recorrer(nodo, [*camino, nodo])
        
        visitados.remove(actual)
    
    _recorrer(inicial, [inicial])
    caminos = [[*camino, inicial] for camino in caminos] # cierra los ciclos con el nodo inicial
    return caminos

min_peso = 1e10
min_recorrido = None
inicial = input("Nodo inicial: ")
for recorrido in recorridos_desde(inicial):
    peso = 0
    for i in range(len(recorrido) - 1):
        origen = recorrido[i]
        destino = recorrido[i + 1]
        peso += nodos[origen][destino]
    if peso < min_peso:
        min_peso = peso
        min_recorrido = recorrido
print('El camino más eficiente es: %s (longitud %d)' % (' -> '.join(min_recorrido), min_peso))