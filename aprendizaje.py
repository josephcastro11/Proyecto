import random
import json
import os
from grafo import Grafo

class AprendizajeSupervisado:
    def __init__(self):
        self.grafo = Grafo()
        self.cargar_aprendizaje()

    def aprender_de_partida(self, historial, resultado):
        peso = 1 if resultado == 'X' else -1
        for tablero, movimiento, tablero_destino in historial:
            self.grafo.agregar_movimiento(tablero, movimiento, tablero_destino, peso)
            peso *= -1
        self.guardar_aprendizaje()
    
    def elegir_mejor_movimiento(self, tablero):
        estado = self.grafo.obtener_estado(tablero)
        if estado in self.grafo.nodos:
            nodo = self.grafo.nodos[estado]
            if nodo.movimientos:
                return max(nodo.movimientos, key=lambda mov: nodo.movimientos[mov][1])
        movimientos_validos = [(i, j) for i in range(3) for j in range(3) if tablero[i][j] == ' ']
        return random.choice(movimientos_validos)

    def guardar_aprendizaje(self):
        data = {
            str(estado): {
                'movimientos': {
                    str(mov): (str(nodo_destino.estado), ponderacion)
                    for mov, (nodo_destino, ponderacion) in nodo.movimientos.items()
                }
            }
            for estado, nodo in self.grafo.nodos.items()
        }
        with open(os.path.join(os.getcwd(), 'aprendizaje.json'), 'w') as file:
            json.dump(data, file)

    def cargar_aprendizaje(self):
        try:
            with open(os.path.join(os.getcwd(), 'aprendizaje.json'), 'r') as file:
                data = json.load(file)
                for estado_str, nodo_data in data.items():
                    estado = eval(estado_str)  # Convertir cadena de vuelta a tupla
                    nodo = self.grafo.agregar_nodo(estado)
                    for mov_str, (estado_destino_str, ponderacion) in nodo_data['movimientos'].items():
                        movimiento = eval(mov_str)  # Convertir cadena de vuelta a tupla
                        estado_destino = eval(estado_destino_str)  # Convertir cadena de vuelta a tupla
                        nodo_destino = self.grafo.agregar_nodo(estado_destino)
                        nodo.agregar_movimiento(movimiento, nodo_destino, ponderacion)
        except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"Error loading learning file: {e}")
