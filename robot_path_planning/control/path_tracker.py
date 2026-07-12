"""Continuous waypoint tracking for grid-planned paths."""

from __future__ import annotations

from dataclasses import dataclass

from robot_path_planning.core.coordinates import Cell, WorldPosition, cell_center_to_world, distance


@dataclass(frozen=True)
class PathTrackerConfig:
    """Tuning values for waypoint switching and goal completion."""

    waypoint_tolerance: float = 0.25
    lookahead_distance: float = 0.75
    recapture_distance: float = 0.9
    recapture_progress_margin: float = 0.35


@dataclass(frozen=True)
class TrackingTarget:
    """Current tracking target and progress information."""

    waypoint: WorldPosition | None
    waypoint_index: int
    distance_to_waypoint: float
    finished: bool
    inside_goal: bool
    segment_start: WorldPosition | None = None
    segment_end: WorldPosition | None = None
    segment_progress: float = 0.0
    cross_track_error: float = 0.0


class PathTracker:
    """Converts a grid path into continuous waypoints and tracks progress."""

    def __init__(self, config: PathTrackerConfig | None = None) -> None:
        self.config = config or PathTrackerConfig()
        self.path: list[Cell] = []
        self.waypoints: list[WorldPosition] = []
        self.goal_cell: Cell | None = None
        self.target_index = 0

    def reset(self, path: list[Cell]) -> None:
        """Load a new planned path and prepare to track its next waypoint."""
        self.path = list(path)
        self.waypoints = [cell_center_to_world(cell) for cell in _compress_path(self.path)]
        self.goal_cell = self.path[-1] if self.path else None
        self.target_index = 1 if len(self.waypoints) > 1 else 0

    def clear(self) -> None:
        """Clear path-tracking state."""
        self.path.clear()
        self.waypoints.clear()
        self.goal_cell = None
        self.target_index = 0

    def update(self, robot_position: WorldPosition) -> TrackingTarget:
        """Return a lookahead target constrained to the current path segment."""
        if not self.waypoints:
            return TrackingTarget(
                waypoint=None,
                waypoint_index=0,
                distance_to_waypoint=0.0,
                finished=False,
                inside_goal=False,
            )

        inside_goal = self._inside_goal_cell(robot_position)
        if inside_goal:
            goal_index = max(len(self.waypoints) - 1, 0)
            return TrackingTarget(
                waypoint=self.waypoints[goal_index],
                waypoint_index=goal_index,
                distance_to_waypoint=distance(robot_position, self.waypoints[goal_index]),
                finished=True,
                inside_goal=True,
                segment_start=self.waypoints[max(goal_index - 1, 0)],
                segment_end=self.waypoints[goal_index],
                segment_progress=1.0,
            )

        if len(self.waypoints) == 1:
            waypoint = self.waypoints[0]
            return TrackingTarget(
                waypoint=waypoint,
                waypoint_index=0,
                distance_to_waypoint=distance(robot_position, waypoint),
                finished=False,
                inside_goal=False,
                segment_start=waypoint,
                segment_end=waypoint,
                segment_progress=0.0,
            )

        self._advance_segment(robot_position)
        self._recapture_segment_if_needed(robot_position)
        segment_start = self.waypoints[self.target_index - 1]
        segment_end = self.waypoints[self.target_index]
        projection = _project_point_to_segment(robot_position, segment_start, segment_end)
        if projection.segment_length == 0:
            lookahead_progress = 0.0
        else:
            lookahead_progress = min(
                1.0,
                max(
                    0.0,
                    projection.progress
                    + self.config.lookahead_distance / projection.segment_length,
                ),
            )
        waypoint = _interpolate(segment_start, segment_end, lookahead_progress)
        distance_to_waypoint = distance(robot_position, waypoint)

        return TrackingTarget(
            waypoint=waypoint,
            waypoint_index=self.target_index,
            distance_to_waypoint=distance_to_waypoint,
            finished=False,
            inside_goal=False,
            segment_start=segment_start,
            segment_end=segment_end,
            segment_progress=projection.progress,
            cross_track_error=projection.cross_track_error,
        )

    def _advance_segment(self, robot_position: WorldPosition) -> None:
        while self.target_index < len(self.waypoints) - 1:
            segment_start = self.waypoints[self.target_index - 1]
            segment_end = self.waypoints[self.target_index]
            projection = _project_point_to_segment(robot_position, segment_start, segment_end)
            distance_to_segment_end = distance(robot_position, segment_end)
            reached_segment_end = distance_to_segment_end <= self.config.waypoint_tolerance
            passed_segment_end = projection.progress >= 1.0

            if not reached_segment_end and not passed_segment_end:
                break
            self.target_index += 1

    def _recapture_segment_if_needed(self, robot_position: WorldPosition) -> None:
        current_start = self.waypoints[self.target_index - 1]
        current_end = self.waypoints[self.target_index]
        current_projection = _project_point_to_segment(robot_position, current_start, current_end)
        is_far_from_segment = current_projection.cross_track_error > self.config.recapture_distance
        is_far_outside_segment = (
            current_projection.progress < -self.config.recapture_progress_margin
            or current_projection.progress > 1.0 + self.config.recapture_progress_margin
        )
        if not is_far_from_segment and not is_far_outside_segment:
            return

        closest_index = self.target_index
        closest_projection = current_projection
        for index in range(1, len(self.waypoints)):
            projection = _project_point_to_segment(
                robot_position,
                self.waypoints[index - 1],
                self.waypoints[index],
            )
            if projection.cross_track_error < closest_projection.cross_track_error:
                closest_index = index
                closest_projection = projection

        self.target_index = closest_index

    def _inside_goal_cell(self, position: WorldPosition) -> bool:
        if self.goal_cell is None:
            return False

        x, y = position
        row, col = self.goal_cell
        return col <= x <= col + 1 and row <= y <= row + 1


@dataclass(frozen=True)
class SegmentProjection:
    progress: float
    clamped_progress: float
    segment_length: float
    cross_track_error: float


def _project_point_to_segment(
    point: WorldPosition,
    segment_start: WorldPosition,
    segment_end: WorldPosition,
) -> SegmentProjection:
    dx = segment_end[0] - segment_start[0]
    dy = segment_end[1] - segment_start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return SegmentProjection(
            progress=0.0,
            clamped_progress=0.0,
            segment_length=0.0,
            cross_track_error=distance(point, segment_start),
        )

    raw_progress = (
        (point[0] - segment_start[0]) * dx
        + (point[1] - segment_start[1]) * dy
    ) / length_squared
    clamped_progress = min(1.0, max(0.0, raw_progress))
    projected = _interpolate(segment_start, segment_end, clamped_progress)
    return SegmentProjection(
        progress=raw_progress,
        clamped_progress=clamped_progress,
        segment_length=length_squared ** 0.5,
        cross_track_error=distance(point, projected),
    )


def _interpolate(
    start: WorldPosition,
    end: WorldPosition,
    progress: float,
) -> WorldPosition:
    return (
        start[0] + (end[0] - start[0]) * progress,
        start[1] + (end[1] - start[1]) * progress,
    )


def _compress_path(path: list[Cell]) -> list[Cell]:
    """Keep endpoints and turning cells so the tracker follows larger segments."""
    if len(path) <= 2:
        return list(path)

    compressed = [path[0]]
    previous_direction = _cell_direction(path[0], path[1])

    for index in range(1, len(path) - 1):
        next_direction = _cell_direction(path[index], path[index + 1])
        if next_direction != previous_direction:
            compressed.append(path[index])
            previous_direction = next_direction

    compressed.append(path[-1])
    return compressed


def _cell_direction(start: Cell, end: Cell) -> tuple[int, int]:
    return end[0] - start[0], end[1] - start[1]
