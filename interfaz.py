import tkinter as tk
from tkinter import messagebox
import json
from tablero import Tablero
from aprendizaje import AprendizajeSupervisado

class InterfazGrafica:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("To Ti To con Aprendizaje Supervisado")
        self.crear_componentes()
        self.juego = AprendizajeSupervisado()
        self.historial = []
        self.partidas_jugadas = 0
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.tablero = None
        self.botones = []
    
    def crear_componentes(self):
        self.frame_menu = tk.Frame(self.ventana)
        self.frame_menu.grid(row=0, column=0)

        self.boton_jugar = tk.Button(self.frame_menu, text="Jugar", command=self.iniciar_juego)
        self.boton_historial = tk.Button(self.frame_menu, text="Ver Historial", command=self.mostrar_historial)
        self.boton_aprendizaje = tk.Button(self.frame_menu, text="Ver Aprendizaje", command=self.mostrar_aprendizaje)
        self.boton_integrantes = tk.Button(self.frame_menu, text="Ver Integrantes", command=self.mostrar_integrantes)
        self.boton_jugar.grid(row=0, column=0, padx=5, pady=5)
        self.boton_historial.grid(row=0, column=1, padx=5, pady=5)
        self.boton_aprendizaje.grid(row=0, column=2, padx=5, pady=5)
        self.boton_integrantes.grid(row=0, column=3, padx=5, pady=5)

    def iniciar_juego(self):
        self.tablero = Tablero()
        self.historial.clear()
        self.crear_tablero()

    def crear_tablero(self):
        if hasattr(self, 'frame_tablero'):
            self.frame_tablero.destroy()

        self.frame_tablero = tk.Frame(self.ventana)
        self.frame_tablero.grid(row=1, column=0)

        self.botones = []
        for i in range(3):
            fila_botones = []
            for j in range(3):
                boton = tk.Button(self.frame_tablero, text=" ", width=10, height=3,
                                  command=lambda fila=i, columna=j: self.realizar_movimiento(fila, columna))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

    def realizar_movimiento(self, fila, columna):
        if self.tablero.realizar_movimiento(fila, columna, 'X'):
            self.botones[fila][columna].config(text='X', state=tk.DISABLED)
            self.historial.append((self.tablero.tablero, (fila, columna), 'X'))
            self.verificar_estado()

    def verificar_estado(self):
        ganador = self.tablero.verificar_ganador()
        if ganador:
            self.partidas_jugadas += 1
            if ganador == 'X':
                self.partidas_ganadas += 1
                messagebox.showinfo("Fin del juego", "¡Ganaste!")
            else:
                self.partidas_perdidas += 1
                messagebox.showinfo("Fin del juego", "Perdiste.")
            self.juego.aprender_de_partida(self.historial, ganador)
            self.mostrar_menu_principal()
            return

        if self.tablero.tablero_lleno():
            self.partidas_jugadas += 1
            messagebox.showinfo("Fin del juego", "Empate.")
            self.mostrar_menu_principal()
            return

        self.movimiento_maquina()

    def movimiento_maquina(self):
        movimiento_oponente = self.juego.elegir_mejor_movimiento(self.tablero.tablero)
        self.tablero.realizar_movimiento(movimiento_oponente[0], movimiento_oponente[1], 'O')
        self.botones[movimiento_oponente[0]][movimiento_oponente[1]].config(text='O', state=tk.DISABLED)
        self.historial.append((self.tablero.tablero, movimiento_oponente, 'O'))

        ganador = self.tablero.verificar_ganador()
        if ganador:
            self.partidas_jugadas += 1
            if ganador == 'X':
                self.partidas_ganadas += 1
                messagebox.showinfo("Fin del juego", "¡Ganaste!")
            else:
                self.partidas_perdidas += 1
                messagebox.showinfo("Fin del juego", "Perdiste.")
            self.juego.aprender_de_partida(self.historial, ganador)
            self.mostrar_menu_principal()
            return

        if self.tablero.tablero_lleno():
            self.partidas_jugadas += 1
            messagebox.showinfo("Fin del juego", "Empate.")
            self.mostrar_menu_principal()
            return

    def mostrar_historial(self):
        historial_texto = f"Partidas jugadas: {self.partidas_jugadas}\nPartidas ganadas: {self.partidas_ganadas}\nPartidas perdidas: {self.partidas_perdidas}\n"
        messagebox.showinfo("Historial", historial_texto)

    def mostrar_integrantes(self):
        integrantes = "Integrantes del grupo:\nJoseph Antonio Castro Artol, 9490-18-4296, Sección0 C\nChristian Saúl García Franco, 9490-17-2279, Sección C"
        messagebox.showinfo("Integrantes", integrantes)

    def mostrar_aprendizaje(self):
        try:
            with open('aprendizaje.json', 'r') as file:
                data = json.load(file)
                aprendizaje_texto = json.dumps(data, indent=2)
                messagebox.showinfo("Aprendizaje", aprendizaje_texto)
        except FileNotFoundError:
            messagebox.showinfo("Aprendizaje", "No se ha encontrado el archivo de aprendizaje.")
        except json.JSONDecodeError:
            messagebox.showinfo("Aprendizaje", "Error al decodificar el archivo de aprendizaje.")

    def mostrar_menu_principal(self):
        if hasattr(self, 'frame_tablero'):
            self.frame_tablero.destroy()
        self.botones = []
        self.crear_componentes()

    def ejecutar(self):
        self.ventana.mainloop()


