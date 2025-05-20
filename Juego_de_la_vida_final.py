import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import os

# Tamaño de las celdas
tamaño_celda = 20

# Contar vecinos vivos
def contar_vecinos(cuadricula, x, y, filas, columnas):
    vivos = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                vivos += cuadricula[nx][ny]
    return vivos

# Reglas del juego
def siguiente_generacion(cuadricula, filas, columnas):
    nueva = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            vecinos = contar_vecinos(cuadricula, i, j, filas, columnas)
            if cuadricula[i][j] == 1:
                fila.append(1 if vecinos in (2, 3) else 0)
            else:
                fila.append(1 if vecinos == 3 else 0)
        nueva.append(fila)
    return nueva

class App:
    def __init__(self, width=1280, height=800, name="Juego de la Vida"):
        self.window = tk.Tk()
        self.window.title(name)
        self.window.geometry(f"{width}x{height}")

        self.canvas = None
        self.cuadricula = []
        self.filas = 0
        self.columnas = 0
        
        self.iteraciones = tk.StringVar(master = self.window, value="0")
        self.SetContent()
        self.window.mainloop()
       
        self.iteracion_actual=1

    def SetContent(self):
        self.label_iteraciones = tk.Label(self.window, text="Número de iteraciones:")
        self.label_iteraciones.pack()

        self.entry_iteraciones = tk.Entry(self.window, width=20, textvariable=self.iteraciones)
        self.entry_iteraciones.pack()

        self.fileButton = tk.Button(self.window, text="Cargar archivo CSV",
                                    height=2, width=20, bg="#9300ff", command=self.getFile)
        self.fileButton.pack(pady=10)

        # ✅ Botón para guardar CSV
        self.saveButton = tk.Button(self.window, text="Guardar como CSV",
                                    height=2, width=20, bg="#00bfff", command=self.Crear_csv)
        self.saveButton.pack(pady=10)

        print(f"El número ingresado es {self.iteraciones}")
        self.nIteraciones = int(self.iteraciones.get())
        return self.nIteraciones

    def getFile(self):
        try:
            self.nIteraciones = int(self.iteraciones.get())
            self.iteracion_actual = 1
        except ValueError:
            print("Por favor ingresa un número válido.")
            return
        file = filedialog.askopenfile(filetypes=[("CSV files", "*.csv")])
        if file:
            self.path_name = file.name
            self.cargar_tablero_desde_csv(self.path_name)
            self.mostrar_canvas()
            self.dibujar_cuadricula()
            self.actualizar()

    def cargar_tablero_desde_csv(self, archivo):
        self.cuadricula = []
        with open(archivo, 'r') as f:
            for linea in f:
                fila = [int(celda) for celda in linea.strip().split(',')]
                self.cuadricula.append(fila)
        self.filas = len(self.cuadricula)
        self.columnas = len(self.cuadricula[0])

    def mostrar_canvas(self):
        if self.canvas:
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.window, width=self.columnas * tamaño_celda,
                                height=self.filas * tamaño_celda, bg="pink")
        self.canvas.pack()

    def dibujar_cuadricula(self):
        self.canvas.delete("all")
        for i in range(self.filas):
            for j in range(self.columnas):
                x1 = j * tamaño_celda
                y1 = i * tamaño_celda
                x2 = x1 + tamaño_celda
                y2 = y1 + tamaño_celda
                color = "#63ff47" if self.cuadricula[i][j] == 1 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#9300ff")

    def actualizar(self):
        if self.nIteraciones <= 1:
            return
        self.cuadricula = siguiente_generacion(self.cuadricula, self.filas, self.columnas)
        self.dibujar_cuadricula()
        self.nIteraciones -= 1
        self.window.after(300, self.actualizar)

    #  Método para guardar como CSV
    def Crear_csv(self):
        ruta = os.path.join(os.getcwd(), "nuevo_csv.csv")  # Guardar en el directorio actual
        with open(ruta, "w") as nuevo_csv:
            for fila in self.cuadricula:
                linea = ",".join(str(celda) for celda in fila)
                nuevo_csv.write(linea + "\n")
        print(f"Archivo CSV guardado en: {ruta}")

# Ejecutar aplicación
app = App()
