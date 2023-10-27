import numpy as np
import random
import pygame
import sys
import math
from pygame.locals import *
import time


pygame.init()
start_time = time.time()
filas = 6
columnas = 7 
jugador = 0
AI = 1
fichaJugador =1
fichaAI = 2
turno = random.randint(jugador, AI)
interfaz = 100
espacios = 45
width = columnas * interfaz
height = (filas + 1) * interfaz
size = (width, height)
profundidades = 3


def filaDisponible(tablero, col):
    for fila in range(filas):
        if tablero[fila][col] == 0:
            return fila
        
def columnaDisponible(tablero):
    columnaDisponible = []
    for col in range(columnas):
        if tablero[filas-1][col] == 0:
            columnaDisponible.append(col)
    return columnaDisponible

def minimax(tablero, depth, alpha, beta, maximixingPlayer):
    columnaDisponibles = columnaDisponible(tablero)
    nodoFinal = ganador(tablero, fichaJugador) or ganador(tablero, fichaAI) or len(columnaDisponible(tablero)) == 0
   
    if depth == 0 or nodoFinal:
        if nodoFinal:
            if ganador(tablero, fichaAI):
                return None, 9999999999999
            elif ganador(tablero, fichaJugador):
                return None, -9999999999999
            else:
                return None, 0
        else:
            return None, puntajes(tablero, fichaAI)

    if maximixingPlayer:
        value = -float('inf')
        column = random.choice(columnaDisponibles)
        for col in columnaDisponibles:
            fila = filaDisponible(tablero, col)
            copiatablero = tablero.copy()
            copiatablero[fila][col] = fichaAI
            newScore = minimax(copiatablero, depth - 1, alpha, beta, False)
            if newScore is not None and newScore[1] > value:
                value = newScore[1]
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = float('inf')
        column = random.choice(columnaDisponibles)
        for col in columnaDisponibles:
            fila = filaDisponible(tablero, col)
            copiatablero = tablero.copy()
            copiatablero[fila][col] = fichaJugador
            newScore = minimax(copiatablero, depth - 1, alpha, beta, True)
            if newScore is not None and newScore[1] < value:
                value = newScore[1]
                column = col
            beta = min(beta, value) 
            if alpha >= beta:
                break
        return column, value

def ganador(tablero, ficha):
  
    for columna  in range(columnas-3):
        for fila in range(filas):
            if tablero[fila][columna ] == ficha and tablero[fila][columna +1] == ficha and tablero[fila][columna +2] == ficha and tablero[fila][columna +3] == ficha:
                return True

    for columna  in range(columnas):
        for fila in range(filas-3):
            if tablero[fila][columna ] == ficha and tablero[fila+1][columna ] == ficha and tablero[fila+2][columna] == ficha and tablero[fila+3][columna] == ficha:
                return True

    for columna in range(columnas-3):
       for fila in range(filas-3):
            if tablero[fila][columna] == ficha and tablero[fila+1][columna+1] == ficha and tablero[fila+2][columna+2] == ficha and tablero[fila+3][columna+3] == ficha:
                return True       
            
    for columna in range(columnas-3):
       for fila in range(3, filas):
            if tablero[fila][columna] == ficha and tablero[fila-1][columna+1] == ficha and tablero[fila-2][columna+2] == ficha and tablero[fila-3][columna+3] == ficha:
                return True  
            
def calcularPuntajes(estadoActual, ficha):
    score = 0
    
    if estadoActual.count(ficha) == 4:
        score = score + 100
    elif estadoActual.count(ficha) == 3 and estadoActual.count(0) == 1:
        score = score + 10
    elif estadoActual.count(ficha) == 2 and estadoActual.count(0) == 2:
        score = score + 5
    
    if ficha == fichaJugador:
        fichaOponete = fichaAI
    else:
        fichaOponete = fichaJugador
        
    if estadoActual.count(fichaOponete) == 3 and estadoActual.count(0) == 1:
        score = score - 15
        
    return score


def puntajes(tablero, ficha):
    score = 0
    
    centroArray = [i for i in list(tablero[:, columnas//2])]
    centerCount = centroArray.count(ficha)
    score = score + centerCount * 5
    
    for fila in range(filas):
        filaArray = [i for i in list(tablero[fila,:])]
        for columna in range(columnas-3):
            estadoActual = filaArray[columna:columna+4]
            score = score + calcularPuntajes(estadoActual, ficha)
            
    for columna in range(columnas):
        colArray = [i for i in list(tablero[:,columna])]
        for fila in range(filas-3):
            estadoActual = colArray[fila:fila+4]
            score = score + calcularPuntajes(estadoActual, ficha)

    for fila in range(filas-3):
        for columna in range(columnas-3):
            estadoActual = [tablero[fila+i][columna+i] for i in range(4)]
            score = score + calcularPuntajes(estadoActual, ficha)
            
    for fila in range(filas-3):
        for columna in range(columnas-3):
            estadoActual = [tablero[fila+3-i][columna+i] for i in range(4)]
            score = score + calcularPuntajes(estadoActual, ficha)
            
    return score

madera = (169, 92, 42)
sombra = (255, 255, 255)
negro = (0,0,0)
rojo = (255,0,0)
blanco = (255, 255, 255)
#pygame.init()
screen = pygame.display.set_mode(size)

pygame.display.update()
myfont = pygame.font.Font(None, 50)

tablero = np.zeros((filas, columnas))
def dibujarTablero(tablero):
    for columna in range(columnas):
        for f in range(filas):
            pygame.draw.rect(screen, madera,(columna*interfaz, f*interfaz+interfaz,interfaz, interfaz)) 
            pygame.draw.line(screen, sombra,[int(columna*100), 100], [int(columna*100),750], 2)
            pygame.draw.circle(screen, negro, (int(columna*interfaz+interfaz/2), int(f*interfaz+interfaz+interfaz/2)), espacios)
            
    for columna in range(columnas):
        for f in range(filas):
            if tablero[f][columna] == fichaJugador:
                pygame.draw.circle(screen, rojo, (int(columna*interfaz+interfaz/2), height-int(f*interfaz+interfaz/2)), espacios)
            elif tablero[f][columna] == fichaAI:
                pygame.draw.circle(screen, blanco , (int(columna*interfaz+interfaz/2), height-int(f*interfaz+interfaz/2)), espacios)
    pygame.display.update()

def seleccionarProfundidad():
    global profundidades
    seleccionado = False
    while not seleccionado:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    profundidades = 1
                    seleccionado = True
                elif event.key == K_2:
                    profundidades = 3
                    seleccionado = True
                elif event.key == K_3:
                    profundidades = 6
                    seleccionado = True

        screen.fill((0, 0, 0))
        label1 = myfont.render("Digite el numero de la dificulta:", 1, (255, 255, 255))
        label2 = myfont.render("1: Facil | 2: Media  | 3: Dificil ", 1, (255, 255, 255))
        screen.blit(label1, (50, 50))
        screen.blit(label2, (50, 100))
        pygame.display.update()
    
    screen.fill((0, 0, 0))
    pygame.display.update()

seleccionarProfundidad()
gameOver = False
dibujarTablero(tablero)

def updateLabel():
    screen.blit(label, (10,10))
    pygame.display.update()
    pygame.time.wait(200)
    

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, negro, (0, 0, width, interfaz))
            if turno == jugador:
                posx = event.pos[0]
                col = int(math.floor(posx / interfaz))

                if tablero[filas - 1][col] == 0:
                    fila = filaDisponible(tablero, col)
                    tablero[fila][col] = fichaJugador

                    if ganador(tablero, fichaJugador):
                        dibujarTablero(tablero)
                        label = myfont.render("¡GANASTES!", 1, rojo)
                        updateLabel()

                        gameOver = True

                    if turno == AI:
                        turno = jugador
                    else:
                        turno = AI

                    dibujarTablero(tablero)

    if turno == AI and not gameOver:
        col, minimaxScore = minimax(tablero, profundidades , -float('inf'), float('inf'), True)

        if tablero[filas - 1][col] == 0:

            fila = filaDisponible(tablero, col)
            tablero[fila][col] = fichaAI

            if ganador(tablero, fichaAI):
                dibujarTablero(tablero)
                label = myfont.render("¡LA IA GANÓ!", 1, blanco )
                updateLabel()

                gameOver = True

            if turno == AI:
                turno = jugador
            else:
                turno = AI

            dibujarTablero(tablero)
    
    if gameOver:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"------------------------------!-------------------------------")
        print(f"Análisis de desempeño con la profundidad en : {profundidades}")
        print(f"Tiempo de ejecución: {execution_time} segundos")
        print(f"------------------------------!-------------------------------")
        pygame.time.wait(1500)
