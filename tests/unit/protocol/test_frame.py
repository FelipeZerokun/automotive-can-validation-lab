"""Tests for the Classical CAN frame domain model."""

import math

import pytest

from automotive_can_validation_lab.protocol.frame import CanFrame


@pytest.mark.parametrize(
    ("identifier", "is_extended"),
    [
        (0x000, False),
        (0x123, False),
        (0x7FF, False),
        (0x00000000, True),
        (0x00000123, True),
        (0x1FFFFFFF, True),
    ],
)
def test_accepts_valid_identifiers(identifier: int, is_extended: bool) -> None:
    frame = CanFrame(
        identifier=identifier,
        is_extended=is_extended,
        data=b"",
        timestamp=0.0,
    )

    assert frame.identifier == identifier
    assert frame.is_extended is is_extended


@pytest.mark.parametrize("identifier", [-1, 0x800])
def test_rejects_standard_identifier_outside_11_bit_range(identifier: int) -> None:
    with pytest.raises(ValueError, match="standard CAN identifier"):
        CanFrame(
            identifier=identifier,
            is_extended=False,
            data=b"",
            timestamp=0.0,
        )


@pytest.mark.parametrize("identifier", [-1, 0x20000000])
def test_rejects_extended_identifier_outside_29_bit_range(identifier: int) -> None:
    with pytest.raises(ValueError, match="extended CAN identifier"):
        CanFrame(
            identifier=identifier,
            is_extended=True,
            data=b"",
            timestamp=0.0,
        )


@pytest.mark.parametrize("identifier", [True, False, 1.5, "0x123", None])
def test_rejects_non_integer_identifier(identifier: object) -> None:
    with pytest.raises(TypeError, match="identifier must be an integer"):
        CanFrame(
            identifier=identifier,  # type: ignore[arg-type]
            is_extended=False,
            data=b"",
            timestamp=0.0,
        )


@pytest.mark.parametrize("is_extended", [0, 1, "false", None])
def test_rejects_non_boolean_frame_format(is_extended: object) -> None:
    with pytest.raises(TypeError, match="is_extended must be a boolean"):
        CanFrame(
            identifier=0x123,
            is_extended=is_extended,  # type: ignore[arg-type]
            data=b"",
            timestamp=0.0,
        )


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"\x01",
        bytes(range(8)),
    ],
)
def test_accepts_classical_can_payload_sizes(data: bytes) -> None:
    frame = CanFrame(
        identifier=0x123,
        is_extended=False,
        data=data,
        timestamp=0.0,
    )

    assert frame.data == data


@pytest.mark.parametrize(
    "data",
    [
        bytearray([0xAA, 0x55]),
        memoryview(b"\xaa\x55"),
    ],
)
def test_copies_bytes_like_payload_to_immutable_bytes(
    data: bytearray | memoryview,
) -> None:
    frame = CanFrame(
        identifier=0x123,
        is_extended=False,
        data=data,  # type: ignore[arg-type]
        timestamp=0.0,
    )

    assert frame.data == b"\xaa\x55"
    assert isinstance(frame.data, bytes)


def test_payload_is_independent_of_mutable_input() -> None:
    mutable_data = bytearray([0xAA, 0x55])

    frame = CanFrame(
        identifier=0x123,
        is_extended=False,
        data=mutable_data,  # type: ignore[arg-type]
        timestamp=0.0,
    )
    mutable_data[0] = 0x00

    assert frame.data == b"\xaa\x55"


def test_rejects_payload_larger_than_eight_bytes() -> None:
    with pytest.raises(ValueError, match="between 0 and 8 bytes"):
        CanFrame(
            identifier=0x123,
            is_extended=False,
            data=bytes(range(9)),
            timestamp=0.0,
        )


@pytest.mark.parametrize("data", [None, "AA55", [0xAA, 0x55], 123])
def test_rejects_non_bytes_like_payload(data: object) -> None:
    with pytest.raises(TypeError, match="data must be bytes-like"):
        CanFrame(
            identifier=0x123,
            is_extended=False,
            data=data,  # type: ignore[arg-type]
            timestamp=0.0,
        )


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        (0, 0.0),
        (1, 1.0),
        (0.125, 0.125),
        (-0.0, 0.0),
    ],
)
def test_accepts_non_negative_finite_timestamp(
    timestamp: int | float,
    expected: float,
) -> None:
    frame = CanFrame(
        identifier=0x123,
        is_extended=False,
        data=b"",
        timestamp=timestamp,
    )

    assert frame.timestamp == expected
    assert isinstance(frame.timestamp, float)
    assert math.copysign(1.0, frame.timestamp) == 1.0


@pytest.mark.parametrize("timestamp", [True, False, "1.0", None])
def test_rejects_non_numeric_timestamp(timestamp: object) -> None:
    with pytest.raises(TypeError, match="timestamp must be an integer or float"):
        CanFrame(
            identifier=0x123,
            is_extended=False,
            data=b"",
            timestamp=timestamp,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "timestamp",
    [
        -0.001,
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_rejects_invalid_numeric_timestamp(timestamp: float) -> None:
    with pytest.raises(
        ValueError,
        match="timestamp must be finite and non-negative",
    ):
        CanFrame(
            identifier=0x123,
            is_extended=False,
            data=b"",
            timestamp=timestamp,
        )
