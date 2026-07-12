"""RobotNav application entry point."""

from __future__ import annotations

from pathlib import Path
import math
import sys
import time

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

import pygame

from robot_path_planning import config
from robot_path_planning.control import (
    PathTracker,
    PathTrackerConfig,
    WaypointForceController,
    WaypointForceControllerConfig,
)
from robot_path_planning.core.app_state import AlgorithmStats, AppState, EditMode, ScreenMode
from robot_path_planning.core.coordinates import cell_center_to_world, distance
from robot_path_planning.core.grid_map import GridMap
from robot_path_planning.planning.astar import astar
from robot_path_planning.planning.bfs import bfs
from robot_path_planning.planning.dfs import dfs
from robot_path_planning.planning.dijkstra import dijkstra
from robot_path_planning.planning.greedy import greedy_best_first
from robot_path_planning.physics import PhysicsWorld, RobotPhysicsConfig
from robot_path_planning.rendering.renderer import Renderer
from robot_path_planning.ui.panel import SidePanel

PLANNERS = {
    "BFS": bfs,
    "A*": astar,
    "DFS": dfs,
    "Dijkstra": dijkstra,
    "Greedy": greedy_best_first,
}


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()

    grid_map = GridMap()
    state = AppState()
    physics_world = PhysicsWorld()
    path_tracker = PathTracker(
        PathTrackerConfig(
            waypoint_tolerance=config.ROBOT_WAYPOINT_TOLERANCE_CELLS,
            lookahead_distance=config.ROBOT_SEGMENT_LOOKAHEAD_CELLS,
            recapture_distance=config.ROBOT_SEGMENT_RECAPTURE_DISTANCE_CELLS,
            recapture_progress_margin=config.ROBOT_SEGMENT_RECAPTURE_PROGRESS_MARGIN,
        )
    )
    waypoint_controller = WaypointForceController(
        WaypointForceControllerConfig(
            drive_force=config.ROBOT_DRIVE_FORCE,
            damping_force=config.ROBOT_DAMPING_FORCE,
            cross_track_gain=config.ROBOT_CROSS_TRACK_GAIN,
            cross_track_damping=config.ROBOT_CROSS_TRACK_DAMPING,
            max_cross_track_force=config.ROBOT_MAX_CROSS_TRACK_FORCE,
            max_force=config.ROBOT_MAX_FORCE,
            arrival_slowdown_radius=config.ROBOT_ARRIVAL_SLOWDOWN_RADIUS_CELLS,
            path_deviation_slowdown=config.ROBOT_PATH_DEVIATION_SLOWDOWN_CELLS,
            path_deviation_stop=config.ROBOT_PATH_DEVIATION_STOP_CELLS,
            heading_gate_power=config.ROBOT_HEADING_GATE_POWER,
            heading_kp=config.ROBOT_HEADING_PID_KP,
            heading_ki=config.ROBOT_HEADING_PID_KI,
            heading_kd=config.ROBOT_HEADING_PID_KD,
            max_torque=config.ROBOT_MAX_TORQUE,
        )
    )
    panel = SidePanel()
    renderer = Renderer(screen, panel)
    drag_action: bool | None = None
    last_drag_cell = None

    running = True
    while running:
        pygame.display.set_caption(_build_window_title(state))
        dt = clock.tick(config.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                _handle_keydown(
                    event.key,
                    grid_map,
                    state,
                    physics_world,
                    path_tracker,
                    waypoint_controller,
                )
            elif event.type == pygame.MOUSEWHEEL:
                _handle_mouse_wheel(event.y, state, panel)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drag_action, last_drag_cell = _handle_mouse_down(
                    event.pos,
                    grid_map,
                    state,
                    panel,
                    physics_world,
                    path_tracker,
                    waypoint_controller,
                )
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drag_action = None
                last_drag_cell = None
            elif event.type == pygame.MOUSEMOTION and drag_action is not None:
                last_drag_cell = _handle_mouse_drag(
                    event.pos,
                    drag_action,
                    last_drag_cell,
                    grid_map,
                    state,
                )

        _update_search_animation(state, dt)
        _update_robot(state, physics_world, path_tracker, waypoint_controller, dt)
        renderer.draw(grid_map, state)
        pygame.display.flip()

    pygame.quit()


def _handle_keydown(
    key: int,
    grid_map: GridMap,
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
) -> None:
    if state.screen == ScreenMode.HOME:
        if key in (pygame.K_RETURN, pygame.K_SPACE):
            state.enter_run_screen()
        return

    if key == pygame.K_1:
        state.set_mode(EditMode.OBSTACLE)
    elif key == pygame.K_2:
        state.set_mode(EditMode.START)
    elif key == pygame.K_3:
        state.set_mode(EditMode.GOAL)
    elif key == pygame.K_SPACE:
        _run_search(grid_map, state)
    elif key == pygame.K_c:
        _clear_all(grid_map, state, physics_world, path_tracker, waypoint_controller)
    elif key == pygame.K_r:
        _generate_random_map(grid_map, state, physics_world, path_tracker)
    elif key == pygame.K_TAB:
        _toggle_algorithm(state)
    elif key == pygame.K_s:
        _start_robot(grid_map, state, physics_world, path_tracker, waypoint_controller)
    elif key == pygame.K_h:
        state.enter_home_screen()


def _handle_mouse_wheel(amount: int, state: AppState, panel: SidePanel) -> None:
    if state.screen != ScreenMode.RUN:
        return

    mouse_x, _ = pygame.mouse.get_pos()
    if mouse_x >= config.GRID_WIDTH:
        panel.handle_scroll(amount, state)


def _handle_mouse_down(
    position: tuple[int, int],
    grid_map: GridMap,
    state: AppState,
    panel: SidePanel,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
) -> tuple[bool | None, tuple[int, int] | None]:
    if state.screen == ScreenMode.HOME:
        _handle_home_action(panel.handle_click(position), state)
        return None, None

    if position[0] >= config.GRID_WIDTH:
        _handle_panel_action(
            panel.handle_click(position, state),
            grid_map,
            state,
            physics_world,
            path_tracker,
            waypoint_controller,
        )
        return None, None

    state.close_menus()

    cell = grid_map.pixel_to_cell(position)
    if cell is None:
        return None, None

    if state.mode == EditMode.OBSTACLE:
        drag_action = cell not in grid_map.obstacles
        _edit_obstacle_cell(cell, drag_action, grid_map, state)
        return drag_action, cell

    changed = False
    if state.mode == EditMode.START:
        changed = grid_map.set_start(cell)
    elif state.mode == EditMode.GOAL:
        changed = grid_map.set_goal(cell)

    if changed:
        state.clear_search()
        state.status = "Map changed. Search result cleared."
    else:
        state.status = "That cell cannot be changed in this mode."
    return None, None


def _handle_mouse_drag(
    position: tuple[int, int],
    drag_action: bool,
    last_drag_cell: tuple[int, int] | None,
    grid_map: GridMap,
    state: AppState,
) -> tuple[int, int] | None:
    if position[0] >= config.GRID_WIDTH:
        return last_drag_cell

    cell = grid_map.pixel_to_cell(position)
    if cell is None or cell == last_drag_cell:
        return last_drag_cell

    _edit_obstacle_cell(cell, drag_action, grid_map, state)
    return cell


def _edit_obstacle_cell(
    cell: tuple[int, int],
    blocked: bool,
    grid_map: GridMap,
    state: AppState,
) -> None:
    changed = grid_map.set_obstacle(cell, blocked)
    if changed:
        state.clear_search()
        action = "added" if blocked else "removed"
        state.status = f"Obstacle {action}. Search result cleared."


def _handle_panel_action(
    action: str | None,
    grid_map: GridMap,
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
) -> None:
    if action is None:
        return

    if action.startswith("restore_history_"):
        _restore_history(action, grid_map, state)
        physics_world.clear()
        path_tracker.clear()
    elif action == "toggle_edit_menu":
        state.edit_menu_open = not state.edit_menu_open
        state.algorithm_menu_open = False
    elif action == "toggle_algorithm_menu":
        state.algorithm_menu_open = not state.algorithm_menu_open
        state.edit_menu_open = False
    elif action == "close_menus":
        state.close_menus()
    elif action == "mode_obstacle":
        state.set_mode(EditMode.OBSTACLE)
    elif action == "mode_start":
        state.set_mode(EditMode.START)
    elif action == "mode_goal":
        state.set_mode(EditMode.GOAL)
    elif action == "select_bfs":
        _select_algorithm(state, "BFS")
    elif action == "select_astar":
        _select_algorithm(state, "A*")
    elif action == "select_dfs":
        _select_algorithm(state, "DFS")
    elif action == "select_dijkstra":
        _select_algorithm(state, "Dijkstra")
    elif action == "select_greedy":
        _select_algorithm(state, "Greedy")
    elif action == "run_search":
        _run_search(grid_map, state)
    elif action == "start_robot":
        _start_robot(grid_map, state, physics_world, path_tracker, waypoint_controller)
    elif action == "random_map":
        _generate_random_map(grid_map, state, physics_world, path_tracker)
    elif action == "clear":
        _clear_all(grid_map, state, physics_world, path_tracker, waypoint_controller)
    elif action == "home":
        state.enter_home_screen()


def _handle_home_action(action: str | None, state: AppState) -> None:
    if action == "enter_run":
        state.enter_run_screen()


def _restore_history(action: str, grid_map: GridMap, state: AppState) -> None:
    try:
        history_index = int(action.removeprefix("restore_history_"))
    except ValueError:
        return

    entry = state.restore_planner_history(history_index)
    if entry is None:
        return

    grid_map.obstacles = set(entry.obstacles)
    grid_map.start = entry.start
    grid_map.goal = entry.goal


def _run_search(grid_map: GridMap, state: AppState) -> None:
    if grid_map.start is None or grid_map.goal is None:
        state.clear_search()
        state.status = "Set both start and goal before searching."
        return

    started_at = time.perf_counter()
    planner = PLANNERS.get(state.selected_algorithm, bfs)
    result = planner(grid_map, grid_map.start, grid_map.goal)
    elapsed_ms = (time.perf_counter() - started_at) * 1000.0
    clearance = _path_min_clearance(result.path, grid_map.obstacles) if result.found else None

    state.path = []
    state.visited = set()
    state.stats = AlgorithmStats(
        name=state.selected_algorithm,
        elapsed_ms=elapsed_ms,
        visited_count=len(result.visited),
        path_length=max(len(result.path) - 1, 0),
        found=result.found,
    )
    state.robot.reset()

    if result.visited_order:
        state.search_animation.start(
            result.visited_order,
            result.path,
            result.visited,
            grid_map.obstacles,
            grid_map.start,
            grid_map.goal,
        )
        state.status = _planner_success_status(
            state.selected_algorithm,
            state.stats.path_length,
            clearance,
            suffix="animation running.",
        )
    elif result.found:
        state.path = result.path
        state.visited = result.visited
        state.add_planner_history(grid_map.obstacles, grid_map.start, grid_map.goal)
        state.status = _planner_success_status(
            state.selected_algorithm,
            state.stats.path_length,
            clearance,
            suffix="path ready.",
        )
    else:
        state.visited = result.visited
        state.add_planner_history(grid_map.obstacles, grid_map.start, grid_map.goal)
        state.status = f"{state.selected_algorithm}: no path found."


def _clear_all(
    grid_map: GridMap,
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
) -> None:
    grid_map.clear()
    state.clear_search()
    physics_world.clear()
    path_tracker.clear()
    state.status = "Map cleared."


def _generate_random_map(
    grid_map: GridMap,
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
) -> None:
    grid_map.generate_random(config.RANDOM_OBSTACLE_DENSITY)
    state.clear_search()
    physics_world.clear()
    path_tracker.clear()
    obstacle_count = len(grid_map.obstacles)
    state.status = f"Random map generated with {obstacle_count} obstacles."


def _select_algorithm(state: AppState, name: str) -> None:
    state.select_algorithm(name)
    state.clear_search()


def _toggle_algorithm(state: AppState) -> None:
    algorithms = list(PLANNERS)
    current_index = algorithms.index(state.selected_algorithm) if state.selected_algorithm in algorithms else 0
    next_algorithm = algorithms[(current_index + 1) % len(algorithms)]
    _select_algorithm(state, next_algorithm)


def _start_robot(
    grid_map: GridMap,
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
) -> None:
    if state.search_animation.active:
        state.status = "Wait for search animation to finish."
        return

    if len(state.path) < 2:
        state.status = "Run a planner before starting the robot."
        return

    first_cell = state.path[0]
    start_position = cell_center_to_world(first_cell)
    state.robot.reset()
    path_tracker.reset(state.path)
    waypoint_controller.reset()
    physics_world.reset(
        grid_map.obstacles,
        start_position,
        RobotPhysicsConfig(
            mass=config.ROBOT_MASS,
            radius=config.ROBOT_RADIUS_CELLS,
        ),
    )
    state.robot.active = True
    state.robot.position = start_position
    state.robot.angle = 0.0
    state.robot.aligning_heading = True
    state.robot.trail.append(state.robot.position)
    state.status = "Physics robot simulation running."


def _initial_path_angle(path: list[tuple[int, int]]) -> float:
    if len(path) < 2:
        return 0.0

    start = cell_center_to_world(path[0])
    next_point = cell_center_to_world(path[1])
    return math.atan2(next_point[1] - start[1], next_point[0] - start[0])


def _update_search_animation(state: AppState, dt: float) -> None:
    animation = state.search_animation
    if not animation.active:
        return

    interval = 1.0 / config.SEARCH_ANIMATION_CELLS_PER_SECOND
    animation.timer += dt

    while animation.active and animation.timer >= interval:
        animation.timer -= interval
        _reveal_next_search_cell(state)


def _reveal_next_search_cell(state: AppState) -> None:
    animation = state.search_animation
    if animation.index < len(animation.visited_order):
        state.visited.add(animation.visited_order[animation.index])
        animation.index += 1

    if animation.index >= len(animation.visited_order):
        _finish_search_animation(state)


def _finish_search_animation(state: AppState) -> None:
    animation = state.search_animation
    final_path = list(animation.final_path)
    final_visited = set(animation.final_visited)
    map_obstacles = set(animation.map_obstacles)
    map_start = animation.map_start
    map_goal = animation.map_goal
    animation.reset()

    state.path = final_path
    state.visited = final_visited
    state.add_planner_history(map_obstacles, map_start, map_goal)

    if state.stats.found:
        clearance = _path_min_clearance(final_path, map_obstacles)
        state.status = _planner_success_status(
            state.stats.name,
            state.stats.path_length,
            clearance,
            suffix="path ready.",
        )
    else:
        state.status = f"{state.stats.name}: no path found."


def _update_robot(
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
    dt: float,
) -> None:
    robot = state.robot
    if not robot.active or len(state.path) < 2:
        return

    robot.physics_accumulator = min(
        robot.physics_accumulator + dt,
        config.PHYSICS_TIME_STEP * config.MAX_PHYSICS_STEPS_PER_FRAME,
    )

    steps = 0
    while robot.active and robot.physics_accumulator >= config.PHYSICS_TIME_STEP:
        _step_robot_physics(
            state,
            physics_world,
            path_tracker,
            waypoint_controller,
            config.PHYSICS_TIME_STEP,
        )
        robot.physics_accumulator -= config.PHYSICS_TIME_STEP
        steps += 1
        if steps >= config.MAX_PHYSICS_STEPS_PER_FRAME:
            robot.physics_accumulator = 0.0
            break

    _sync_robot_from_physics(state, physics_world)


def _step_robot_physics(
    state: AppState,
    physics_world: PhysicsWorld,
    path_tracker: PathTracker,
    waypoint_controller: WaypointForceController,
    dt: float,
) -> None:
    robot = state.robot
    physics_state = physics_world.robot_state()
    if physics_state is None:
        robot.reset()
        state.status = "Physics robot is not initialized."
        return

    robot.position = physics_state.position
    robot.angle = physics_state.angle
    robot.speed = _vector_length(physics_state.velocity)
    robot.angular_velocity = physics_state.angular_velocity
    target = path_tracker.update(physics_state.position)
    robot.path_index = max(target.waypoint_index - 1, 0)
    robot.tracking_target_index = target.waypoint_index
    robot.tracking_target_distance = target.distance_to_waypoint
    robot.segment_progress = target.segment_progress
    robot.cross_track_error = target.cross_track_error

    if target.finished:
        robot.active = False
        robot.finished = True
        robot.blocked = False
        robot.stuck_timer = 0.0
        robot.last_target_distance = None
        state.status = "Robot reached the goal."
        return

    if target.waypoint is None:
        robot.reset()
        state.status = "Path tracker has no target."
        return

    if _align_robot_heading_before_drive(
        state,
        physics_world,
        waypoint_controller,
        physics_state,
        target.waypoint,
        dt,
    ):
        return

    command = waypoint_controller.compute_command(physics_state, target, dt)
    robot.force = command.force
    robot.torque = command.torque
    physics_world.apply_robot_force(command.force)
    physics_world.apply_robot_torque(command.torque)
    physics_world.step(dt)
    physics_world.limit_robot_speed(config.ROBOT_MAX_SPEED_CELLS_PER_SECOND)

    _sync_robot_from_physics(state, physics_world)
    _update_robot_stuck_diagnostics(state, physics_world, target, dt)


def _align_robot_heading_before_drive(
    state: AppState,
    physics_world: PhysicsWorld,
    waypoint_controller: WaypointForceController,
    physics_state,
    waypoint: tuple[float, float],
    dt: float,
) -> bool:
    """Rotate in place at startup until the robot faces the first path target."""
    robot = state.robot
    desired_heading = math.atan2(
        waypoint[1] - physics_state.position[1],
        waypoint[0] - physics_state.position[0],
    )
    heading_error = _normalize_angle(desired_heading - physics_state.angle)
    robot.heading_error = heading_error

    if not robot.aligning_heading:
        return False

    is_aligned = abs(heading_error) <= config.ROBOT_START_HEADING_TOLERANCE_RADIANS
    is_settled = robot.speed <= config.ROBOT_START_ALIGNMENT_SPEED_THRESHOLD_CELLS_PER_SECOND
    if is_aligned and is_settled:
        robot.aligning_heading = False
        robot.force = (0.0, 0.0)
        robot.torque = 0.0
        waypoint_controller.reset()
        physics_world.stop_robot()
        _sync_robot_from_physics(state, physics_world)
        return False

    torque = waypoint_controller.heading_pid.update(heading_error, dt)
    robot.force = (0.0, 0.0)
    robot.torque = torque
    physics_world.stop_robot_translation()
    physics_world.apply_robot_torque(torque)
    physics_world.step(dt)
    _sync_robot_from_physics(state, physics_world)
    state.status = "Aligning robot heading before driving."
    return True


def _sync_robot_from_physics(state: AppState, physics_world: PhysicsWorld) -> None:
    robot = state.robot
    updated_state = physics_world.robot_state()
    if updated_state is None:
        return

    robot.position = updated_state.position
    robot.angle = updated_state.angle
    robot.speed = _vector_length(updated_state.velocity)
    robot.angular_velocity = updated_state.angular_velocity

    if not robot.trail or distance(robot.trail[-1], robot.position) >= 0.2:
        robot.trail.append(robot.position)


def _vector_length(vector: tuple[float, float]) -> float:
    return (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5


def _normalize_angle(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def _planner_success_status(
    algorithm: str,
    path_length: int,
    clearance: float | None,
    suffix: str,
) -> str:
    base = f"{algorithm} found a path with {path_length} steps; {suffix}"
    if clearance is None:
        return base

    warning_threshold = (
        config.ROBOT_RADIUS_CELLS
        + config.PLANNING_CLEARANCE_WARNING_MARGIN_CELLS
    )
    if clearance < warning_threshold:
        return (
            f"{base} Clearance {clearance:.2f} < robot radius "
            f"{config.ROBOT_RADIUS_CELLS:.2f}; tracking may be tight."
        )
    return f"{base} Clearance {clearance:.2f} cells."


def _path_min_clearance(
    path: list[tuple[int, int]],
    obstacles: set[tuple[int, int]],
) -> float | None:
    """Return the minimum distance from path centerline segments to obstacle squares."""
    if not path or not obstacles:
        return None

    points = [cell_center_to_world(cell) for cell in path]
    if len(points) == 1:
        segments = [(points[0], points[0])]
    else:
        segments = list(zip(points, points[1:]))

    min_clearance: float | None = None
    for start, end in segments:
        for obstacle in obstacles:
            clearance = _segment_to_cell_rect_distance(start, end, obstacle)
            min_clearance = clearance if min_clearance is None else min(min_clearance, clearance)
    return min_clearance


def _segment_to_cell_rect_distance(
    start: tuple[float, float],
    end: tuple[float, float],
    cell: tuple[int, int],
) -> float:
    """Approximate segment-to-cell clearance by sampling along the segment."""
    row, col = cell
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    segment_length = (dx * dx + dy * dy) ** 0.5
    samples = max(2, int(segment_length / 0.1) + 1)
    min_distance = float("inf")

    for index in range(samples):
        t = index / (samples - 1)
        x = start[0] + dx * t
        y = start[1] + dy * t
        min_distance = min(
            min_distance,
            _point_to_rect_distance(x, y, col, row, col + 1.0, row + 1.0),
        )
    return min_distance


def _point_to_rect_distance(
    x: float,
    y: float,
    left: float,
    top: float,
    right: float,
    bottom: float,
) -> float:
    closest_x = min(max(x, left), right)
    closest_y = min(max(y, top), bottom)
    dx = x - closest_x
    dy = y - closest_y
    return (dx * dx + dy * dy) ** 0.5


def _update_robot_stuck_diagnostics(
    state: AppState,
    physics_world: PhysicsWorld,
    target,
    dt: float,
) -> None:
    """Track low-speed/no-progress behavior and stop hard-pushing blocked robots."""
    robot = state.robot
    updated_state = physics_world.robot_state()
    if updated_state is None or target.waypoint is None:
        return

    velocity = updated_state.velocity
    speed = (velocity[0] * velocity[0] + velocity[1] * velocity[1]) ** 0.5
    force = _vector_length(robot.force)
    previous_distance = robot.last_target_distance
    current_distance = target.distance_to_waypoint
    made_progress = (
        previous_distance is None
        or previous_distance - current_distance > config.ROBOT_STUCK_PROGRESS_EPSILON_CELLS
    )

    is_low_speed = speed < config.ROBOT_STUCK_SPEED_THRESHOLD_CELLS_PER_SECOND
    is_high_force = force >= config.ROBOT_BLOCKED_FORCE_THRESHOLD

    if is_low_speed and is_high_force and not made_progress:
        robot.stuck_timer += dt
    else:
        robot.stuck_timer = 0.0

    robot.last_target_distance = current_distance

    if robot.stuck_timer >= config.ROBOT_STUCK_TIMEOUT_SECONDS:
        robot.stuck_warnings += 1
        robot.stuck_timer = 0.0
        robot.active = False
        robot.blocked = True
        robot.force = (0.0, 0.0)
        robot.torque = 0.0
        physics_world.stop_robot()
        state.status = (
            "Robot blocked: low speed despite force. "
            "The physical robot may be wedged against an obstacle or the path is too tight."
        )


def _build_window_title(state: AppState) -> str:
    if state.screen == ScreenMode.HOME:
        return f"{config.TITLE} | Home"
    return f"{config.TITLE} | Mode: {state.mode.value} | {state.status}"


if __name__ == "__main__":
    main()
