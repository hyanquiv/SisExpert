import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

class DiagnosticoEnfermedad:
    def __init__(self, master):
        self.master = master
        self.master.title("Diagnóstico de Enfermedades")
        self.master.geometry("400x300")

        self.enfermedades = self.cargar_base_conocimientos("base_conocimientos.txt")
        self.sintomas_preguntados = []
        self.respuestas = {}
        self.enfermedad_diagnostico = None

        self.label = tk.Label(master, text="¿Tiene alguno de estos síntomas?")
        self.label.pack(pady=10)

        self.boton_si = tk.Button(master, text="Sí", command=lambda: self.responder('si'))
        self.boton_si.pack(side=tk.LEFT, padx=20, pady=20)

        self.boton_no = tk.Button(master, text="No", command=lambda: self.responder('no'))
        self.boton_no.pack(side=tk.RIGHT, padx=20, pady=20)

        self.sintoma_actual = None
        self.proximo_sintoma()

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

    def diagnosticar(self):
        puntajes = defaultdict(int)
        for sintoma, respuesta in self.respuestas.items():
            if respuesta == 'si':
                for enfermedad, sintomas in self.enfermedades.items():
                    if sintoma in sintomas:
                        puntajes[enfermedad] += 1

        if puntajes:
            self.enfermedad_diagnostico = max(puntajes, key=puntajes.get)
            self.label.config(text=f"Diagnóstico: {self.enfermedad_diagnostico.replace('_', ' ')}")
        else:
            self.label.config(text="No se pudo determinar la enfermedad con los síntomas proporcionados.")

        self.boton_si.pack_forget()
        self.boton_no.pack_forget()
        tk.Button(self.master, text="Salir", command=self.master.quit).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosticoEnfermedad(root)
    root.mainloop()
