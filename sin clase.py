import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Necesario para formatos de imagen comunes como JPG

# Tamaño de las celdas
tamaño_celda = 55

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
        self.image_label = None  # Para mantener referencia de imagen
        self.SetContent()
        self.window.mainloop()

    def SetContent(self):
        # Mostrar imagen
        imagen_path = "mi_papa.jpg"
        imagen = Image.open(imagen_path)
        imagen = imagen.resize((300, 400))  # Ajustar tamaño de la imagen
        self.tk_image = ImageTk.PhotoImage(imagen)

        self.image_label = tk.Label(self.window, image=self.tk_image)
        self.image_label.pack(pady=10)

        # Botón para abrir archivo
        self.fileButton = tk.Button(self.window, text="Open file",
                                    height=2, width=15, bg="#9300ff", command=self.getFile)
        self.fileButton.pack(pady=10)

    def getFile(self):
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
        self.cuadricula = siguiente_generacion(self.cuadricula, self.filas, self.columnas)
        self.dibujar_cuadricula()
        self.window.after(300, self.actualizar)

# Ejecutar aplicación
app = App()