#No se si sirve, creo que no
cuadricula = [[1 for _ in range (filas)] for _ in range(columnas)]
celdas_seleccionadas = 0
inicializa = False
 

# Contar vecinos vivos
def contar_vecinos(cuadricula, x, y):
    vivos = 0
    for desplazamiento_x in [-1, 0, 1]:
        for desplazamiento_y in [-1, 0, 1]:
            if desplazamiento_x == 0 and desplazamiento_y == 0:
                continue
            nx, ny = x + desplazamiento_x, y + desplazamiento_y
            if 0 <= nx < filas and 0 <= ny < columnas:
                vivos += cuadricula[nx][ny]
    return vivos

#reglas 
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