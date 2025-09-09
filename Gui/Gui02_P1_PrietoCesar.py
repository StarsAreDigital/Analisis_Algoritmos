import tkinter as tk

def saludar():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"Hola Compa, {nombre} 👋")


def despedir():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"Adios, {nombre}")

def mayus():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"AAAAA, {nombre.upper()}")

def minus():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"aaaaa, {nombre.lower()}")

root = tk.Tk()
root.title("Saludador de Compas")
root.geometry("400x300")
root.tk_setPalette(background="#333")


lbl = tk.Label(root, text="Eh compa, Escribe tu nombre y presiona el botón")
lbl.pack(pady=20)

grupo = tk.Frame(root, )
label = tk.Label(grupo, text="Nombre:")
label.pack(padx=5)
entrada = tk.Entry(grupo)
entrada.pack(padx=5)
grupo.pack()


btn1 = tk.Button(root, text="Saludar", command=saludar, relief="ridge")
btn1.pack(pady=5)
btn2 = tk.Button(root, text="Despedir", command=despedir, relief="raised")
btn2.pack(pady=5)
btn3 = tk.Button(root, text="Mayúsculas", command=mayus, relief="solid")
btn3.pack(pady=5)
btn4 = tk.Button(root, text="Minúsculas", command=minus, relief="flat")
btn4.pack(pady=5)

root.mainloop()
