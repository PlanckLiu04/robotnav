"""Dijkstra shortest-path planner."""

from __future__ import annotations

import heapq

from robot_path_planning.core.grid_map import Cell, GridMap
from robot_path_planning.planning.bfs import SearchResult, reconstruct_path


def dijkstra(grid_map: GridMap, start: Cell, goal: Cell) -> SearchResult:
    open_set: list[tuple[int, int, Cell]] = []
    heapq.heappush(open_set, (0, 0, start))

    visited: set[Cell] = set()
    visited_order: list[Cell] = []
    parent: dict[Cell, Cell] = {}
    distance: dict[Cell, int] = {start: 0}
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
            new_distance = distance[current] + 1
            if new_distance < distance.get(neighbor, 1_000_000):
                parent[neighbor] = current
                distance[neighbor] = new_distance
                sequence += 1
                heapq.heappush(open_set, (new_distance, sequence, neighbor))

    return SearchResult(path=[], visited=visited, visited_order=visited_order)
