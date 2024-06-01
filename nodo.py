class Nodo:
    def __init__(self, estado):
        self.estado = estado  # Estado del tablero como una tupla de tuplas
        self.movimientos = {}  # Diccionario de movimientos posibles y sus ponderaciones

    def agregar_movimiento(self, movimiento, nodo_destino, ponderacion=0):
        self.movimientos[movimiento] = (nodo_destino, ponderacion)
