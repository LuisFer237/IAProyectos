import pygame
import tkinter as tk
from tkinter import ttk, messagebox
import heapq

pygame.font.init()

# Configuración de la ventana y colores
ANCHO = 800
VENTANA = pygame.display.set_mode((ANCHO, ANCHO))
pygame.display.set_caption("Visualización de Caminos")

BLANCO = (255, 255, 255)
NEGRO = (33, 33, 33)
GRIS = (211, 211, 211)
VERDE = (34, 193, 34)
GRIS_BLOQUE = (169, 169, 169)
NARANJA = (255, 140, 0)
PURPURA = (148, 0, 211)

class Nodo:
    def __init__(self, fila, columna, ancho, total_filas):
        self.fila, self.columna = fila, columna
        self.x, self.y = fila * ancho, columna * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.padre = None

    def __lt__(self, otro):
        return self.f < otro.f

    def obtener_posicion(self):
        return self.fila, self.columna

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g, self.h, self.f = float('inf'), 0, float('inf')
        self.padre = None

    def marcar_inicio(self):
        self.color = NARANJA

    def marcar_pared(self):
        self.color = NEGRO

    def marcar_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))


def crear_matriz(filas, ancho):
    matriz = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        fila = []
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            fila.append(nodo)
        matriz.append(fila)
    return matriz


def dibujar_matriz(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))


def renderizar(ventana, matriz, filas, ancho):
    ventana.fill(BLANCO)
    for fila in matriz:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_matriz(ventana, filas, ancho)
    pygame.display.update()


def obtener_posicion_click(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    columna = x // ancho_nodo
    return fila, columna


def calcular_heuristica(nodo, fin):
    dx = abs(nodo.fila - fin.fila)
    dy = abs(nodo.columna - fin.columna)
    return max(dx, dy) + (1.41 - 1) * min(dx, dy)


def obtener_vecinos(nodo, matriz):
    vecinos = []
    filas, columnas = len(matriz), len(matriz[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in direcciones:
        x, y = nodo.fila + dx, nodo.columna + dy
        if 0 <= x < filas and 0 <= y < columnas:
            if abs(dx) + abs(dy) == 2:
                if matriz[nodo.fila][nodo.columna + dy].es_pared() and matriz[nodo.fila + dx][nodo.columna].es_pared():
                    continue
            vecinos.append(matriz[x][y])
    return vecinos


def reconstruir_camino(viene_de, nodo, ventana, matriz, inicio, fin):
    camino = []
    while nodo in viene_de:
        camino.append(nodo)
        nodo = viene_de[nodo]
    camino.append(inicio)

    for nodo in reversed(camino):
        if nodo != inicio and nodo != fin:
            nodo.color = VERDE
        renderizar(ventana, matriz, len(matriz), ANCHO)
        pygame.time.delay(100)


def algoritmo_a_estrella(ventana, matriz, inicio, fin):
    conjunto_abierto = []
    heapq.heappush(conjunto_abierto, (inicio.f, inicio))
    viene_de = {}

    inicio.g = 0
    inicio.f = calcular_heuristica(inicio, fin)

    while conjunto_abierto:
        _, nodo_actual = heapq.heappop(conjunto_abierto)

        if nodo_actual == fin:
            reconstruir_camino(viene_de, nodo_actual, ventana, matriz, inicio, fin)
            return True

        if nodo_actual != inicio and nodo_actual != fin:
            nodo_actual.color = GRIS_BLOQUE

        for vecino in obtener_vecinos(nodo_actual, matriz):
            if vecino.es_pared():
                continue

            dx = vecino.x - nodo_actual.x
            dy = vecino.y - nodo_actual.y

            g_tentativo = nodo_actual.g + (1.41 if abs(dx) + abs(dy) == 2 else 1)

            if g_tentativo < vecino.g:
                viene_de[vecino] = nodo_actual
                vecino.g = g_tentativo
                vecino.h = calcular_heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h
                heapq.heappush(conjunto_abierto, (vecino.f, vecino))

        renderizar(ventana, matriz, len(matriz), ANCHO)
        pygame.time.delay(10)

    return False


def principal():
    tamano_tablero = 10
    matriz = crear_matriz(tamano_tablero, ANCHO)

    inicio, fin = None, None
    dibujando_pared = False
    puede_dibujar_paredes = True

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                fila, col = obtener_posicion_click(pygame.mouse.get_pos(), tamano_tablero, ANCHO)
                nodo = matriz[fila][col]
                if evento.button == 1:
                    if not inicio and nodo != fin:
                        inicio = nodo
                        nodo.marcar_inicio()
                    elif not fin and nodo != inicio:
                        fin = nodo
                        nodo.marcar_fin()
                    elif nodo != fin and nodo != inicio and puede_dibujar_paredes:
                        nodo.marcar_pared()
                    dibujando_pared = True
                elif evento.button == 3:
                    nodo.restablecer()
                    if nodo == inicio:
                        inicio = None
                    elif nodo == fin:
                        fin = None

            elif evento.type == pygame.MOUSEBUTTONUP:
                dibujando_pared = False

            if evento.type == pygame.MOUSEMOTION and dibujando_pared and puede_dibujar_paredes:
                fila, col = obtener_posicion_click(pygame.mouse.get_pos(), tamano_tablero, ANCHO)
                nodo = matriz[fila][col]
                if nodo != inicio and nodo != fin:
                    nodo.marcar_pared()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and inicio and fin:
                    algoritmo_a_estrella(VENTANA, matriz, inicio, fin)
                    puede_dibujar_paredes = False

        renderizar(VENTANA, matriz, tamano_tablero, ANCHO)

    pygame.quit()


if __name__ == "__main__":
    principal()