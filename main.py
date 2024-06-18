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
        self.sintomas_ingresados = []
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
        self.label = tk.Label(self.frame_botones, text="Ingrese sus síntomas (separados por comas):")
        self.label.pack(pady=10)

        self.entrada_sintomas = tk.Entry(self.frame_botones, width=50)
        self.entrada_sintomas.pack(pady=10)

        self.boton_diagnosticar = tk.Button(self.frame_botones, text="Diagnosticar", command=self.diagnosticar_manual)
        self.boton_diagnosticar.pack(pady=20)

        # Crear el área de texto para mostrar los síntomas y diagnóstico
        self.text_sintomas = tk.Text(self.frame_sintomas, wrap=tk.WORD, width=50)
        self.text_sintomas.pack(fill=tk.BOTH, expand=True)

        # Inicializar la figura del gráfico en el frame de gráficos
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Botón "Nuevo Diagnóstico" inicial, pero lo ocultamos
        self.boton_nuevo_diagnostico = tk.Button(self.frame_botones, text="Nuevo Diagnóstico", command=self.nuevo_diagnostico)
        self.boton_nuevo_diagnostico.pack(pady=20)
        self.boton_nuevo_diagnostico.pack_forget()

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

    def diagnosticar_manual(self):
        sintomas_usuario = self.entrada_sintomas.get().split(',')
        sintomas_usuario = [sintoma.strip().replace(' ', '_') for sintoma in sintomas_usuario]
        
        if not sintomas_usuario or sintomas_usuario == ['']:
            messagebox.showerror("Error", "Por favor, ingrese al menos un síntoma.")
            return

        self.respuestas = {sintoma: 'si' for sintoma in sintomas_usuario}
        self.diagnosticar()

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

        self.boton_diagnosticar.config(state=tk.DISABLED)
        self.boton_nuevo_diagnostico.pack()
        self.actualizar_grafico()

    def nuevo_diagnostico(self):
        # Resetear variables y widgets
        self.sintomas_ingresados = []
        self.respuestas = {}
        self.enfermedad_diagnostico = None
        self.puntajes = {}

        # Limpiar la entrada de texto y el área de texto de síntomas
        self.entrada_sintomas.delete(0, tk.END)
        self.text_sintomas.delete(1.0, tk.END)

        # Restablecer el estado de los botones y la etiqueta
        self.boton_diagnosticar.config(state=tk.NORMAL)
        self.boton_nuevo_diagnostico.pack_forget()
        self.label.config(text="Ingrese sus síntomas (separados por comas):")

        # Limpiar el gráfico
        self.ax.clear()
        self.canvas.draw()

    def actualizar_grafico(self):
        if not hasattr(self, 'puntajes') or not self.puntajes:
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

