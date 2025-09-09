import tkinter as tk

def size():
    lbl.config(font=("Helvetica", 100))

root = tk.Tk()
root.title("Mi primera GUI")
root.geometry("360x200")

lbl = tk.Label(root, text="¡Hola, GUI!")
lbl.pack(pady=10)

btn = tk.Button(root, text="Tamaño", command=size)
btn.pack()

root.mainloop()
