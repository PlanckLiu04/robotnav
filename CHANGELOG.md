# Changelog

本文件记录 RobotNav 项目的阶段性进展，方便回顾每周完成了什么，也方便后续整理项目展示材料。

## Week 1 - 2026-06-27

- Created the initial Python + Pygame prototype.
- Added a runnable 2D simulation window.
- Added grid rendering.
- Added mouse interaction for editing obstacles.
- Added start and goal selection.
- Implemented BFS path planning.
- Added path rendering.
- Added project documentation files for Git-based development.

## Week 2 - 2026-06-27

- Refactored the single-file prototype into feature modules.
- Added `config.py` for shared window, grid, color, and FPS settings.
- Added `core/grid_map.py` for map data, obstacle editing, start/goal editing, and neighbor lookup.
- Added `core/app_state.py` for edit mode, path, visited cells, algorithm name, and status messages.
- Moved BFS into `planning/bfs.py` and added a `SearchResult` object.
- Added `rendering/renderer.py` for grid, obstacle, path, visited-node, start, and goal drawing.
- Added `ui/panel.py` for the right-side interactive UI panel.
- Added clickable UI buttons for obstacle, start, goal, run BFS, and clear actions.
- Added `C` shortcut and UI clear action.
- Added `R` shortcut and UI random-map action.
- Added random generation of obstacles, start, and goal.
- Added click-and-drag obstacle painting and erasing.
- Added a startup home screen with a guided entry point.
- Added a richer run interface with edit state, algorithm controls, metrics, and simulation state.
- Added A* path planning.
- Added BFS / A* algorithm selection.
- Added runtime, visited-node count, and path-length statistics.
- Added basic robot path-following animation and trail rendering.
- Improved UI text clarity with cross-platform font fallback.
- Increased the right-side panel width.
- Resized the window to `1160 x 780` with a clean `840 x 780` grid area.
- Reduced run-panel font sizes slightly and capped status messages to two lines.
- Simplified the home screen into a shorter transition screen.
- Replaced crowded edit and algorithm buttons with floating dropdown selectors.
- Added no-path status feedback.
- Added visited-node display after BFS search.
- Updated README and development notes for the new modular structure.

## Week 3 - 2026-07-04

- Extended `SearchResult` with `visited_order` so planners can preserve the exact node visitation sequence.
- Added step-by-step search animation for BFS, A*, DFS, Dijkstra, and Greedy Best-First Search.
- Added `SearchAnimationState` to manage animation progress, final path reveal, and history recording after animation finishes.
- Added planner run history with snapshots of obstacles, start, goal, visited cells, and final path.
- Added clickable Recent Runs entries that restore the selected historical map and result on the left grid.
- Added map identity numbering with `M1`, `M2`, etc., based on a map signature of obstacles, start, and goal.
- Reused the same map ID when the same map appears again, instead of assigning a new ID every time.
- Increased stored run history to 20 entries and made the right-side panel scrollable.
- Refined the run-panel UI by removing extra titles, using a lighter macOS-style color palette, and tightening typography.
- Reworked Recent Runs into compact horizontal entries for easier scanning and clicking.
- Added DFS path planning in `planning/dfs.py`.
- Added Dijkstra shortest-path planning in `planning/dijkstra.py`.
- Added Greedy Best-First Search in `planning/greedy.py`.
- Expanded the planner selector and `Tab` shortcut cycle to include BFS, A*, DFS, Dijkstra, and Greedy.
- Verified the planner implementations with compile checks and a planner smoke test.

## Week 4 - 2026-07-12

- Added `pymunk` as the 2D rigid-body physics engine dependency.
- Added `core/coordinates.py` for grid cell, continuous world position, and screen pixel conversion.
- Added `physics/physics_world.py` with a Pymunk `Space`, dynamic circular robot body, and static square obstacle bodies.
- Replaced basic interpolated robot animation with continuous physics-based robot simulation.
- Added fixed physics timestep integration with a bounded accumulator for more stable simulation.
- Added robot physical parameters including mass, radius, force limits, speed limits, and collision shapes.
- Added `control/pid.py` with reusable `PIDConfig` and `PIDController`.
- Added PID heading control that converts heading error into torque.
- Added `control/path_tracker.py` to convert discrete planner paths into continuous waypoint / segment tracking targets.
- Added path compression so the robot tracks endpoints and turning cells instead of every cell center.
- Added segment-constrained lookahead tracking to reduce direct diagonal pulls across turns.
- Added cross-track error diagnostics and cross-track correction force.
- Added segment recapture logic when the robot is pushed far from the current path segment.
- Added force damping, maximum force limiting, maximum speed limiting, heading gate, and arrival slowdown.
- Added soft path clearance warnings instead of hard obstacle inflation, preserving one-cell corridor feasibility.
- Added startup heading alignment so the robot turns in place before applying forward force.
- Added `blocked` detection for low-speed, no-progress, high-force states, and stopped hard-pushing after physical blockage.
- Added `PhysicsWorld.stop_robot()` and `stop_robot_translation()` helpers for blocked and alignment states.
- Fixed a critical force-coordinate bug by applying controller force with `apply_force_at_world_point()` instead of local-space force application.
- Expanded the Simulation panel with speed, target, distance, segment progress, cross-track error, force, torque, heading error, alignment state, physical parameters, PID values, max torque, max velocity, and stuck diagnostics.
- Updated development notes with detailed records for stages 6-A through 6-J, including stuck debugging, PID limitations, and force coordinate-system lessons.
- Added Week 4 QA documentation explaining Pymunk, PathTracker, PID, stuck iterations, world-space force vs local force, and Simulation panel variables.
- Verified Week 4 with compile checks and focused straight, vertical, turning, and one-cell corridor smoke tests.

## Upcoming

- Improve corner approach behavior with turn-aware slowdown.
- Split motion control into tangent-speed control and normal cross-track correction.
- Add narrow-corridor speed protection based on clearance and cross-track error.
- Add blocked recovery tools such as Reset Robot, Pause / Resume, or local recovery.
- Visualize current segment, projected point, and lookahead target for easier debugging.
- Save representative stuck cases as repeatable regression scenarios.
