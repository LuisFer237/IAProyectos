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

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.valor_g = float("inf")
        self.valor_f = float("inf")

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

    def hacer_inicio(self):
        self.color = VERDE

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = ROJO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.valor_g != float("inf") and self.valor_f != float("inf"):
            font = pygame.font.SysFont('Arial', 12)
            g_text = font.render(f'g: {int(self.valor_g)}', True, NEGRO)
            f_text = font.render(f'f: {int(self.valor_f)}', True, NEGRO)
            ventana.blit(g_text, (self.x + 5, self.y + 5))
            ventana.blit(f_text, (self.x + 5, self.y + 20))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():  # Abajo
            self.vecinos.append(grid[self.fila + 1][self.col])
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():  # Arriba
            self.vecinos.append(grid[self.fila - 1][self.col])
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():  # Derecha
            self.vecinos.append(grid[self.fila][self.col + 1])
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():  # Izquierda
            self.vecinos.append(grid[self.fila][self.col - 1])
        # Diagonales
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][self.col + 1].es_pared():  # Abajo-Derecha
            self.vecinos.append(grid[self.fila + 1][self.col + 1])
        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared():  # Abajo-Izquierda
            self.vecinos.append(grid[self.fila + 1][self.col - 1])
        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():  # Arriba-Derecha
            self.vecinos.append(grid[self.fila - 1][self.col + 1])
        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():  # Arriba-Izquierda
            self.vecinos.append(grid[self.fila - 1][self.col - 1])

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

def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return max(abs(x1 - x2), abs(y1 - y2))

def reconstruir_camino(came_from, actual, draw):
    while actual in came_from:
        actual = came_from[actual]
        actual.color = GRIS
        draw()

def algoritmoasterisco(draw, grid, inicio, fin):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, inicio))
    came_from = {}
    valor_g = {nodo: float("inf") for fila in grid for nodo in fila}
    valor_g[inicio] = 0
    valor_f = {nodo: float("inf") for fila in grid for nodo in fila}
    valor_f[inicio] = heuristica(inicio.get_pos(), fin.get_pos())

    open_set_hash = {inicio}

    while not len(open_set) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        actual = heapq.heappop(open_set)[2]
        open_set_hash.remove(actual)

        if actual == fin:
            reconstruir_camino(came_from, fin, draw)
            fin.color = ROJO
            inicio.color = VERDE
            return True

        for vecino in actual.vecinos:
            temp_valor_g = valor_g[actual] + 1

            if temp_valor_g < valor_g[vecino]:
                came_from[vecino] = actual
                valor_g[vecino] = temp_valor_g
                valor_f[vecino] = temp_valor_g + heuristica(vecino.get_pos(), fin.get_pos())
                vecino.valor_g = valor_g[vecino]
                vecino.valor_f = valor_f[vecino]
                if vecino not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (valor_f[vecino], count, vecino))
                    open_set_hash.add(vecino)
                    vecino.color = AZUL

        draw()

        if actual != inicio and actual != fin:
            actual.color = AZUL

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

                    algoritmoasterisco(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)