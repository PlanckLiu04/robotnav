"""Greedy best-first search path planner."""

from __future__ import annotations

import heapq

from robot_path_planning.core.grid_map import Cell, GridMap
from robot_path_planning.planning.bfs import SearchResult, reconstruct_path


def greedy_best_first(grid_map: GridMap, start: Cell, goal: Cell) -> SearchResult:
    open_set: list[tuple[int, int, Cell]] = []
    heapq.heappush(open_set, (_manhattan(start, goal), 0, start))

    visited: set[Cell] = set()
    visited_order: list[Cell] = []
    parent: dict[Cell, Cell] = {}
    queued: set[Cell] = {start}
    sequence = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return SearchResult(
                path=reconstruct_path(parent, start, goal),
                visited=visited,
                visited_order=visited_order,
            )

        for neighbor in grid_map.neighbors(current):
            if neighbor not in visited and neighbor not in queued:
                parent[neighbor] = current
                queued.add(neighbor)
                sequence += 1
                heapq.heappush(open_set, (_manhattan(neighbor, goal), sequence, neighbor))

    return SearchResult(path=[], visited=visited, visited_order=visited_order)


def _manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
