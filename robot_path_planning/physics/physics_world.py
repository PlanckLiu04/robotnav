"""Minimal Pymunk-backed 2D rigid body world."""

from __future__ import annotations

from dataclasses import dataclass

import pymunk

from robot_path_planning.core.coordinates import Cell, WorldPosition, cell_center_to_world


@dataclass(frozen=True)
class RobotPhysicsConfig:
    """Physical parameters for the robot rigid body."""

    mass: float = 5.0
    radius: float = 0.35
    friction: float = 0.8
    elasticity: float = 0.1


@dataclass(frozen=True)
class RobotPhysicsState:
    """Snapshot of the robot body state in continuous world coordinates."""

    position: WorldPosition
    velocity: WorldPosition
    angle: float
    angular_velocity: float


class PhysicsWorld:
    """Owns a Pymunk space with one dynamic robot and static grid obstacles."""

    def __init__(self, gravity: WorldPosition = (0.0, 0.0)) -> None:
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.robot_body: pymunk.Body | None = None
        self.robot_shape: pymunk.Shape | None = None
        self.obstacle_bodies: list[pymunk.Body] = []
        self.obstacle_shapes: list[pymunk.Shape] = []

    def reset(
        self,
        obstacles: set[Cell],
        robot_position: WorldPosition,
        robot_config: RobotPhysicsConfig | None = None,
        robot_angle: float = 0.0,
    ) -> None:
        """Rebuild the world from grid obstacles and a robot start position."""
        self.clear()
        self.add_obstacles(obstacles)
        self.add_robot(robot_position, robot_config or RobotPhysicsConfig(), initial_angle=robot_angle)

    def clear(self) -> None:
        """Remove all bodies and shapes from the physics space."""
        for body, shape in zip(self.obstacle_bodies, self.obstacle_shapes):
            self.space.remove(shape, body)
        self.obstacle_bodies.clear()
        self.obstacle_shapes.clear()

        if self.robot_shape is not None:
            self.space.remove(self.robot_shape)
            self.robot_shape = None

        if self.robot_body is not None:
            self.space.remove(self.robot_body)
            self.robot_body = None

    def add_obstacles(self, obstacles: set[Cell]) -> None:
        """Create static square collision shapes for occupied grid cells."""
        for cell in obstacles:
            center = cell_center_to_world(cell)
            body, shape = self._create_static_cell_shape(center)
            self.space.add(body, shape)
            self.obstacle_bodies.append(body)
            self.obstacle_shapes.append(shape)

    def add_robot(
        self,
        position: WorldPosition,
        config: RobotPhysicsConfig,
        initial_velocity: WorldPosition = (0.0, 0.0),
        initial_angle: float = 0.0,
    ) -> None:
        """Create a circular dynamic robot body."""
        moment = pymunk.moment_for_circle(config.mass, 0.0, config.radius)
        body = pymunk.Body(config.mass, moment)
        body.position = position
        body.velocity = initial_velocity
        body.angle = initial_angle

        shape = pymunk.Circle(body, config.radius)
        shape.friction = config.friction
        shape.elasticity = config.elasticity

        self.space.add(body, shape)
        self.robot_body = body
        self.robot_shape = shape

    def apply_robot_force(self, force: WorldPosition) -> None:
        """Apply a world-space force to the robot center of mass."""
        if self.robot_body is None:
            return
        self.robot_body.apply_force_at_world_point(force, self.robot_body.position)

    def apply_robot_torque(self, torque: float) -> None:
        """Apply torque to the robot body."""
        if self.robot_body is None:
            return
        self.robot_body.torque += torque

    def limit_robot_speed(self, max_speed: float) -> None:
        """Clamp the robot linear velocity to a maximum world-space speed."""
        if self.robot_body is None or max_speed <= 0:
            return

        velocity = self.robot_body.velocity
        speed = (velocity.x * velocity.x + velocity.y * velocity.y) ** 0.5
        if speed <= max_speed or speed == 0:
            return

        scale = max_speed / speed
        self.robot_body.velocity = velocity.x * scale, velocity.y * scale

    def stop_robot(self) -> None:
        """Stop robot motion and clear accumulated force/torque."""
        if self.robot_body is None:
            return

        self.robot_body.velocity = (0.0, 0.0)
        self.robot_body.angular_velocity = 0.0
        self.robot_body.force = (0.0, 0.0)
        self.robot_body.torque = 0.0

    def stop_robot_translation(self) -> None:
        """Stop linear motion while preserving angular motion for in-place turns."""
        if self.robot_body is None:
            return

        self.robot_body.velocity = (0.0, 0.0)
        self.robot_body.force = (0.0, 0.0)

    def step(self, dt: float) -> None:
        """Advance the physics simulation by one time step."""
        if dt <= 0:
            return
        self.space.step(dt)

    def robot_state(self) -> RobotPhysicsState | None:
        """Return the current robot state, if the robot exists."""
        if self.robot_body is None:
            return None

        body = self.robot_body
        return RobotPhysicsState(
            position=(body.position.x, body.position.y),
            velocity=(body.velocity.x, body.velocity.y),
            angle=body.angle,
            angular_velocity=body.angular_velocity,
        )

    def _create_static_cell_shape(self, center: WorldPosition) -> tuple[pymunk.Body, pymunk.Shape]:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = center
        width = 1.0
        height = 1.0
        shape = pymunk.Poly.create_box(body, (width, height), radius=0.0)
        shape.friction = 1.0
        shape.elasticity = 0.0
        return body, shape
