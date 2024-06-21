# Diagnóstico de Enfermedades

Este programa en Python permite diagnosticar enfermedades basándose en síntomas ingresados por el usuario. Utiliza Tkinter para la interfaz gráfica y Matplotlib para visualizar el puntaje de diagnóstico por enfermedad.

## Uso

1. **Ejecución:**
   - Ejecuta `main.py` con Python 3.
   
2. **Interfaz de Usuario:**
   - Ingresa los síntomas separados por comas.
   - Haz clic en "Diagnosticar" para obtener el diagnóstico.
   - Para iniciar un nuevo diagnóstico, haz clic en "Nuevo Diagnóstico".

## Requisitos

- Python 3.x
- Tkinter (incluido en Python estándar)
- Matplotlib (`pip install matplotlib`)

## Archivos

- **main.py:** Implementación principal del programa.
- **base_conocimientos.txt:** Archivo con enfermedades y síntomas asociados.

## Estructura y Componentes

El programa implementa un Sistema Experto para el diagnóstico de enfermedades, que consta de varios componentes clave:

- **Base de Conocimientos:** Se carga desde el archivo `base_conocimientos.txt`. Este archivo contiene información sobre enfermedades y sus síntomas asociados, organizados en un diccionario.

- **Mecanismo de Inferencia:** Implementado en el método `inferencia` de la clase `DiagnosticoEnfermedad`. Este mecanismo calcula puntajes para cada enfermedad basándose en los síntomas ingresados por el usuario y la base de conocimientos cargada.

- **Interfaz de Usuario:** Utiliza Tkinter para crear una interfaz gráfica simple. Permite al usuario ingresar síntomas, realizar diagnósticos y mostrar resultados de manera interactiva.

- **Componente Explicativo:** La clase `DiagnosticoEnfermedad` también incluye métodos como `mostrar_diagnostico` para explicar al usuario cómo se llegó al diagnóstico, mostrando los síntomas relevantes y los puntajes de cada enfermedad.

- **Componente de Adquisición:** Aunque no está implementado explícitamente en este código, la estructura permite la extensión del sistema para agregar más enfermedades y síntomas en el archivo `base_conocimientos.txt`.

Estos componentes trabajan en conjunto para proporcionar un diagnóstico interactivo de enfermedades basado en la información de la base de conocimientos y la interacción del usuario.