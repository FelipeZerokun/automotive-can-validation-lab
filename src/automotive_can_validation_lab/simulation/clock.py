"""Deterministic simulation clock."""

from math import isfinite


class SimulationClock:
    """A manually controlled monotonic clock measured in simulation seconds."""

    def __init__(self, initial_time: int | float = 0.0) -> None:
        """Create a clock at a finite, non-negative simulation time."""
        self._now = self._normalize_time(initial_time, field_name="initial_time")

    @property
    def now(self) -> float:
        """Return the current simulation time in seconds."""
        return self._now

    def advance(self, delta: int | float) -> float:
        """Advance by a non-negative duration and return the new time."""
        normalized_delta = self._normalize_time(delta, field_name="delta")
        new_time = self._now + normalized_delta

        if not isfinite(new_time):
            raise ValueError("resulting simulation time must be finite")

        self._now = new_time
        return self._now

    def advance_to(self, timestamp: int | float) -> float:
        """Advance to an absolute time that is not earlier than the current time."""
        normalized_timestamp = self._normalize_time(timestamp, field_name="timestamp")

        if normalized_timestamp < self._now:
            raise ValueError(
                f"timestamp must not be earlier than current time {self._now}, got {timestamp!r}"
            )

        self._now = normalized_timestamp
        return self._now

    @staticmethod
    def _normalize_time(value: int | float, *, field_name: str) -> float:
        """Validate and normalize a simulation-time value."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"{field_name} must be an integer or float, got {type(value).__name__}")

        normalized_value = float(value)

        if not isfinite(normalized_value) or normalized_value < 0:
            raise ValueError(f"{field_name} must be finite and non-negative, got {value!r}")

        if normalized_value == 0:
            return 0.0

        return normalized_value
