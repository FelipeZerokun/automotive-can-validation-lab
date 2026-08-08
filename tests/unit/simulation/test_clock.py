"""Tests for the deterministic simulation clock."""

import math

import pytest

from automotive_can_validation_lab.simulation import SimulationClock


def test_clock_starts_at_zero_by_default() -> None:
    clock = SimulationClock()

    assert clock.now == 0.0
    assert isinstance(clock.now, float)


@pytest.mark.parametrize(
    ("initial_time", "expected"),
    [
        (0, 0.0),
        (-0.0, 0.0),
        (1, 1.0),
        (1.25, 1.25),
    ],
)
def test_clock_accepts_non_negative_initial_time(
    initial_time: int | float,
    expected: float,
) -> None:
    clock = SimulationClock(initial_time)

    assert clock.now == expected
    assert isinstance(clock.now, float)
    assert math.copysign(1.0, clock.now) == 1.0


@pytest.mark.parametrize(
    ("initial_time", "delta", "expected"),
    [
        (0.0, 0, 0.0),
        (0.0, 1, 1.0),
        (1.0, 0.25, 1.25),
    ],
)
def test_advance_moves_time_forward_and_returns_new_time(
    initial_time: float,
    delta: int | float,
    expected: float,
) -> None:
    clock = SimulationClock(initial_time)

    result = clock.advance(delta)

    assert result == expected
    assert clock.now == expected


@pytest.mark.parametrize(
    ("initial_time", "timestamp"),
    [
        (0.0, 0),
        (1.0, 1.0),
        (1.0, 2.5),
    ],
)
def test_advance_to_moves_to_same_or_later_time(
    initial_time: float,
    timestamp: int | float,
) -> None:
    clock = SimulationClock(initial_time)

    result = clock.advance_to(timestamp)

    assert result == float(timestamp)
    assert clock.now == float(timestamp)


@pytest.mark.parametrize("operation", ["initial_time", "advance", "advance_to"])
@pytest.mark.parametrize("value", [True, False, "1.0", None])
def test_rejects_non_numeric_time_values(operation: str, value: object) -> None:
    clock = SimulationClock(1.0)

    with pytest.raises(TypeError, match="must be an integer or float"):
        if operation == "initial_time":
            SimulationClock(value)  # type: ignore[arg-type]
        elif operation == "advance":
            clock.advance(value)  # type: ignore[arg-type]
        else:
            clock.advance_to(value)  # type: ignore[arg-type]

    assert clock.now == 1.0


@pytest.mark.parametrize("operation", ["initial_time", "advance", "advance_to"])
@pytest.mark.parametrize(
    "value",
    [-0.001, float("inf"), float("-inf"), float("nan")],
)
def test_rejects_invalid_numeric_time_values(operation: str, value: float) -> None:
    clock = SimulationClock(1.0)

    with pytest.raises(ValueError, match="must be finite and non-negative"):
        if operation == "initial_time":
            SimulationClock(value)
        elif operation == "advance":
            clock.advance(value)
        else:
            clock.advance_to(value)

    assert clock.now == 1.0


def test_advance_to_rejects_moving_backwards_without_changing_time() -> None:
    clock = SimulationClock(2.0)

    with pytest.raises(ValueError, match="must not be earlier than current time"):
        clock.advance_to(1.0)

    assert clock.now == 2.0


def test_advance_rejects_non_finite_result_without_changing_time() -> None:
    clock = SimulationClock(float.fromhex("0x1.fffffffffffffp+1023"))

    with pytest.raises(ValueError, match="resulting simulation time must be finite"):
        clock.advance(float.fromhex("0x1.fffffffffffffp+1023"))

    assert clock.now == float.fromhex("0x1.fffffffffffffp+1023")
