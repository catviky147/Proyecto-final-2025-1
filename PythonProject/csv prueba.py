def cargar_tablero_desde_csv(nombre_archivo):
    tablero = []
    archivo= open(nombre_archivo, "r")
     
    tablero=archivo.read()
    return tablero

#codigo principal
tablero = cargar_tablero_desde_csv('juego de la vida.csv')

print (tablero)