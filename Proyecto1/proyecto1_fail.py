import pygame
import heapq

pygame.init()

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (245, 245, 245)
NEGRO = (30, 30, 30)
GRIS = (150, 150, 150)
VERDE = (50, 200, 50)
ROJO = (220, 50, 50)
AZUL_CLARO = (100, 180, 255)
PURPURA = (150, 75, 175)
AZUL = (50, 100, 200)
MORADO_SUAVE = (200, 150, 255)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.padre = None

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == VERDE

    def es_fin(self):
        return self.color == ROJO

    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.padre = None

    def hacer_inicio(self):
        self.color = VERDE

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = ROJO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.g != float("inf") and self.f != float("inf"):
            font = pygame.font.SysFont('Arial', 12)
            g_text = font.render(f'g: {int(self.g)}', True, NEGRO)
            f_text = font.render(f'f: {int(self.f)}', True, NEGRO)
            ventana.blit(g_text, (self.x + 5, self.y + 5))
            ventana.blit(f_text, (self.x + 5, self.y + 20))

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def calcular_heuristica(nodo, fin):
    dx = abs(nodo.fila - fin.fila)
    dy = abs(nodo.col - fin.col)
    return max(dx, dy) + (1.41 - 1) * min(dx, dy)

def vecinos(nodo, grid):
    vecinos = []
    filas, cols = len(grid), len(grid[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in direcciones:
        x, y = nodo.fila + dx, nodo.col + dy
        if 0 <= x < filas and 0 <= y < cols:
            if abs(dx) + abs(dy) == 2:
                if grid[nodo.fila][nodo.col + dy].es_pared() and grid[nodo.fila + dx][nodo.col].es_pared():
                    continue
            vecinos.append(grid[x][y])
    return vecinos

def reconstruir_camino(came_from, nodo, ventana, grid, inicio, fin):
    camino = []
    while nodo in came_from:
        camino.append(nodo)
        nodo = came_from[nodo]
    camino.append(inicio)
    for nodo in reversed(camino):
        if nodo != inicio and nodo != fin:
            nodo.color = MORADO_SUAVE
        dibujar(ventana, grid, len(grid), ANCHO_VENTANA)
        pygame.time.delay(100)

def algoritmo_a_asterisco(ventana, grid, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (inicio.f, inicio))
    came_from = {}
    inicio.g = 0
    inicio.f = calcular_heuristica(inicio, fin)
    while open_set:
        _, nodo_actual = heapq.heappop(open_set)
        if nodo_actual == fin:
            reconstruir_camino(came_from, nodo_actual, ventana, grid, inicio, fin)
            return True
        if nodo_actual != inicio and nodo_actual != fin:
            nodo_actual.color = (255, 255, 0)
        for vecino in vecinos(nodo_actual, grid):
            if vecino.es_pared():
                continue
            dx = vecino.x - nodo_actual.x
            dy = vecino.y - nodo_actual.y
            tentativo_g = nodo_actual.g + (1.41 if abs(dx) + abs(dy) == 2 else 1)
            if tentativo_g < vecino.g:
                came_from[vecino] = nodo_actual
                vecino.g = tentativo_g
                vecino.h = calcular_heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h
                heapq.heappush(open_set, (vecino.f, vecino))
        dibujar(ventana, grid, len(grid), ANCHO_VENTANA)
        pygame.time.delay(10)
    return False

def main(ventana, ancho):
    FILAS = 7
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    algoritmo_a_asterisco(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)