"""A* path planner."""

from __future__ import annotations

import heapq

from robot_path_planning.core.grid_map import Cell, GridMap
from robot_path_planning.planning.bfs import SearchResult, reconstruct_path


def astar(grid_map: GridMap, start: Cell, goal: Cell) -> SearchResult:
    open_set: list[tuple[int, int, Cell]] = []
    heapq.heappush(open_set, (0, 0, start))

    visited: set[Cell] = set()
    parent: dict[Cell, Cell] = {}
    g_score: dict[Cell, int] = {start: 0}
    sequence = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in visited:
            continue

        visited.add(current)
        if current == goal:
            return SearchResult(
                path=reconstruct_path(parent, start, goal),
                visited=visited,
            )

        for neighbor in grid_map.neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, 1_000_000):
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                sequence += 1
                f_score = tentative_g + _manhattan(neighbor, goal)
                heapq.heappush(open_set, (f_score, sequence, neighbor))

    return SearchResult(path=[], visited=visited)


def _manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
