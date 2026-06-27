import pygame
from collections import deque

pygame.init()

WIDTH, HEIGHT = 900, 600
CELL_SIZE = 30

ROWS = HEIGHT // CELL_SIZE  # 行 row
COLS = WIDTH // CELL_SIZE  # 列 column

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Robot Path Planning Simulator")

clock = pygame.time.Clock()
running = True

obstacles = set()
start = None
goal = None
path = []

mode = "obstacle"


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (210, 210, 210), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (210, 210, 210), (0, y), (WIDTH, y))


def draw_cell(cell, color):
    row, col = cell

    rect = pygame.Rect(
        col * CELL_SIZE,
        row * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(screen, color, rect)


def draw_obstacles():
    for cell in obstacles:
        draw_cell(cell, (40, 40, 40))


def get_neighbors(cell):
    row, col = cell

    neighbors = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1)
    ]

    valid_neighbors = []

    for neighbor in neighbors:
        n_row, n_col = neighbor

        inside_grid = 0 <= n_row < ROWS and 0 <= n_col < COLS
        not_obstacle = neighbor not in obstacles

        if inside_grid and not_obstacle:
            valid_neighbors.append(neighbor)

    return valid_neighbors


def bfs(start, goal):
    queue = deque()
    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            result_path = []
            while current != start:
                result_path.append(current)
                current = parent[current]

            result_path.append(start)
            result_path.reverse()
            return result_path

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return []


while running:
    pygame.display.set_caption(
        f"Mode: {mode} | 1: obstacle  2: start  3: goal  SPACE: find path"
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "obstacle"
            elif event.key == pygame.K_2:
                mode = "start"
            elif event.key == pygame.K_3:
                mode = "goal"
            elif event.key == pygame.K_SPACE:
                if start is not None and goal is not None:
                    path = bfs(start, goal)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE
            cell = (row, col)

            path = []

            if mode == "obstacle":
                if cell != start and cell != goal:
                    if cell in obstacles:
                        obstacles.remove(cell)
                    else:
                        obstacles.add(cell)

            elif mode == "start":
                if cell not in obstacles and cell != goal:
                    start = cell

            elif mode == "goal":
                if cell not in obstacles and cell != start:
                    goal = cell

    screen.fill((245, 245, 245))

    for cell in path:
        draw_cell(cell, (80, 160, 255))

    draw_obstacles()

    if start is not None:
        draw_cell(start, (0, 180, 90))

    if goal is not None:
        draw_cell(goal, (220, 60, 60))

    draw_grid()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
