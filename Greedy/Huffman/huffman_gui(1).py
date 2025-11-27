import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import Counter
import heapq
import os

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izq = None
        self.der = None

    # comparación para heapq
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol(frecuencias):
    heap = [NodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        nuevo = NodoHuffman(None, n1.frecuencia + n2.frecuencia)
        nuevo.izq = n1
        nuevo.der = n2
        heapq.heappush(heap, nuevo)

    return heap[0] if heap else None


def generar_codigos(nodo, codigo="", codigos={}):
    if nodo is None:
        return

    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo

    generar_codigos(nodo.izq, codigo + "0", codigos)
    generar_codigos(nodo.der, codigo + "1", codigos)
    return codigos


def codificar(texto, codigos):
    return ''.join(codigos[c] for c in texto)


def decodificar(codigo_binario, nodo_raiz):
    resultado = ""
    actual = nodo_raiz
    for bit in codigo_binario:
        actual = actual.izq if bit == "0" else actual.der
        if actual.caracter is not None:
            resultado += actual.caracter
            actual = nodo_raiz
    return resultado

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor Huffman")
        self.root.geometry("1000x700")

        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill="both", expand=True)

        ttk.Button(self.frame, text="Seleccionar archivo .txt", command=self.cargar_archivo).pack(pady=10)

        self.label_archivo = ttk.Label(self.frame, text="Archivo: (ninguno seleccionado)")
        self.label_archivo.pack(pady=5)

        ttk.Button(self.frame, text="Ejecutar Compresión", command=self.ejecutar_huffman).pack(pady=10)

        self.texto_resultados = tk.Text(self.frame, wrap="word", height=25)
        self.texto_resultados.pack(fill="both", expand=True)

        self.archivo_ruta = None
        self.codigos = {}
        self.arbol = None
        
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if ruta:
            self.archivo_ruta = ruta
            self.label_archivo.config(text=f"Archivo: {os.path.basename(ruta)}")

    def ejecutar_huffman(self):
        if not self.archivo_ruta:
            messagebox.showwarning("Advertencia", "Primero selecciona un archivo .txt")
            return

        with open(self.archivo_ruta, "r", encoding="utf-8") as f:
            texto = f.read()

        if not texto:
            messagebox.showwarning("Archivo vacío", "El archivo no contiene texto.")
            return

        frecuencias = Counter(texto)
        self.arbol = construir_arbol(frecuencias)
        self.codigos = generar_codigos(self.arbol)

        # Codificación
        texto_codificado = codificar(texto, self.codigos)
        texto_decodificado = decodificar(texto_codificado, self.arbol)

        # Mostrar resultados
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"Frecuencias de caracteres:\n{frecuencias}\n\n")
        self.texto_resultados.insert(tk.END, f"Códigos Huffman:\n{self.codigos}\n\n")
        self.texto_resultados.insert(tk.END, f"Texto codificado (primeros 200 bits):\n{texto_codificado[:200]}...\n\n")

        if texto == texto_decodificado:
            self.texto_resultados.insert(tk.END, "Decodificación correcta\n")
        else:
            self.texto_resultados.insert(tk.END, "Error en la decodificación\n")
            
        self.guardar_en_txt("resultado.txt", texto_codificado, self.codigos)

    def guardar_en_txt(self, nombre_archivo, texto_codificado, codigos):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            for c, codigo in codigos.items():
                f.write(f"'{c}': {codigo}\n")
        messagebox.showinfo("Guardado", f"Resultado guardado'")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
