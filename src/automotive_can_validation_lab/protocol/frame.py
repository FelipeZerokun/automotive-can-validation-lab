"""Classical CAN frame domain model."""

from dataclasses import dataclass
from math import isfinite

_STANDARD_IDENTIFIER_MAX = 0x7FF
_EXTENDED_IDENTIFIER_MAX = 0x1FFFFFFF


@dataclass(frozen=True)
class CanFrame:
    """An immutable logical representation of a Classical CAN data frame."""

    identifier: int
    is_extended: bool
    data: bytes
    timestamp: float

    def __post_init__(self) -> None:
        """Validate the frame fields after initialization."""

        if not isinstance(self.is_extended, bool):
            raise TypeError(f"is_extended must be a boolean, got {type(self.is_extended).__name__}")

        if not isinstance(self.identifier, int) or isinstance(self.identifier, bool):
            raise TypeError(f"identifier must be an integer, got {type(self.identifier).__name__}")

        maximum = _EXTENDED_IDENTIFIER_MAX if self.is_extended else _STANDARD_IDENTIFIER_MAX
        frame_format = "extended" if self.is_extended else "standard"

        if not 0 <= self.identifier <= maximum:
            raise ValueError(
                f"{frame_format} CAN identifier must be between "
                f"0x0 and 0x{maximum:X}, got {self.identifier!r}"
            )

        if not isinstance(self.data, (bytes, bytearray, memoryview)):
            raise TypeError(f"data must be bytes-like, got {type(self.data).__name__}")

        immutable_data = bytes(self.data)

        if len(immutable_data) > 8:
            raise ValueError(f"data must contain between 0 and 8 bytes, got {len(immutable_data)}")

        object.__setattr__(self, "data", immutable_data)

        if not isinstance(self.timestamp, (int, float)) or isinstance(
            self.timestamp,
            bool,
        ):
            raise TypeError(
                f"timestamp must be an integer or float, got {type(self.timestamp).__name__}"
            )

        normalized_timestamp = float(self.timestamp)

        if not isfinite(normalized_timestamp) or normalized_timestamp < 0:
            raise ValueError(f"timestamp must be finite and non-negative, got {self.timestamp!r}")

        if normalized_timestamp == 0:
            normalized_timestamp = 0.0

        object.__setattr__(self, "timestamp", normalized_timestamp)

    def __str__(self) -> str:
        """Return the stable human-readable frame representation."""
        identifier_width = 8 if self.is_extended else 3
        frame_format = "extended" if self.is_extended else "standard"
        formatted_data = " ".join(f"{byte:02X}" for byte in self.data)

        return (
            f"CanFrame(id=0x{self.identifier:0{identifier_width}X}, "
            f"format={frame_format}, dlc={len(self.data)}, "
            f"data={formatted_data}, timestamp={self.timestamp:.6f}s)"
        )

    def __repr__(self) -> str:
        """Return the stable developer-facing frame representation."""
        return str(self)
