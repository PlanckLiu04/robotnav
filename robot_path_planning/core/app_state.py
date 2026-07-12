"""Application state that changes during user interaction."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from robot_path_planning.core.coordinates import WorldPosition
from robot_path_planning.core.grid_map import Cell

MapSignature = tuple[tuple[Cell, ...], Optional[Cell], Optional[Cell]]


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
class PlannerHistoryEntry:
    map_id: int
    name: str
    elapsed_ms: float
    visited_count: int
    path_length: int
    found: bool
    path: list[Cell] = field(default_factory=list)
    visited: set[Cell] = field(default_factory=set)
    obstacles: set[Cell] = field(default_factory=set)
    start: Cell | None = None
    goal: Cell | None = None


@dataclass
class RobotState:
    active: bool = False
    finished: bool = False
    blocked: bool = False
    path_index: int = 0
    progress: float = 0.0
    physics_accumulator: float = 0.0
    position: WorldPosition | None = None
    angle: float = 0.0
    tracking_target_index: int = 0
    tracking_target_distance: float = 0.0
    segment_progress: float = 0.0
    cross_track_error: float = 0.0
    speed: float = 0.0
    angular_velocity: float = 0.0
    force: WorldPosition = (0.0, 0.0)
    torque: float = 0.0
    aligning_heading: bool = False
    heading_error: float = 0.0
    stuck_timer: float = 0.0
    stuck_warnings: int = 0
    last_target_distance: float | None = None
    trail: list[WorldPosition] = field(default_factory=list)

    def reset(self) -> None:
        self.active = False
        self.finished = False
        self.blocked = False
        self.path_index = 0
        self.progress = 0.0
        self.physics_accumulator = 0.0
        self.position = None
        self.angle = 0.0
        self.tracking_target_index = 0
        self.tracking_target_distance = 0.0
        self.segment_progress = 0.0
        self.cross_track_error = 0.0
        self.speed = 0.0
        self.angular_velocity = 0.0
        self.force = (0.0, 0.0)
        self.torque = 0.0
        self.aligning_heading = False
        self.heading_error = 0.0
        self.stuck_timer = 0.0
        self.stuck_warnings = 0
        self.last_target_distance = None
        self.trail.clear()


@dataclass
class SearchAnimationState:
    active: bool = False
    visited_order: list[Cell] = field(default_factory=list)
    final_path: list[Cell] = field(default_factory=list)
    final_visited: set[Cell] = field(default_factory=set)
    map_obstacles: set[Cell] = field(default_factory=set)
    map_start: Cell | None = None
    map_goal: Cell | None = None
    index: int = 0
    timer: float = 0.0

    def start(
        self,
        visited_order: list[Cell],
        final_path: list[Cell],
        final_visited: set[Cell],
        map_obstacles: set[Cell],
        map_start: Cell | None,
        map_goal: Cell | None,
    ) -> None:
        self.active = bool(visited_order)
        self.visited_order = list(visited_order)
        self.final_path = list(final_path)
        self.final_visited = set(final_visited)
        self.map_obstacles = set(map_obstacles)
        self.map_start = map_start
        self.map_goal = map_goal
        self.index = 0
        self.timer = 0.0

    def reset(self) -> None:
        self.active = False
        self.visited_order.clear()
        self.final_path.clear()
        self.final_visited.clear()
        self.map_obstacles.clear()
        self.map_start = None
        self.map_goal = None
        self.index = 0
        self.timer = 0.0


@dataclass
class AppState:
    screen: ScreenMode = ScreenMode.HOME
    mode: EditMode = EditMode.OBSTACLE
    edit_menu_open: bool = False
    algorithm_menu_open: bool = False
    panel_scroll_y: int = 0
    path: list[Cell] = field(default_factory=list)
    visited: set[Cell] = field(default_factory=set)
    status: str = "Draw obstacles, then set start and goal."
    selected_algorithm: str = "BFS"
    stats: AlgorithmStats = field(default_factory=AlgorithmStats)
    planner_history: list[PlannerHistoryEntry] = field(default_factory=list)
    map_ids: dict[MapSignature, int] = field(default_factory=dict)
    next_map_id: int = 1
    robot: RobotState = field(default_factory=RobotState)
    search_animation: SearchAnimationState = field(default_factory=SearchAnimationState)

    def clear_search(self) -> None:
        self.path.clear()
        self.visited.clear()
        self.stats = AlgorithmStats(name=self.selected_algorithm)
        self.robot.reset()
        self.search_animation.reset()

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

    def add_planner_history(
        self,
        obstacles: set[Cell],
        start: Cell | None,
        goal: Cell | None,
    ) -> None:
        if self.stats.name == "-":
            return

        map_id = self.resolve_map_id(obstacles, start, goal)
        self.planner_history.append(
            PlannerHistoryEntry(
                map_id=map_id,
                name=self.stats.name,
                elapsed_ms=self.stats.elapsed_ms,
                visited_count=self.stats.visited_count,
                path_length=self.stats.path_length,
                found=self.stats.found,
                path=list(self.path),
                visited=set(self.visited),
                obstacles=set(obstacles),
                start=start,
                goal=goal,
            )
        )
        if len(self.planner_history) > 20:
            del self.planner_history[:-20]

    def resolve_map_id(
        self,
        obstacles: set[Cell],
        start: Cell | None,
        goal: Cell | None,
    ) -> int:
        signature = _map_signature(obstacles, start, goal)
        if signature not in self.map_ids:
            self.map_ids[signature] = self.next_map_id
            self.next_map_id += 1
        return self.map_ids[signature]

    def restore_planner_history(self, index: int) -> PlannerHistoryEntry | None:
        if index < 0 or index >= len(self.planner_history):
            return None

        entry = self.planner_history[index]
        self.search_animation.reset()
        self.robot.reset()
        self.selected_algorithm = entry.name
        self.stats = AlgorithmStats(
            name=entry.name,
            elapsed_ms=entry.elapsed_ms,
            visited_count=entry.visited_count,
            path_length=entry.path_length,
            found=entry.found,
        )
        self.path = list(entry.path)
        self.visited = set(entry.visited)
        result = "path" if entry.found else "no path"
        self.status = f"Restored M{entry.map_id} {entry.name} run: {result}."
        return entry


def _map_signature(
    obstacles: set[Cell],
    start: Cell | None,
    goal: Cell | None,
) -> MapSignature:
    return tuple(sorted(obstacles)), start, goal
