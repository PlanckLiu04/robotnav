"""Reusable PID controller primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PIDConfig:
    """Tuning values and output limits for a PID controller."""

    kp: float
    ki: float = 0.0
    kd: float = 0.0
    output_limit: float | None = None
    integral_limit: float | None = None


class PIDController:
    """Stateful PID controller for one scalar error signal."""

    def __init__(self, config: PIDConfig) -> None:
        self.config = config
        self.integral = 0.0
        self.previous_error: float | None = None

    def reset(self) -> None:
        """Clear accumulated controller state."""
        self.integral = 0.0
        self.previous_error = None

    def update(self, error: float, dt: float) -> float:
        """Compute PID output for the latest error value."""
        if dt <= 0:
            return self._clamp(self.config.kp * error, self.config.output_limit)

        self.integral += error * dt
        self.integral = self._clamp(self.integral, self.config.integral_limit)

        derivative = 0.0
        if self.previous_error is not None:
            derivative = (error - self.previous_error) / dt
        self.previous_error = error

        output = (
            self.config.kp * error
            + self.config.ki * self.integral
            + self.config.kd * derivative
        )
        return self._clamp(output, self.config.output_limit)

    @staticmethod
    def _clamp(value: float, limit: float | None) -> float:
        if limit is None:
            return value
        return max(-limit, min(limit, value))
