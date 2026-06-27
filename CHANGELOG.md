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

## Upcoming

- Animate BFS search progress.
- Add planner history for richer algorithm comparison.
- Add a guaranteed-solvable random map generator.
- Improve robot rendering with heading triangle.
- Add PID heading controller.
