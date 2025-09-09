import sys
import time
import numpy
from matplotlib import pyplot

from bigO import BigO

sys.setrecursionlimit(30000)

def generador(n) -> numpy.ndarray:
    return numpy.random.randint(0, 100, n)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        taken = end - start
        return (result, taken)
    return wrapper

def bubblesort(vectorbs):
    n = 0 # Establecemos un contador del largo del vector
    
    for _ in vectorbs:
        n += 1 #Contamos la cantidad de caracteres dentro del vector
    
    for i in range(n-1): 
    # Le damos un rango n para que complete el proceso. 
        for j in range(0, n-i-1): 
            # Revisa la matriz de 0 hasta n-i-1
            if vectorbs[j] > vectorbs[j+1] :
                vectorbs[j], vectorbs[j+1] = vectorbs[j+1], vectorbs[j]
            # Se intercambian si el elemento encontrado es mayor 
            # Luego pasa al siguiente

def mergesort(vectormerge): 
    def merge(vectormerge):
        if len(vectormerge) >1: 
            medio = len(vectormerge)//2 # Buscamos el medio del vector
            
            # Lo dividimos en 2 partes 
            izq = vectormerge[:medio]  
            der = vectormerge[medio:]
            
            merge(izq) # Mismo procedimiento a la primer mitad
            merge(der) # Mismo procedimiento a la segunda mitad
            
            i = j = k = 0
            
            # Copiamos los datos a los vectores temporales izq[] y der[] 
            while i < len(izq) and j < len(der): 
                if izq[i] < der[j]: 
                    vectormerge[k] = izq[i] 
                    i+= 1
                else: 
                    vectormerge[k] = der[j] 
                    j+= 1
                k += 1
            
            # Nos fijamos si quedaron elementos en la lista
            # tanto derecha como izquierda 
            while i < len(izq): 
                vectormerge[k] = izq[i] 
                i+= 1
                k+= 1
            
            while j < len(der): 
                vectormerge[k] = der[j] 
                j+= 1
                k+= 1
    merge(vectormerge)

# def quicksort(vectorquick):
#     def _quicksort(vectorquick, start, end):
        
#         def quick(vectorquick, start = 0, end = len(vectorquick) - 1):
            
            
#             if start >= end:
#                 return

#             def particion(vectorquick, start = 0, end = len(vectorquick) - 1):
#                 pivot = vectorquick[start]
#                 menor = start + 1
#                 mayor = end

#                 while True:
#                     # Si el valor actual es mayor que el pivot
#                     # está en el lugar correcto (lado derecho del pivot) y podemos 
#                     # movernos hacia la izquierda, al siguiente elemento.
#                     # También debemos asegurarnos de no haber superado el puntero bajo, ya que indica 
#                     # que ya hemos movido todos los elementos a su lado correcto del pivot
#                     while menor <= mayor and vectorquick[mayor] >= pivot:
#                         mayor = mayor - 1

#                     # Proceso opuesto al anterior            
#                     while menor <= mayor and vectorquick[menor] <= pivot:
#                         menor = menor + 1

#                     # Encontramos un valor sea mayor o menor y que este fuera del arreglo
#                     # ó menor es más grande que mayor, en cuyo caso salimos del ciclo
#                     if menor <= mayor:
#                         vectorquick[menor], vectorquick[mayor] = vectorquick[mayor], vectorquick[menor]
#                         # Continua el bucle
#                     else:
#                         # Salimos del bucle
#                         break

#                 vectorquick[start], vectorquick[mayor] = vectorquick[mayor], vectorquick[start]
                
#                 return mayor
            
#             p = particion(vectorquick, start, end)
#             quick(vectorquick, start, p-1)
#             quick(vectorquick, p+1, end)
            
#         quick(vectorquick)


#     return _quicksort(vectorquick, 0, len(vectorquick) - 1)

def quicksort(array):
    """Sort the array by using quicksort."""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array

@measure_time
def timed_sort(arr, sort) -> tuple[any, float]:
    return sort(arr)

def graph(results: dict):
    plot = pyplot.figure()
    ax = plot.add_subplot()
    ax.grid(visible=True, which="both", axis="both")
    ax.set_title("Algoritmos de ordenamiento")
    ax.set_xlabel("Tamaño de la lista")
    ax.set_ylabel("Tiempo de ejecución (segundos)")
    for name, values in results.items():
        xvalues = [v[0] for v in values]
        yvalues = [v[1] for v in values]
        ax.plot(xvalues, yvalues, label=name)
    ax.legend()
    plot.show()

lib = BigO()
stepsize = 50
sorts = bubblesort, mergesort, quicksort

results = {}
complexities= {}
for sort in sorts:
    complexity = lib.test(sort, "random", prtResult=False)
    label = f"{sort.__name__}: {complexity}"
    for n in range(0 + stepsize, 1000 + stepsize, stepsize):
        arr = generador(n)
        result, taken = timed_sort(arr, sort)
        if label not in results:
            results[label] = []
        results[label].append((n, taken))
    
for name, complexity in complexities.items():
    print(f"{name}: {complexity}")
graph(results)
input()