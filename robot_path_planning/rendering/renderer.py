"""Pygame renderer for the map, path, and interface."""

from __future__ import annotations

import math

import pygame

from robot_path_planning import config
from robot_path_planning.core.app_state import AppState, ScreenMode
from robot_path_planning.core.coordinates import cell_to_screen_rect, world_to_screen
from robot_path_planning.core.grid_map import Cell, GridMap
from robot_path_planning.ui.panel import SidePanel


class Renderer:
    def __init__(self, screen: pygame.Surface, panel: SidePanel) -> None:
        self.screen = screen
        self.panel = panel

    def draw(self, grid_map: GridMap, state: AppState) -> None:
        self.screen.fill(config.COLOR_BACKGROUND)

        if state.screen == ScreenMode.HOME:
            self.panel.draw_home(self.screen)
            return

        self._draw_grid_background()
        self._draw_visited(state.visited, state.path)
        self._draw_path(state.path)
        self._draw_obstacles(grid_map)
        self._draw_start_goal(grid_map)
        self._draw_robot(state)
        self._draw_grid_lines()
        self.panel.draw(self.screen, grid_map, state)

    def _draw_grid_background(self) -> None:
        rect = pygame.Rect(0, 0, config.GRID_WIDTH, config.GRID_HEIGHT)
        pygame.draw.rect(self.screen, config.COLOR_GRID_BACKGROUND, rect)

    def _draw_cell(self, cell: Cell, color: tuple[int, int, int], inset: int = 1) -> None:
        rect = pygame.Rect(cell_to_screen_rect(cell, inset))
        pygame.draw.rect(self.screen, color, rect)

    def _draw_visited(self, visited: set[Cell], path: list[Cell]) -> None:
        path_cells = set(path)
        for cell in visited:
            if cell not in path_cells:
                self._draw_cell(cell, config.COLOR_VISITED, inset=4)

    def _draw_path(self, path: list[Cell]) -> None:
        for cell in path:
            self._draw_cell(cell, config.COLOR_PATH, inset=3)

    def _draw_obstacles(self, grid_map: GridMap) -> None:
        for cell in grid_map.obstacles:
            self._draw_cell(cell, config.COLOR_OBSTACLE, inset=1)

    def _draw_start_goal(self, grid_map: GridMap) -> None:
        if grid_map.start is not None:
            self._draw_cell(grid_map.start, config.COLOR_START, inset=2)

        if grid_map.goal is not None:
            self._draw_cell(grid_map.goal, config.COLOR_GOAL, inset=2)

    def _draw_grid_lines(self) -> None:
        for x in range(0, config.GRID_WIDTH + 1, config.CELL_SIZE):
            pygame.draw.line(
                self.screen,
                config.COLOR_GRID_LINE,
                (x, 0),
                (x, config.GRID_HEIGHT),
            )

        for y in range(0, config.GRID_HEIGHT + 1, config.CELL_SIZE):
            pygame.draw.line(
                self.screen,
                config.COLOR_GRID_LINE,
                (0, y),
                (config.GRID_WIDTH, y),
            )

    def _draw_robot(self, state: AppState) -> None:
        robot = state.robot
        if robot.position is None:
            return

        if len(robot.trail) > 1:
            points = [world_to_screen(position) for position in robot.trail]
            pygame.draw.lines(self.screen, config.COLOR_ROBOT_TRAIL, False, points, 3)

        center = world_to_screen(robot.position)
        radius = max(config.CELL_SIZE // 3, 8)
        pygame.draw.circle(self.screen, config.COLOR_ROBOT, center, radius)
        pygame.draw.circle(self.screen, (120, 53, 15), center, radius, width=2)

        heading = (math.cos(robot.angle), math.sin(robot.angle))
        end = (
            int(center[0] + heading[0] * radius * 1.4),
            int(center[1] + heading[1] * radius * 1.4),
        )
        pygame.draw.line(self.screen, (120, 53, 15), center, end, 3)

    def _robot_heading(self, state: AppState) -> tuple[float, float] | None:
        robot = state.robot
        if len(state.path) < 2:
            return None

        start = state.path[min(robot.path_index, len(state.path) - 1)]
        end = state.path[min(robot.path_index + 1, len(state.path) - 1)]
        delta_row = end[0] - start[0]
        delta_col = end[1] - start[1]
        length = (delta_row * delta_row + delta_col * delta_col) ** 0.5
        if length == 0:
            return None
        return delta_col / length, delta_row / length
