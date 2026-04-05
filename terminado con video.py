import tkinter as tk


filas = 16
columnas = 16
tamano_celda = 20

# Inicializar cuadrícula vacía
cuadricula = [[0 for _ in range(columnas)] for _ in range(filas)]
celdas_seleccionadas = 0
juego_iniciado = False

# Contar vecinos vivos
def contar_vecinos(cuadricula, x, y):
    vivos = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                vivos += cuadricula[nx][ny]
    return vivos

# Aplicar reglas del juego de la vida
def siguiente_generacion(cuadricula):
    nueva = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            vecinos = contar_vecinos(cuadricula, i, j)
            if cuadricula[i][j] == 1:
                fila.append(1 if vecinos in (2, 3) else 0)
            else:
                fila.append(1 if vecinos == 3 else 0)
        nueva.append(fila)
    return nueva

# Dibujar la cuadrícula
def dibujar_cuadricula():
    canvas.delete("all")
    for i in range(filas):
        for j in range(columnas):
            x1 = j * tamano_celda
            y1 = i * tamano_celda
            x2 = x1 + tamano_celda
            y2 = y1 + tamano_celda
            color = "white" if cuadricula[i][j] == 1 else "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

# Guardar en CSV
def guardar_csv():
    with open("cuadricula_vida.csv", "w") as archivo:
        for fila in cuadricula:
            linea = ",".join(str(celda) for celda in fila)
            archivo.write(linea + "\n")

# Clic del usuario para seleccionar 3 celdas vivas
def seleccionar_celda(event):
    global celdas_seleccionadas, juego_iniciado
    if juego_iniciado:
        return

    fila = event.y // tamano_celda
    columna = event.x // tamano_celda

    if 0 <= fila < filas and 0 <= columna < columnas:
        if cuadricula[fila][columna] == 0:
            cuadricula[fila][columna] = 1
            celdas_seleccionadas += 1
            dibujar_cuadricula()
            if celdas_seleccionadas == 10:
                juego_iniciado = True
                guardar_csv()
                ventana.after(5000, actualizar)

# Actualización automática del juego
def actualizar():
    global cuadricula
    if juego_iniciado:
        cuadricula = siguiente_generacion(cuadricula)
        dibujar_cuadricula()
        ventana.after(500, actualizar)

# Crear ventana
ventana = tk.Tk()
ventana.title("Juego de la Vida - Selección Inicial")

canvas = tk.Canvas(ventana, width=columnas * tamano_celda, height=filas * tamano_celda)
canvas.pack()
canvas.bind("<Button-1>", seleccionar_celda)

dibujar_cuadricula()
ventana.mainloop()