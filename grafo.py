from nodo import Nodo

class Grafo:
    def __init__(self):
        self.nodos = {}  # Diccionario de estados a nodos

    def obtener_estado(self, tablero):
        return tuple(map(tuple, tablero))

    def agregar_nodo(self, tablero):
        estado = self.obtener_estado(tablero)
        if estado not in self.nodos:
            self.nodos[estado] = Nodo(estado)
        return self.nodos[estado]

    def agregar_movimiento(self, tablero_origen, movimiento, tablero_destino, ponderacion=0):
        nodo_origen = self.agregar_nodo(tablero_origen)
        nodo_destino = self.agregar_nodo(tablero_destino)
        nodo_origen.agregar_movimiento(movimiento, nodo_destino, ponderacion)
