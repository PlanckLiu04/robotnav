"""Breadth-first search path planner."""

from collections import deque
from dataclasses import dataclass, field

from robot_path_planning.core.grid_map import Cell, GridMap


@dataclass
class SearchResult:
    path: list[Cell] = field(default_factory=list)
    visited: set[Cell] = field(default_factory=set)

    @property
    def found(self) -> bool:
        return bool(self.path)


def bfs(grid_map: GridMap, start: Cell, goal: Cell) -> SearchResult:
    queue: deque[Cell] = deque([start])
    visited: set[Cell] = {start}
    parent: dict[Cell, Cell] = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            return SearchResult(
                path=reconstruct_path(parent, start, goal),
                visited=visited,
            )

        for neighbor in grid_map.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return SearchResult(path=[], visited=visited)


def reconstruct_path(parent: dict[Cell, Cell], start: Cell, goal: Cell) -> list[Cell]:
    current = goal
    path = [current]

    while current != start:
        current = parent[current]
        path.append(current)

    path.reverse()
    return path
