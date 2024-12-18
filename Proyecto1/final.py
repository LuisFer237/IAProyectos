import pygame
import random
import heapq

ANCHO_VENTANA = 800
FILAS = 10
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("A* - Laberinto chido")
clock = pygame.time.Clock()

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float('inf')
        self.f = float('inf')
        self.neighbors = []
        self.previous = None
        self.explored = False

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def __lt__(self, other):
        return self.f < other.f

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

def connect_neighbors(grid):
    for fila in grid:
        for nodo in fila:
            if not nodo.es_pared():
                if nodo.fila > 0 and not grid[nodo.fila - 1][nodo.col].es_pared():
                    nodo.neighbors.append(grid[nodo.fila - 1][nodo.col])
                if nodo.fila < FILAS - 1 and not grid[nodo.fila + 1][nodo.col].es_pared():
                    nodo.neighbors.append(grid[nodo.fila + 1][nodo.col])
                if nodo.col > 0 and not grid[nodo.fila][nodo.col - 1].es_pared():
                    nodo.neighbors.append(grid[nodo.fila][nodo.col - 1])
                if nodo.col < FILAS - 1 and not grid[nodo.fila][nodo.col + 1].es_pared():
                    nodo.neighbors.append(grid[nodo.fila][nodo.col + 1])

                if nodo.fila > 0 and nodo.col > 0 and not grid[nodo.fila - 1][nodo.col - 1].es_pared():
                    nodo.neighbors.append(grid[nodo.fila - 1][nodo.col - 1])
                if nodo.fila < FILAS - 1 and nodo.col > 0 and not grid[nodo.fila + 1][nodo.col - 1].es_pared():
                    nodo.neighbors.append(grid[nodo.fila + 1][nodo.col - 1])
                if nodo.fila > 0 and nodo.col < FILAS - 1 and not grid[nodo.fila - 1][nodo.col + 1].es_pared():
                    nodo.neighbors.append(grid[nodo.fila - 1][nodo.col + 1])
                if nodo.fila < FILAS - 1 and nodo.col < FILAS - 1 and not grid[nodo.fila + 1][nodo.col + 1].es_pared():
                    nodo.neighbors.append(grid[nodo.fila + 1][nodo.col + 1])

def heuristic(node1, node2):
    return max(abs(node1.fila - node2.fila), abs(node1.col - node2.col))

def a_star(start, end, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g = 0
    start.f = heuristic(start, end)

    path = []

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        current = heapq.heappop(open_set)[1]
        current.explored = True

        if current == end:
            path = reconstruct_path(end)
            break

        for neighbor in current.neighbors:
            tentative_g = current.g + (1 if neighbor.fila == current.fila or neighbor.col == current.col else 1.414)
            if tentative_g < neighbor.g:
                neighbor.previous = current
                neighbor.g = tentative_g
                neighbor.f = tentative_g + heuristic(neighbor, end)
                if not any(neighbor == item[1] for item in open_set):
                    heapq.heappush(open_set, (neighbor.f, neighbor))

        VENTANA.fill(BLANCO)
        dibujar(VENTANA, grid, FILAS, ANCHO_VENTANA)
        for fila in grid:
            for nodo in fila:
                if nodo.explored and nodo != start and nodo != end:
                    nodo.color = AMARILLO
        current.color = VERDE
        start.color = NARANJA
        end.color = PURPURA
        pygame.display.update()
        clock.tick(10)

    return path

def reconstruct_path(end):
    path = []
    current = end
    while current.previous:
        path.append(current)
        current = current.previous
    path.reverse()
    for nodo in path:
        nodo.color = AZUL
    pygame.display.update()
    return path

# ...existing code...

def main():
    grid = crear_grid(FILAS, ANCHO_VENTANA)

    start = None
    end = None

    running = True
    solving = False
    path = []

    while running:
        dibujar(VENTANA, grid, FILAS, ANCHO_VENTANA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0] and not solving:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ANCHO_VENTANA)
                clicked_node = grid[fila][col]
                if not start and clicked_node != end:
                    start = clicked_node
                    start.hacer_inicio()
                elif not end and clicked_node != start:
                    end = clicked_node
                    end.hacer_fin()
                elif clicked_node != end and clicked_node != start:
                    clicked_node.hacer_pared()

            elif pygame.mouse.get_pressed()[2] and not solving:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ANCHO_VENTANA)
                clicked_node = grid[fila][col]
                clicked_node.restablecer()
                if clicked_node == start:
                    start = None
                elif clicked_node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not solving:
                    connect_neighbors(grid)
                    solving = True
                    path = a_star(start, end, grid)

        VENTANA.fill(BLANCO)
        dibujar(VENTANA, grid, FILAS, ANCHO_VENTANA)
        if path:
            for nodo in path:
                nodo.color = AZUL
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()