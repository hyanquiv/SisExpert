import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DiagnosticoEnfermedad:
    def __init__(self, master):
        self.master = master
        self.master.title("Diagnóstico de Enfermedades")
        self.master.geometry("800x600")

        self.enfermedades = self.cargar_base_conocimientos("base_conocimientos.txt")
        self.sintomas_preguntados = []
        self.respuestas = {}
        self.enfermedad_diagnostico = None

        # Crear los frames
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.frame_sintomas = tk.Frame(master)
        self.frame_sintomas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_grafico = tk.Frame(master)
        self.frame_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear los widgets en el frame de botones
        self.label = tk.Label(self.frame_botones, text="¿Tiene alguno de estos síntomas?")
        self.label.pack(pady=10)

        self.boton_si = tk.Button(self.frame_botones, text="Sí", command=lambda: self.responder('si'))
        self.boton_si.pack(side=tk.LEFT, padx=20, pady=20)

        self.boton_no = tk.Button(self.frame_botones, text="No", command=lambda: self.responder('no'))
        self.boton_no.pack(side=tk.RIGHT, padx=20, pady=20)

        # Crear el área de texto para mostrar los síntomas
        self.text_sintomas = tk.Text(self.frame_sintomas, wrap=tk.WORD, width=50)
        self.text_sintomas.pack(fill=tk.BOTH, expand=True)

        self.sintoma_actual = None
        self.proximo_sintoma()

        # Inicializar la figura del gráfico en el frame de gráficos
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def cargar_base_conocimientos(self, archivo):
        enfermedades = defaultdict(list)
        with open(archivo, 'r') as file:
            for linea in file:
                if ':' in linea:
                    enfermedad, sintomas = linea.split(':')
                    enfermedades[enfermedad.strip()] = [sintoma.strip() for sintoma in sintomas.split(',')]
                else:
                    print(f"Línea mal formateada ignorada: {linea}")
        return enfermedades

    def proximo_sintoma(self):
        todos_sintomas = [sintoma for sintomas in self.enfermedades.values() for sintoma in sintomas]
        sintomas_restantes = list(set(todos_sintomas) - set(self.sintomas_preguntados))
        if sintomas_restantes:
            self.sintoma_actual = sintomas_restantes[0]
            self.label.config(text=f"¿Tiene {self.sintoma_actual.replace('_', ' ')}?")
        else:
            self.diagnosticar()

    def responder(self, respuesta):
        self.sintomas_preguntados.append(self.sintoma_actual)
        self.respuestas[self.sintoma_actual] = respuesta
        self.proximo_sintoma()
        self.actualizar_grafico()

    def diagnosticar(self):
        self.puntajes = defaultdict(int)
        for sintoma, respuesta in self.respuestas.items():
            if respuesta == 'si':
                for enfermedad, sintomas in self.enfermedades.items():
                    if sintoma in sintomas:
                        self.puntajes[enfermedad] += 1

        if self.puntajes:
            self.enfermedad_diagnostico = max(self.puntajes, key=self.puntajes.get)
            sintomas_diagnostico = [sintoma.replace('_', ' ') for sintoma, respuesta in self.respuestas.items() if respuesta == 'si' and sintoma in self.enfermedades[self.enfermedad_diagnostico]]
            sintomas_no_diagnostico = [sintoma.replace('_', ' ') for sintoma, respuesta in self.respuestas.items() if respuesta == 'si' and sintoma not in self.enfermedades[self.enfermedad_diagnostico]]
            self.label.config(text=f"Diagnóstico: {self.enfermedad_diagnostico.replace('_', ' ')}")

            # Mostrar los síntomas en el área de texto
            self.text_sintomas.insert(tk.END, f"Diagnóstico: {self.enfermedad_diagnostico.replace('_', ' ')}\n")
            self.text_sintomas.insert(tk.END, "Síntomas que ayudaron al diagnóstico:\n")
            for sintoma in sintomas_diagnostico:
                self.text_sintomas.insert(tk.END, f" - {sintoma}\n")
            self.text_sintomas.insert(tk.END, "Otros síntomas marcados con 'Sí':\n")
            for sintoma in sintomas_no_diagnostico:
                self.text_sintomas.insert(tk.END, f" - {sintoma}\n")
        else:
            self.label.config(text="No se pudo determinar la enfermedad con los síntomas proporcionados.")
            self.text_sintomas.insert(tk.END, "No se pudo determinar la enfermedad con los síntomas proporcionados.\n")

        self.boton_si.pack_forget()
        self.boton_no.pack_forget()
        tk.Button(self.frame_botones, text="Salir", command=self.master.quit).pack(pady=20)

    def actualizar_grafico(self):
        if not hasattr(self, 'puntajes'):
            return

        self.ax.clear()
        enfermedades = list(self.puntajes.keys())
        puntajes = list(self.puntajes.values())

        self.ax.barh(enfermedades, puntajes, color='skyblue')
        self.ax.set_xlabel('Puntaje')
        self.ax.set_ylabel('Enfermedad')
        self.ax.set_title('Puntaje de Diagnóstico por Enfermedad')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosticoEnfermedad(root)
    root.mainloop()
