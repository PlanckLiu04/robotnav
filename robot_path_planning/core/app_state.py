"""Application state that changes during user interaction."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from robot_path_planning.core.grid_map import Cell


class EditMode(str, Enum):
    OBSTACLE = "obstacle"
    START = "start"
    GOAL = "goal"


class ScreenMode(str, Enum):
    HOME = "home"
    RUN = "run"


@dataclass
class AlgorithmStats:
    name: str = "-"
    elapsed_ms: float = 0.0
    visited_count: int = 0
    path_length: int = 0
    found: bool = False


@dataclass
class RobotState:
    active: bool = False
    finished: bool = False
    path_index: int = 0
    progress: float = 0.0
    position: tuple[float, float] | None = None
    trail: list[tuple[float, float]] = field(default_factory=list)

    def reset(self) -> None:
        self.active = False
        self.finished = False
        self.path_index = 0
        self.progress = 0.0
        self.position = None
        self.trail.clear()


@dataclass
class AppState:
    screen: ScreenMode = ScreenMode.HOME
    mode: EditMode = EditMode.OBSTACLE
    edit_menu_open: bool = False
    algorithm_menu_open: bool = False
    path: list[Cell] = field(default_factory=list)
    visited: set[Cell] = field(default_factory=set)
    status: str = "Draw obstacles, then set start and goal."
    selected_algorithm: str = "BFS"
    stats: AlgorithmStats = field(default_factory=AlgorithmStats)
    robot: RobotState = field(default_factory=RobotState)

    def clear_search(self) -> None:
        self.path.clear()
        self.visited.clear()
        self.stats = AlgorithmStats(name=self.selected_algorithm)
        self.robot.reset()

    def set_mode(self, mode: EditMode) -> None:
        self.mode = mode
        self.edit_menu_open = False
        self.algorithm_menu_open = False
        mode_label = mode.value.capitalize()
        self.status = f"{mode_label} mode selected."

    def enter_run_screen(self) -> None:
        self.screen = ScreenMode.RUN
        self.edit_menu_open = False
        self.algorithm_menu_open = False
        self.status = "Ready. Edit the map or run a planner."

    def enter_home_screen(self) -> None:
        self.screen = ScreenMode.HOME
        self.edit_menu_open = False
        self.algorithm_menu_open = False

    def select_algorithm(self, name: str) -> None:
        self.selected_algorithm = name
        self.edit_menu_open = False
        self.algorithm_menu_open = False
        self.stats = AlgorithmStats(name=name)
        self.status = f"{name} selected."

    def close_menus(self) -> None:
        self.edit_menu_open = False
        self.algorithm_menu_open = False
