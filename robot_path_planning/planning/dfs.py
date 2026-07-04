"""Depth-first search path planner."""

from robot_path_planning.core.grid_map import Cell, GridMap
from robot_path_planning.planning.bfs import SearchResult, reconstruct_path


def dfs(grid_map: GridMap, start: Cell, goal: Cell) -> SearchResult:
    stack: list[Cell] = [start]
    visited: set[Cell] = set()
    visited_order: list[Cell] = []
    parent: dict[Cell, Cell] = {}

    while stack:
        current = stack.pop()
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

        for neighbor in reversed(grid_map.neighbors(current)):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                stack.append(neighbor)

    return SearchResult(path=[], visited=visited, visited_order=visited_order)
