"""Virtual node attached to the deterministic CAN simulation."""

from automotive_can_validation_lab.protocol.frame import CanFrame


class VirtualCanNode:
    """A named CAN participant with an ordered receive history."""

    def __init__(self, name: str) -> None:
        """Create a node with a non-empty normalized name."""
        if not isinstance(name, str):
            raise TypeError(f"name must be a string, got {type(name).__name__}")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("name must not be empty or contain only whitespace")

        self._name = normalized_name
        self._received_frames: list[CanFrame] = []

    @property
    def name(self) -> str:
        """Return the normalized node name."""
        return self._name

    @property
    def received_frames(self) -> tuple[CanFrame, ...]:
        """Return an immutable snapshot of frames in arrival order."""
        return tuple(self._received_frames)

    def receive(self, frame: CanFrame) -> None:
        """Record a frame delivered to this node."""
        if not isinstance(frame, CanFrame):
            raise TypeError(f"frame must be a CanFrame, got {type(frame).__name__}")

        self._received_frames.append(frame)

    def clear_received_frames(self) -> None:
        """Remove every frame from the receive history."""
        self._received_frames.clear()
