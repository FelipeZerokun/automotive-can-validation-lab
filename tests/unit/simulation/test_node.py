"""Tests for a virtual CAN node."""

import pytest

from automotive_can_validation_lab.protocol.frame import CanFrame
from automotive_can_validation_lab.simulation import VirtualCanNode


def make_frame(identifier: int, timestamp: float = 0.0) -> CanFrame:
    """Create a valid standard frame for node tests."""
    return CanFrame(
        identifier=identifier,
        is_extended=False,
        data=b"",
        timestamp=timestamp,
    )


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("instrument-cluster", "instrument-cluster"),
        (" powertrain ", "powertrain"),
    ],
)
def test_accepts_and_normalizes_valid_name(name: str, expected: str) -> None:
    node = VirtualCanNode(name)

    assert node.name == expected


@pytest.mark.parametrize("name", ["", " ", "\t\n"])
def test_rejects_empty_or_whitespace_only_name(name: str) -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        VirtualCanNode(name)


@pytest.mark.parametrize("name", [None, 123, True])
def test_rejects_non_string_name(name: object) -> None:
    with pytest.raises(TypeError, match="name must be a string"):
        VirtualCanNode(name)  # type: ignore[arg-type]


def test_starts_with_no_received_frames() -> None:
    node = VirtualCanNode("instrument-cluster")

    assert node.received_frames == ()


def test_receives_can_frame() -> None:
    node = VirtualCanNode("instrument-cluster")
    frame = make_frame(0x100)

    node.receive(frame)

    assert node.received_frames == (frame,)


def test_preserves_frame_arrival_order() -> None:
    node = VirtualCanNode("instrument-cluster")
    first = make_frame(0x200, timestamp=1.0)
    second = make_frame(0x100, timestamp=2.0)

    node.receive(first)
    node.receive(second)

    assert node.received_frames == (first, second)


@pytest.mark.parametrize("invalid_frame", [None, 0x100, b"\x00", "frame"])
def test_rejects_non_frame_without_changing_history(invalid_frame: object) -> None:
    node = VirtualCanNode("instrument-cluster")
    existing_frame = make_frame(0x100)
    node.receive(existing_frame)

    with pytest.raises(TypeError, match="frame must be a CanFrame"):
        node.receive(invalid_frame)  # type: ignore[arg-type]

    assert node.received_frames == (existing_frame,)


def test_received_frames_is_an_immutable_snapshot() -> None:
    node = VirtualCanNode("instrument-cluster")
    received_frame = make_frame(0x100)
    additional_frame = make_frame(0x200)
    node.receive(received_frame)

    snapshot = node.received_frames
    snapshot += (additional_frame,)

    assert snapshot == (received_frame, additional_frame)
    assert node.received_frames == (received_frame,)


def test_clears_received_frames() -> None:
    node = VirtualCanNode("instrument-cluster")
    node.receive(make_frame(0x100))
    node.receive(make_frame(0x200))

    node.clear_received_frames()

    assert node.received_frames == ()
