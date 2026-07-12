"""Coordinate conversion helpers for grid, world, and screen spaces."""

from __future__ import annotations

from robot_path_planning import config

Cell = tuple[int, int]
WorldPosition = tuple[float, float]
ScreenPosition = tuple[int, int]


def cell_center_to_world(cell: Cell) -> WorldPosition:
    """Return the continuous world-space center of a grid cell."""
    row, col = cell
    return col + 0.5, row + 0.5


def world_to_screen(position: WorldPosition) -> ScreenPosition:
    """Convert a continuous world-space point to a Pygame pixel position."""
    x, y = position
    return int(x * config.CELL_SIZE), int(y * config.CELL_SIZE)


def cell_to_screen_rect(cell: Cell, inset: int = 0) -> tuple[int, int, int, int]:
    """Return the screen-space rectangle occupied by a grid cell."""
    row, col = cell
    return (
        col * config.CELL_SIZE + inset,
        row * config.CELL_SIZE + inset,
        config.CELL_SIZE - inset * 2,
        config.CELL_SIZE - inset * 2,
    )


def distance(a: WorldPosition, b: WorldPosition) -> float:
    """Return Euclidean distance between two continuous world-space points."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
