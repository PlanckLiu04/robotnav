"""Pygame screens and right-side control panel."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from robot_path_planning import config
from robot_path_planning.core.app_state import AppState, EditMode, PlannerHistoryEntry
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
        self.font = get_font(20)
        self.small_font = get_font(17)
        self.tiny_font = get_font(15)
        self.title_font = get_font(30, bold=True)
        self.hero_font = get_font(54, bold=True)
        self.line_height = 19
        self._mouse_position = (0, 0)
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
        height = 32

        return [
            Button(pygame.Rect(left, 174, width, height), "Run Planner", "run_search", "Space"),
            Button(pygame.Rect(left, 212, width, height), "Start Robot", "start_robot", "S"),
            Button(pygame.Rect(left, 258, width, height), "Random Map", "random_map", "R"),
            Button(pygame.Rect(left, 296, half_width, height), "Clear", "clear", "C"),
            Button(pygame.Rect(left + half_width + 10, 296, half_width, height), "Home", "home", "H"),
        ]

    def handle_click(self, position: tuple[int, int], state: AppState | None = None) -> str | None:
        if state is not None:
            content_position = self._to_content_position(position, state)
            action = self._handle_select_click(content_position, state)
            if action is not None:
                return action
            action = self._handle_history_click(content_position, state)
            if action is not None:
                return action

        buttons = self.home_buttons if state is None else self.buttons
        test_position = position if state is None else self._to_content_position(position, state)
        for button in buttons:
            if button.contains(test_position):
                return button.action
        return "close_menus" if state is not None else None

    def handle_scroll(self, amount: int, state: AppState) -> None:
        content_height = self._content_height(state)
        max_scroll = max(0, content_height - config.WINDOW_HEIGHT)
        state.panel_scroll_y = _clamp(state.panel_scroll_y - amount * 44, 0, max_scroll)

    def draw_home(self, screen: pygame.Surface) -> None:
        self._mouse_position = pygame.mouse.get_pos()
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
        content_height = self._content_height(state)
        max_scroll = max(0, content_height - config.WINDOW_HEIGHT)
        state.panel_scroll_y = _clamp(state.panel_scroll_y, 0, max_scroll)
        self._mouse_position = self._to_content_position(pygame.mouse.get_pos(), state)

        content = pygame.Surface((config.WINDOW_WIDTH, content_height))
        content.fill(config.COLOR_PANEL)
        pygame.draw.line(content, config.COLOR_PANEL_BORDER, (self.x, 0), (self.x, content_height), 2)

        self._draw_selects(content, state)
        self._draw_group_label(content, "Actions", 154)
        self._draw_buttons(content)
        self._draw_group_label(content, "Results", 360)
        self._draw_status(content, grid_map, state)
        self._draw_metrics(content, state)
        self._draw_simulation(content, state)
        self._draw_history(content, state)
        self._draw_open_select_options(content, state)

        source = pygame.Rect(self.x, state.panel_scroll_y, self.width, config.WINDOW_HEIGHT)
        screen.blit(content, (self.x, 0), source)
        self._draw_scrollbar(screen, state, content_height)

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

    def _handle_history_click(self, position: tuple[int, int], state: AppState) -> str | None:
        for history_index, rect, _ in self._history_rows(state):
            if rect.collidepoint(position):
                return f"restore_history_{history_index}"
        return None

    def _select_boxes(self, state: AppState) -> tuple[SelectBox, SelectBox]:
        left = self.x + self.margin
        width = self.width - self.margin * 2
        height = 38
        edit_select = SelectBox(
            pygame.Rect(left, 36, width, height),
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
            pygame.Rect(left, 102, width, height),
            "Path Planner",
            state.selected_algorithm,
            "toggle_algorithm_menu",
            [
                ("BFS", "select_bfs"),
                ("A*", "select_astar"),
                ("DFS", "select_dfs"),
                ("Dijkstra", "select_dijkstra"),
                ("Greedy", "select_greedy"),
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
        mouse_pos = self._mouse_position
        for button in self.home_buttons:
            color = config.COLOR_BUTTON_ACTIVE if button.contains(mouse_pos) else (37, 99, 235)
            pygame.draw.rect(screen, color, button.rect, border_radius=8)
            label = f"{button.label}  [{button.hotkey}]"
            text = self.font.render(label, True, (255, 255, 255))
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
        self._draw_text(screen, select.value, self.small_font, (select.rect.x + 14, select.rect.y + 8))
        arrow = "v" if not select.expanded else "^"
        self._draw_text(screen, arrow, self.small_font, (select.rect.right - 28, select.rect.y + 8), config.COLOR_TEXT_MUTED)

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
        mouse_pos = self._mouse_position

        for button in self.buttons:
            color = config.COLOR_BUTTON_HOVER if button.contains(mouse_pos) else config.COLOR_BUTTON
            text_color = config.COLOR_TEXT
            if button.action == "run_search":
                color = config.COLOR_BUTTON_ACTIVE if not button.contains(mouse_pos) else (59, 130, 246)
                text_color = (255, 255, 255)
            if button.action == "clear":
                color = config.COLOR_DANGER if button.contains(mouse_pos) else config.COLOR_BUTTON
                text_color = (255, 255, 255) if button.contains(mouse_pos) else config.COLOR_TEXT

            pygame.draw.rect(screen, color, button.rect, border_radius=6)
            pygame.draw.rect(screen, config.COLOR_PANEL_BORDER, button.rect, width=1, border_radius=6)

            label = button.label
            if button.hotkey:
                label = f"{button.label}  [{button.hotkey}]"
            self._draw_centered_text(screen, label, self.small_font, button.rect, text_color)

    def _draw_status(self, screen: pygame.Surface, grid_map: GridMap, state: AppState) -> None:
        top = 384
        self._draw_section_header(screen, "Current State", top)
        lines = [
            f"Mode: {_edit_mode_label(state.mode)}",
            f"Walls: {len(grid_map.obstacles)}",
            f"Start: {_format_cell(grid_map.start)}",
            f"Goal: {_format_cell(grid_map.goal)}",
        ]
        self._draw_lines(screen, lines, self.x + self.margin, top + 36, max_lines=4)

    def _draw_metrics(self, screen: pygame.Surface, state: AppState) -> None:
        top = 384
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
        top = 518
        self._draw_section_header(screen, "Simulation", top, width=self.width - self.margin * 2)
        status = "running" if state.robot.active else "finished" if state.robot.finished else "idle"
        self._draw_lines(screen, [f"Robot: {status}"], self.x + self.margin, top + 36, max_lines=1, width=self.width - self.margin * 2)
        self._draw_message(screen, state.status, self.x + self.margin, top + 58, self.width - self.margin * 2, max_lines=2)

    def _draw_history(self, screen: pygame.Surface, state: AppState) -> None:
        top = 626
        self._draw_section_header(screen, "Recent Runs", top, width=self.width - self.margin * 2)
        if not state.planner_history:
            self._draw_lines(screen, ["No planner runs yet."], self.x + self.margin, top + 38, max_lines=1, width=self.width - self.margin * 2)
            return

        mouse_pos = self._mouse_position
        for _, rect, entry in self._history_rows(state):
            color = (255, 255, 255) if not rect.collidepoint(mouse_pos) else (242, 242, 247)
            pygame.draw.rect(screen, color, rect, border_radius=7)
            pygame.draw.rect(screen, config.COLOR_PANEL_BORDER, rect, width=1, border_radius=7)
            self._draw_text(screen, _format_history_entry(entry), self.tiny_font, (rect.x + 10, rect.y + 8), config.COLOR_TEXT)

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

    def _history_rows(self, state: AppState) -> list[tuple[int, pygame.Rect, PlannerHistoryEntry]]:
        left = self.x + self.margin
        width = self.width - self.margin * 2
        row_height = 31
        top = 664
        rows: list[tuple[int, pygame.Rect, PlannerHistoryEntry]] = []
        latest_entries = list(enumerate(state.planner_history))
        for display_index, (history_index, entry) in enumerate(reversed(latest_entries)):
            rect = pygame.Rect(left, top + display_index * (row_height + 8), width, row_height)
            rows.append((history_index, rect, entry))
        return rows

    def _content_height(self, state: AppState) -> int:
        history_count = max(len(state.planner_history), 1)
        history_bottom = 664 + history_count * 39 + self.margin
        return max(config.WINDOW_HEIGHT, history_bottom)

    def _to_content_position(self, position: tuple[int, int], state: AppState) -> tuple[int, int]:
        x, y = position
        return x, y + state.panel_scroll_y

    def _draw_scrollbar(self, screen: pygame.Surface, state: AppState, content_height: int) -> None:
        if content_height <= config.WINDOW_HEIGHT:
            return

        track_height = config.WINDOW_HEIGHT - 18
        track = pygame.Rect(self.x + self.width - 7, 9, 3, track_height)
        thumb_height = max(42, int(track_height * config.WINDOW_HEIGHT / content_height))
        max_scroll = content_height - config.WINDOW_HEIGHT
        thumb_y = track.y + int((track_height - thumb_height) * state.panel_scroll_y / max_scroll)
        thumb = pygame.Rect(track.x, thumb_y, track.width, thumb_height)
        pygame.draw.rect(screen, (218, 218, 222), track, border_radius=2)
        pygame.draw.rect(screen, (142, 142, 147), thumb, border_radius=2)

    def _draw_centered_text(
        self,
        screen: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        rect: pygame.Rect,
        color: tuple[int, int, int] = config.COLOR_TEXT,
    ) -> None:
        surface = font.render(text, True, color)
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


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


def _format_history_entry(entry: PlannerHistoryEntry) -> str:
    result = "OK" if entry.found else "No"
    return (
        f"M{entry.map_id} {entry.name} {result} "
        f"{entry.elapsed_ms:.1f}ms V{entry.visited_count} P{entry.path_length}"
    )
