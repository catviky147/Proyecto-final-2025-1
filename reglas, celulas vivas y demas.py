import tkinter as tk

# Tamaño de las celdas
tamaño_celda = 20

#obtener ruta

# Cargar tablero desde archivo
def cargar_tablero_desde_csv(archivo):
    tablero = []
    with open(archivo, 'r') as archivo:
        for linea in archivo:
            fila = [int(celda) for celda in linea.strip().split(',')]
            tablero.append(fila)
    return tablero

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

# Dibujar el tablero
def dibujar_cuadricula(cuadricula, filas, columnas):
    canvas.delete("all")
    for i in range(filas):
        for j in range(columnas):
            x1 = j * tamaño_celda
            y1 = i * tamaño_celda
            x2 = x1 + tamaño_celda
            y2 = y1 + tamaño_celda
            color = "pink" if cuadricula[i][j] == 1 else "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

# Actualizar sin usar global
def actualizar(cuadricula, filas, columnas):
    nueva = siguiente_generacion(cuadricula, filas, columnas)
    dibujar_cuadricula(nueva, filas, columnas)
    root.after(300, lambda: actualizar(nueva, filas, columnas))

# ---- Código principal ----

# Cargar datos


cuadricula_inicial = cargar_tablero_desde_csv("archivo")
filas = len(cuadricula_inicial)
columnas = len(cuadricula_inicial[0])

# Crear ventana
root = tk.Tk()
root.title("Juego de la Vida")
canvas = tk.Canvas(root, width=columnas * tamaño_celda, height=filas * tamaño_celda)
canvas.pack()

# Dibujar y comenzar animación
dibujar_cuadricula(cuadricula_inicial, filas, columnas)
actualizar(cuadricula_inicial, filas, columnas)

root.mainloop()
