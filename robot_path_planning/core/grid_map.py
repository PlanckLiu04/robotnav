"""Grid map state and editing helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
import random

from robot_path_planning.config import CELL_SIZE, COLS, ROWS

Cell = tuple[int, int]


@dataclass
class GridMap:
    rows: int = ROWS
    cols: int = COLS
    cell_size: int = CELL_SIZE
    obstacles: set[Cell] = field(default_factory=set)
    start: Cell | None = None
    goal: Cell | None = None

    def contains(self, cell: Cell) -> bool:
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols

    def pixel_to_cell(self, position: tuple[int, int]) -> Cell | None:
        x, y = position
        cell = (y // self.cell_size, x // self.cell_size)
        if not self.contains(cell):
            return None
        return cell

    def is_walkable(self, cell: Cell) -> bool:
        return self.contains(cell) and cell not in self.obstacles

    def inflated_copy(self, inflation_cells: int) -> "GridMap":
        """Return a planning copy with obstacles expanded by a cell radius."""
        inflated = GridMap(rows=self.rows, cols=self.cols, cell_size=self.cell_size)
        inflated.start = self.start
        inflated.goal = self.goal

        for obstacle in self.obstacles:
            for cell in self._inflated_cells(obstacle, inflation_cells):
                if cell != self.start and cell != self.goal:
                    inflated.obstacles.add(cell)

        return inflated

    def neighbors(self, cell: Cell) -> list[Cell]:
        row, col = cell
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return [candidate for candidate in candidates if self.is_walkable(candidate)]

    def toggle_obstacle(self, cell: Cell) -> bool:
        if cell == self.start or cell == self.goal:
            return False

        if cell in self.obstacles:
            self.obstacles.remove(cell)
        else:
            self.obstacles.add(cell)
        return True

    def set_obstacle(self, cell: Cell, blocked: bool) -> bool:
        if cell == self.start or cell == self.goal:
            return False

        if blocked:
            if cell in self.obstacles:
                return False
            self.obstacles.add(cell)
            return True

        if cell not in self.obstacles:
            return False
        self.obstacles.remove(cell)
        return True

    def set_start(self, cell: Cell) -> bool:
        if cell in self.obstacles or cell == self.goal:
            return False
        self.start = cell
        return True

    def set_goal(self, cell: Cell) -> bool:
        if cell in self.obstacles or cell == self.start:
            return False
        self.goal = cell
        return True

    def clear(self) -> None:
        self.obstacles.clear()
        self.start = None
        self.goal = None

    def generate_random(self, obstacle_density: float) -> None:
        self.clear()

        all_cells = [(row, col) for row in range(self.rows) for col in range(self.cols)]
        self.start, self.goal = random.sample(all_cells, 2)

        obstacle_count = int(len(all_cells) * obstacle_density)
        candidates = [
            cell for cell in all_cells
            if cell != self.start and cell != self.goal
        ]
        self.obstacles = set(random.sample(candidates, obstacle_count))

    def _inflated_cells(self, center: Cell, inflation_cells: int) -> list[Cell]:
        if inflation_cells <= 0:
            return [center] if self.contains(center) else []

        center_row, center_col = center
        cells = []
        for row in range(center_row - inflation_cells, center_row + inflation_cells + 1):
            for col in range(center_col - inflation_cells, center_col + inflation_cells + 1):
                cell = (row, col)
                if self.contains(cell):
                    cells.append(cell)
        return cells
