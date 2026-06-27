"""Pygame screens and right-side control panel."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from robot_path_planning import config
from robot_path_planning.core.app_state import AppState, EditMode
from robot_path_planning.core.grid_map import GridMap
from robot_path_planning.ui.fonts import get_font


@dataclass
class Button:
    rect: pygame.Rect
    label: str
    action: str
    hotkey: str = ""

    def contains(self, position: tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)


@dataclass
class SelectBox:
    rect: pygame.Rect
    label: str
    value: str
    action: str
    options: list[tuple[str, str]]
    expanded: bool = False

    def option_rect(self, index: int) -> pygame.Rect:
        return pygame.Rect(self.rect.x, self.rect.bottom + index * self.rect.height, self.rect.width, self.rect.height)

    def contains(self, position: tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)


class SidePanel:
    def __init__(self) -> None:
        self.x = config.GRID_WIDTH
        self.width = config.PANEL_WIDTH
        self.margin = 22
        self.font = get_font(22)
        self.small_font = get_font(20)
        self.tiny_font = get_font(18)
        self.title_font = get_font(32, bold=True)
        self.hero_font = get_font(58, bold=True)
        self.line_height = 21
        self.home_buttons = self._create_home_buttons()
        self.buttons = self._create_run_buttons()

    def _create_home_buttons(self) -> list[Button]:
        return [
            Button(
                pygame.Rect(86, 332, 220, 46),
                "Start Lab",
                "enter_run",
                "Enter",
            )
        ]

    def _create_run_buttons(self) -> list[Button]:
        left = self.x + self.margin
        width = self.width - self.margin * 2
        half_width = (width - 10) // 2
        height = 34

        return [
            Button(pygame.Rect(left, 246, width, height), "Run Planner", "run_search", "Space"),
            Button(pygame.Rect(left, 288, width, height), "Start Robot", "start_robot", "S"),
            Button(pygame.Rect(left, 342, width, height), "Random Map", "random_map", "R"),
            Button(pygame.Rect(left, 384, half_width, height), "Clear", "clear", "C"),
            Button(pygame.Rect(left + half_width + 10, 384, half_width, height), "Home", "home", "H"),
        ]

    def handle_click(self, position: tuple[int, int], state: AppState | None = None) -> str | None:
        if state is not None:
            action = self._handle_select_click(position, state)
            if action is not None:
                return action

        for button in self.home_buttons + self.buttons:
            if button.contains(position):
                return button.action
        return "close_menus" if state is not None else None

    def draw_home(self, screen: pygame.Surface) -> None:
        screen.fill((232, 238, 246))
        self._draw_home_grid_preview(screen)
        self._draw_text(screen, "RobotNav", self.hero_font, (72, 116), config.COLOR_DARK_TEXT)
        self._draw_text(
            screen,
            "2D path planning and robot simulation",
            self.font,
            (78, 176),
            (55, 65, 81),
        )
        self._draw_home_buttons(screen)

    def draw(self, screen: pygame.Surface, grid_map: GridMap, state: AppState) -> None:
        panel_rect = pygame.Rect(self.x, 0, self.width, config.WINDOW_HEIGHT)
        pygame.draw.rect(screen, config.COLOR_PANEL, panel_rect)
        pygame.draw.line(screen, config.COLOR_PANEL_BORDER, (self.x, 0), (self.x, config.WINDOW_HEIGHT), 2)

        self._draw_title(screen)
        self._draw_selects(screen, state)
        self._draw_group_label(screen, "Actions", 222)
        self._draw_buttons(screen)
        self._draw_group_label(screen, "Results", 444)
        self._draw_status(screen, grid_map, state)
        self._draw_metrics(screen, state)
        self._draw_simulation(screen, state)
        self._draw_open_select_options(screen, state)

    def _handle_select_click(self, position: tuple[int, int], state: AppState) -> str | None:
        edit_select, algorithm_select = self._select_boxes(state)

        for index, (_, action) in enumerate(edit_select.options):
            if edit_select.expanded and edit_select.option_rect(index).collidepoint(position):
                return action

        for index, (_, action) in enumerate(algorithm_select.options):
            if algorithm_select.expanded and algorithm_select.option_rect(index).collidepoint(position):
                return action

        if edit_select.contains(position):
            return "toggle_edit_menu"
        if algorithm_select.contains(position):
            return "toggle_algorithm_menu"

        return None

    def _select_boxes(self, state: AppState) -> tuple[SelectBox, SelectBox]:
        left = self.x + self.margin
        width = self.width - self.margin * 2
        height = 42
        edit_select = SelectBox(
            pygame.Rect(left, 104, width, height),
            "Edit Mode",
            _edit_mode_label(state.mode),
            "toggle_edit_menu",
            [
                ("Obstacle", "mode_obstacle"),
                ("Start", "mode_start"),
                ("Goal", "mode_goal"),
            ],
            state.edit_menu_open,
        )
        algorithm_select = SelectBox(
            pygame.Rect(left, 182, width, height),
            "Path Planner",
            state.selected_algorithm,
            "toggle_algorithm_menu",
            [
                ("BFS", "select_bfs"),
                ("A*", "select_astar"),
            ],
            state.algorithm_menu_open,
        )
        return edit_select, algorithm_select

    def _draw_home_grid_preview(self, screen: pygame.Surface) -> None:
        rect = pygame.Rect(650, 82, 360, 460)
        pygame.draw.rect(screen, (248, 250, 252), rect, border_radius=8)
        pygame.draw.rect(screen, (148, 163, 184), rect, width=2, border_radius=8)
        for x in range(rect.x + 20, rect.right - 20, 30):
            pygame.draw.line(screen, (226, 232, 240), (x, rect.y + 20), (x, rect.bottom - 20))
        for y in range(rect.y + 20, rect.bottom - 20, 30):
            pygame.draw.line(screen, (226, 232, 240), (rect.x + 20, y), (rect.right - 20, y))

        blocks = [(690, 144), (720, 144), (750, 144), (840, 264), (870, 264), (840, 294), (930, 354)]
        for x, y in blocks:
            pygame.draw.rect(screen, config.COLOR_OBSTACLE, pygame.Rect(x, y, 28, 28), border_radius=3)
        pygame.draw.rect(screen, config.COLOR_START, pygame.Rect(690, 434, 28, 28), border_radius=3)
        pygame.draw.rect(screen, config.COLOR_GOAL, pygame.Rect(960, 144, 28, 28), border_radius=3)
        pygame.draw.lines(
            screen,
            config.COLOR_PATH,
            False,
            [(704, 448), (794, 448), (794, 328), (944, 328), (944, 158), (974, 158)],
            5,
        )
        pygame.draw.circle(screen, config.COLOR_ROBOT, (825, 328), 12)

    def _draw_home_buttons(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for button in self.home_buttons:
            color = config.COLOR_BUTTON_ACTIVE if button.contains(mouse_pos) else (37, 99, 235)
            pygame.draw.rect(screen, color, button.rect, border_radius=8)
            label = f"{button.label}  [{button.hotkey}]"
            text = self.font.render(label, True, config.COLOR_TEXT)
            text_rect = text.get_rect(center=button.rect.center)
            screen.blit(text, text_rect)

    def _draw_title(self, screen: pygame.Surface) -> None:
        self._draw_text(screen, "RobotNav", self.title_font, (self.x + self.margin, 24))
        self._draw_text(
            screen,
            "Run interface",
            self.small_font,
            (self.x + self.margin, 58),
            config.COLOR_TEXT_MUTED,
        )

    def _draw_selects(self, screen: pygame.Surface, state: AppState) -> None:
        edit_select, algorithm_select = self._select_boxes(state)
        self._draw_select(screen, edit_select)
        self._draw_select(screen, algorithm_select)

    def _draw_select(self, screen: pygame.Surface, select: SelectBox) -> None:
        self._draw_text(screen, select.label, self.tiny_font, (select.rect.x, select.rect.y - 26), config.COLOR_TEXT_MUTED)
        pygame.draw.rect(screen, config.COLOR_BUTTON, select.rect, border_radius=6)
        pygame.draw.rect(screen, config.COLOR_PANEL_BORDER, select.rect, width=1, border_radius=6)
        self._draw_text(screen, select.value, self.small_font, (select.rect.x + 14, select.rect.y + 9))
        arrow = "v" if not select.expanded else "^"
        self._draw_text(screen, arrow, self.small_font, (select.rect.right - 28, select.rect.y + 9), config.COLOR_TEXT_MUTED)

    def _draw_open_select_options(self, screen: pygame.Surface, state: AppState) -> None:
        for select in self._select_boxes(state):
            if not select.expanded:
                continue
            for index, (label, _) in enumerate(select.options):
                rect = select.option_rect(index)
                pygame.draw.rect(screen, config.COLOR_PANEL_SECTION, rect)
                pygame.draw.rect(screen, config.COLOR_PANEL_BORDER, rect, width=1)
                self._draw_text(screen, label, self.small_font, (rect.x + 14, rect.y + 9))

    def _draw_buttons(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            color = config.COLOR_BUTTON_HOVER if button.contains(mouse_pos) else config.COLOR_BUTTON
            if button.action == "run_search":
                color = config.COLOR_BUTTON_ACTIVE if not button.contains(mouse_pos) else (59, 130, 246)
            if button.action == "clear":
                color = config.COLOR_DANGER if button.contains(mouse_pos) else config.COLOR_BUTTON

            pygame.draw.rect(screen, color, button.rect, border_radius=6)
            pygame.draw.rect(screen, config.COLOR_PANEL_BORDER, button.rect, width=1, border_radius=6)

            label = button.label
            if button.hotkey:
                label = f"{button.label}  [{button.hotkey}]"
            self._draw_centered_text(screen, label, self.small_font, button.rect)

    def _draw_status(self, screen: pygame.Surface, grid_map: GridMap, state: AppState) -> None:
        top = 470
        self._draw_section_header(screen, "Current State", top)
        lines = [
            f"Mode: {_edit_mode_label(state.mode)}",
            f"Walls: {len(grid_map.obstacles)}",
            f"Start: {_format_cell(grid_map.start)}",
            f"Goal: {_format_cell(grid_map.goal)}",
        ]
        self._draw_lines(screen, lines, self.x + self.margin, top + 36, max_lines=4)

    def _draw_metrics(self, screen: pygame.Surface, state: AppState) -> None:
        top = 470
        x = self.x + self.margin + 148
        self._draw_section_header(screen, "Metrics", top, x=x, width=self.x + self.width - self.margin - x)
        stats = state.stats
        lines = [
            f"Alg: {state.selected_algorithm}",
            f"Time: {stats.elapsed_ms:.2f} ms",
            f"Visited: {stats.visited_count}",
            f"Path: {stats.path_length}",
        ]
        self._draw_lines(screen, lines, x, top + 36, max_lines=4, width=self.x + self.width - self.margin - x)

    def _draw_simulation(self, screen: pygame.Surface, state: AppState) -> None:
        top = 620
        self._draw_section_header(screen, "Simulation", top, width=self.width - self.margin * 2)
        status = "running" if state.robot.active else "finished" if state.robot.finished else "idle"
        self._draw_lines(screen, [f"Robot: {status}"], self.x + self.margin, top + 36, max_lines=1, width=self.width - self.margin * 2)
        self._draw_message(screen, state.status, self.x + self.margin, top + 60, self.width - self.margin * 2, max_lines=2)

    def _draw_group_label(self, screen: pygame.Surface, title: str, y: int) -> None:
        self._draw_text(screen, title, self.tiny_font, (self.x + self.margin, y), config.COLOR_TEXT_MUTED)

    def _draw_section_header(self, screen: pygame.Surface, title: str, y: int, x: int | None = None, width: int = 132) -> None:
        left = self.x + self.margin if x is None else x
        rect = pygame.Rect(left, y, width, 30)
        pygame.draw.rect(screen, config.COLOR_PANEL_SECTION, rect, border_radius=5)
        self._draw_text(screen, title, self.tiny_font, (rect.x + 10, rect.y + 6))

    def _draw_lines(
        self,
        screen: pygame.Surface,
        lines: list[str],
        x: int,
        y: int,
        max_lines: int,
        width: int = 132,
    ) -> None:
        drawn_lines = 0
        for line in lines:
            for chunk in self._wrap_text(line, width):
                if drawn_lines >= max_lines:
                    return
                self._draw_text(screen, chunk, self.tiny_font, (x, y), config.COLOR_TEXT_MUTED)
                y += self.line_height
                drawn_lines += 1

    def _draw_message(self, screen: pygame.Surface, message: str, x: int, y: int, width: int, max_lines: int) -> None:
        chunks = self._wrap_text(f"Msg: {message}", width)
        for index, chunk in enumerate(chunks[:max_lines]):
            if index == max_lines - 1 and len(chunks) > max_lines:
                chunk = _truncate_text(chunk, self.tiny_font, width)
            self._draw_text(screen, chunk, self.tiny_font, (x, y), config.COLOR_TEXT_MUTED)
            y += self.line_height

    def _wrap_text(self, text: str, max_width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""

        for word in words:
            candidate = word if not current else f"{current} {word}"
            if self.tiny_font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines or [text]

    def _draw_centered_text(self, screen: pygame.Surface, text: str, font: pygame.font.Font, rect: pygame.Rect) -> None:
        surface = font.render(text, True, config.COLOR_TEXT)
        screen.blit(surface, surface.get_rect(center=rect.center))

    def _draw_text(
        self,
        screen: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        position: tuple[int, int],
        color: tuple[int, int, int] = config.COLOR_TEXT,
    ) -> None:
        surface = font.render(text, True, color)
        screen.blit(surface, position)


def _format_cell(cell: tuple[int, int] | None) -> str:
    if cell is None:
        return "-"
    return f"{cell[0]},{cell[1]}"


def _edit_mode_label(mode: EditMode) -> str:
    labels = {
        EditMode.OBSTACLE: "Obstacle",
        EditMode.START: "Start",
        EditMode.GOAL: "Goal",
    }
    return labels[mode]


def _truncate_text(text: str, font: pygame.font.Font, max_width: int) -> str:
    ellipsis = "..."
    while text and font.size(text + ellipsis)[0] > max_width:
        text = text[:-1]
    return text + ellipsis if text else ellipsis
