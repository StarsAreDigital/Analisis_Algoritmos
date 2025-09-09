import os
import time
import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot, use

use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algorithms


class App:
    MAX_10_POWER = 6
    NUMS_PER_LINE = 10

    def generate(self):
        self.arr = algorithms.generate(self.selected_size.get())
        self.linear_search_btn.config(state="normal")
        self.binary_search_btn.config(state="normal")
        with open(self.arr_path, "w") as file:
            file.writelines(
                ", ".join(str(i) for i in self.arr[i : i + self.NUMS_PER_LINE]) + "\n"
                for i in range(0, len(self.arr), self.NUMS_PER_LINE)
            )

    def graph_results(self):
        values_linear = [
            (x, sum(self.linear_results[x]) / len(self.linear_results[x]))
            for x in self.value_indexes
            if len(self.linear_results[x])
        ]
        values_binary = [
            (x, sum(self.binary_results[x]) / len(self.binary_results[x]))
            for x in self.value_indexes
            if len(self.binary_results[x])
        ]
        values_linear_x = [v[0] for v in values_linear]
        values_linear_y = [v[1] for v in values_linear]
        values_binary_x = [v[0] for v in values_binary]
        values_binary_y = [v[1] for v in values_binary]
        print("linear", values_linear)
        print("binary", values_binary)

        self.ax.clear()
        self.ax.grid(visible=True, which="both", axis="both")
        self.ax.plot(values_linear_x, values_linear_y, "ro-", label="lineal")
        self.ax.plot(values_binary_x, values_binary_y, "bo-", label="binaria")
        self.ax.set_title("Tiempos de búsqueda")
        self.ax.set_xscale("log")
        self.ax.set_xlabel("Tamaño del arreglo")
        self.ax.set_yscale("log")
        self.ax.set_ylabel("Tiempo de ejecución (microsegundos)")
        self.ax.legend(loc="upper left")
        self.scatter.draw()

    def linear_search(self):
        if self.arr is None:
            self.search_result_label.config(text="No se han generado elementos")
            return

        try:
            target = self.target.get()
        except Exception:
            self.search_result_label.config(text="No puede estar vacío")
            return

        self.search_result_label.config(text="")
        start = time.perf_counter()
        result = algorithms.linear_search(target, self.arr)
        end = time.perf_counter()
        taken = (end - start) * 1e3  # milisegundos

        if result == -1:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"No se encontró el valor {target}")
        else:
            size = self.selected_size.get()
            self.linear_results[size].append(taken)

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(
                "1.0",
                f"Encontrado en la posición {result}\n"
                + f"Tiempo total: {taken}ms\n"
                + f"Minimo: {min(self.linear_results[size])}ms\n"
                + f"Maximo: {max(self.linear_results[size])}ms\n"
                + f"Media: {sum(self.linear_results[size]) / len(self.linear_results[size])}ms\n",
            )
        self.graph_results()

    def binary_search(self):
        if self.arr is None:
            self.search_result_label.config(text="No se han generado elementos")
            return

        try:
            target = self.target.get()
        except Exception:
            self.search_result_label.config(text="No puede estar vacío")
            return

        self.search_result_label.config(text="")
        sorted_arr = algorithms.return_sorted(self.arr)
        start = time.perf_counter()
        result = algorithms.binary_search(target, sorted_arr)
        end = time.perf_counter()
        taken = (end - start) * 1e3  # milisegundos

        if result == -1:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"No se encontró el valor {target}")
        else:
            size = self.selected_size.get()
            self.binary_results[size].append(taken)

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(
                "1.0",
                f"Encontrado en la posición {result}\n"
                f"Tiempo total: {taken}s\n"
                f"Minimo: {min(self.binary_results[size])}\n"
                f"Maximo: {max(self.binary_results[size])}\n"
                f"Media: {sum(self.binary_results[size]) / len(self.binary_results[size])}\n",
            )
        self.graph_results()

    def validate_input(self, entry: str):
        return entry.isdigit() or entry == ""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Comparacion busqueda lineal y binaria")

        self.arr = None
        self.selected_size = tk.IntVar(self.root)
        self.target = tk.IntVar(self.root)

        self.arr_path = os.path.join(os.path.dirname(__file__), "data.txt")
        self.value_indexes = [pow(10, i) for i in range(1, self.MAX_10_POWER)]
        self.linear_results = {i: [] for i in self.value_indexes}
        self.binary_results = {i: [] for i in self.value_indexes}

        input_frame = tk.Frame(self.root)
        input_frame.pack(side="left", padx=10)

        # region Generar lista
        generate_frame = tk.Frame(input_frame)
        generate_frame.pack(side="top", anchor="w")

        generate_label = tk.Label(generate_frame, text="Generar lista de numeros:")
        generate_label.pack(side="left")

        generate_select_size = ttk.Combobox(
            generate_frame,
            values=self.value_indexes,
            textvariable=self.selected_size,
            state="readonly",
            width=self.MAX_10_POWER,
        )
        generate_select_size.current(0)
        generate_select_size.pack(side="left")

        self.generate_button = tk.Button(
            generate_frame, text="Generar", command=self.generate
        )
        self.generate_button.pack(side="left")
        # endregion

        # region Buscar valor
        search_frame = tk.Frame(input_frame)
        search_frame.pack(side="top", anchor="w")

        search_label = tk.Label(search_frame, text="Buscar: ")
        search_label.pack(side="left")

        validate_input_fn = self.root.register(self.validate_input)
        search_value_entry = tk.Entry(
            search_frame,
            validate="all",
            validatecommand=(validate_input_fn, "%P"),
            textvariable=self.target,
        )
        search_value_entry.pack(side="left")

        self.linear_search_btn = tk.Button(
            search_frame, text="Lineal", command=self.linear_search, state="disabled"
        )
        self.linear_search_btn.pack(side="left")

        self.binary_search_btn = tk.Button(
            search_frame, text="Binaria", command=self.binary_search, state="disabled"
        )
        self.binary_search_btn.pack(side="left")

        self.search_result_label = tk.Label(search_frame, fg="red")
        self.search_result_label.pack(side="left")
        # endregion

        # region Resultados
        result_label = tk.Label(input_frame, text="Resultados")
        result_label.pack(side="top", anchor="w")

        self.result_text = tk.Text(input_frame, font="consolas", width=40, height=10)
        self.result_text.pack(side="top", anchor="w")
        # endregion

        # region Grafica
        results_frame = tk.Frame(self.root)
        results_frame.pack(side="right")

        self.fig = pyplot.figure()
        self.scatter = FigureCanvasTkAgg(self.fig, results_frame)
        self.scatter.get_tk_widget().pack(side="right", fill="both", expand=1)
        self.ax = self.fig.add_subplot()
        
        self.ax.clear()
        self.ax.grid(visible=True, which="both", axis="both")
        self.ax.set_title("Tiempos de búsqueda")
        self.ax.set_xscale("log")
        self.ax.set_xlabel("Tamaño del arreglo")
        self.ax.set_yscale("log")
        self.ax.set_ylabel("Tiempo de ejecución (microsegundos)")
        self.scatter.draw()

        # endregion

        self.root.mainloop()
