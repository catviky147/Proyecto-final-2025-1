import csv
def cargar_tablero_desde_csv(nombre_archivo):
    tablero = []
    with open(nombre_archivo, newline='') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            # Convertimos cada valor de texto a entero
            tablero.append([int(celda) for celda in fila])
    return tablero

tablero = cargar_tablero_desde_csv('juego de la vida.csv')

for sublista in tablero:
    for elemento in sublista:
        print(elemento, end=" ") 
    print()