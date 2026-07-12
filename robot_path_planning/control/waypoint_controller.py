"""Basic force controller for waypoint tracking."""

from __future__ import annotations

from dataclasses import dataclass
import math

from robot_path_planning.control.path_tracker import TrackingTarget
from robot_path_planning.control.pid import PIDConfig, PIDController
from robot_path_planning.core.coordinates import WorldPosition
from robot_path_planning.physics import RobotPhysicsState


@dataclass(frozen=True)
class WaypointForceControllerConfig:
    """Tuning values for the simple waypoint force controller."""

    drive_force: float = 35.0
    damping_force: float = 8.0
    cross_track_gain: float = 10.0
    cross_track_damping: float = 10.0
    max_cross_track_force: float = 12.0
    max_force: float = 45.0
    arrival_slowdown_radius: float = 1.0
    path_deviation_slowdown: float = 0.8
    path_deviation_stop: float = 1.4
    heading_gate_power: float = 2.0
    heading_kp: float = 18.0
    heading_ki: float = 0.0
    heading_kd: float = 4.0
    max_torque: float = 120.0


@dataclass(frozen=True)
class ControlCommand:
    """Controller output consumed by the physics world."""

    force: WorldPosition
    torque: float = 0.0


class WaypointForceController:
    """Computes a world-space force that pulls the robot toward a waypoint."""

    def __init__(self, config: WaypointForceControllerConfig | None = None) -> None:
        self.config = config or WaypointForceControllerConfig()
        self.heading_pid = PIDController(
            PIDConfig(
                kp=self.config.heading_kp,
                ki=self.config.heading_ki,
                kd=self.config.heading_kd,
                output_limit=self.config.max_torque,
            )
        )

    def reset(self) -> None:
        """Reset controller history before a new robot run."""
        self.heading_pid.reset()

    def compute_command(
        self,
        robot_state: RobotPhysicsState,
        target: TrackingTarget,
        dt: float,
    ) -> ControlCommand:
        """Return force and torque commands for the current tracking target."""
        if target.waypoint is None or target.distance_to_waypoint <= 0:
            return ControlCommand(force=(0.0, 0.0))

        to_target = (
            target.waypoint[0] - robot_state.position[0],
            target.waypoint[1] - robot_state.position[1],
        )
        direction = (
            to_target[0] / target.distance_to_waypoint,
            to_target[1] / target.distance_to_waypoint,
        )
        desired_heading = math.atan2(direction[1], direction[0])
        heading_error = _normalize_angle(desired_heading - robot_state.angle)
        heading_alignment = max(0.0, math.cos(heading_error)) ** self.config.heading_gate_power
        arrival_scale = min(1.0, target.distance_to_waypoint / self.config.arrival_slowdown_radius)
        path_deviation_scale = self._path_deviation_drive_scale(target.cross_track_error)
        drive_scale = heading_alignment * arrival_scale * path_deviation_scale
        correction = self._cross_track_correction(robot_state, target)
        force = (
            direction[0] * self.config.drive_force * drive_scale
            + correction[0]
            - robot_state.velocity[0] * self.config.damping_force,
            direction[1] * self.config.drive_force * drive_scale
            + correction[1]
            - robot_state.velocity[1] * self.config.damping_force,
        )
        force = _clamp_vector(force, self.config.max_force)
        torque = self.heading_pid.update(heading_error, dt)
        return ControlCommand(force=force, torque=torque)

    def _path_deviation_drive_scale(self, cross_track_error: float) -> float:
        """Reduce forward drive while the robot is far from the current segment."""
        if cross_track_error <= self.config.path_deviation_slowdown:
            return 1.0
        if cross_track_error >= self.config.path_deviation_stop:
            return 0.0

        span = self.config.path_deviation_stop - self.config.path_deviation_slowdown
        if span <= 0:
            return 0.0
        return 1.0 - (cross_track_error - self.config.path_deviation_slowdown) / span

    def _cross_track_correction(
        self,
        robot_state: RobotPhysicsState,
        target: TrackingTarget,
    ) -> WorldPosition:
        """Return a bounded force that pulls the robot back to the current segment."""
        if target.segment_start is None or target.segment_end is None:
            return (0.0, 0.0)

        position = robot_state.position
        projected = _project_point_to_segment(position, target.segment_start, target.segment_end)
        normal_error = (projected[0] - position[0], projected[1] - position[1])
        normal_velocity = _normal_velocity(
            robot_state.velocity,
            target.segment_start,
            target.segment_end,
        )
        correction = (
            normal_error[0] * self.config.cross_track_gain
            - normal_velocity[0] * self.config.cross_track_damping,
            normal_error[1] * self.config.cross_track_gain
            - normal_velocity[1] * self.config.cross_track_damping,
        )
        return _clamp_vector(correction, self.config.max_cross_track_force)


def _normalize_angle(angle: float) -> float:
    """Normalize an angle to [-pi, pi]."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def _clamp_vector(vector: WorldPosition, max_length: float) -> WorldPosition:
    length = (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5
    if length <= max_length or length == 0:
        return vector
    scale = max_length / length
    return vector[0] * scale, vector[1] * scale


def _project_point_to_segment(
    point: WorldPosition,
    segment_start: WorldPosition,
    segment_end: WorldPosition,
) -> WorldPosition:
    dx = segment_end[0] - segment_start[0]
    dy = segment_end[1] - segment_start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return segment_start

    progress = (
        (point[0] - segment_start[0]) * dx
        + (point[1] - segment_start[1]) * dy
    ) / length_squared
    progress = min(1.0, max(0.0, progress))
    return (
        segment_start[0] + dx * progress,
        segment_start[1] + dy * progress,
    )


def _normal_velocity(
    velocity: WorldPosition,
    segment_start: WorldPosition,
    segment_end: WorldPosition,
) -> WorldPosition:
    dx = segment_end[0] - segment_start[0]
    dy = segment_end[1] - segment_start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return velocity

    tangent_velocity_scale = (velocity[0] * dx + velocity[1] * dy) / length_squared
    tangent_velocity = (
        dx * tangent_velocity_scale,
        dy * tangent_velocity_scale,
    )
    return (
        velocity[0] - tangent_velocity[0],
        velocity[1] - tangent_velocity[1],
    )
