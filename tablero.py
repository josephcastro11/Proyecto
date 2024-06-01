class Tablero:
    def __init__(self):
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
    
    def mostrar_tablero(self):
        for fila in self.tablero:
            print('|'.join(fila))
            print('-' * 5)
    
    def movimiento_valido(self, fila, columna):
        return self.tablero[fila][columna] == ' '
    
    def realizar_movimiento(self, fila, columna, jugador):
        if self.movimiento_valido(fila, columna):
            self.tablero[fila][columna] = jugador
            return True
        return False
    
    def verificar_ganador(self):
        combinaciones = [self.tablero[i] for i in range(3)] + \
                        [list(col) for col in zip(*self.tablero)] + \
                        [[self.tablero[i][i] for i in range(3)]] + \
                        [[self.tablero[i][2-i] for i in range(3)]]
        for combinacion in combinaciones:
            if combinacion[0] != ' ' and combinacion.count(combinacion[0]) == 3:
                return combinacion[0]
        return None
    
    def tablero_lleno(self):
        return all(cell != ' ' for row in self.tablero for cell in row)
