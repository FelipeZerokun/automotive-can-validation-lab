"""Deterministic virtual CAN bus."""

from dataclasses import dataclass
from typing import Literal

from automotive_can_validation_lab.protocol.frame import CanFrame
from automotive_can_validation_lab.simulation.clock import SimulationClock
from automotive_can_validation_lab.simulation.node import VirtualCanNode


@dataclass(frozen=True)
class BusEvent:
    """An immutable simulation event; frame timestamps retain request time."""

    kind: Literal["registered", "deregistered", "requested", "cancelled", "lost", "delivered"]
    timestamp: float
    node_name: str
    frame: CanFrame | None = None
    recipients: tuple[str, ...] = ()


class VirtualCanBus:
    """A deterministic bus that queues and broadcasts Classical CAN frames."""

    def __init__(self, clock: SimulationClock) -> None:
        """Create a bus controlled by the supplied simulation clock."""
        if not isinstance(clock, SimulationClock):
            raise TypeError(f"clock must be a SimulationClock, got {type(clock).__name__}")

        self._clock = clock
        self._nodes: dict[str, VirtualCanNode] = {}
        self._pending_transmissions: list[tuple[VirtualCanNode, CanFrame]] = []
        self._events: list[BusEvent] = []

    @property
    def events(self) -> tuple[BusEvent, ...]:
        """Return an immutable snapshot of the ordered event history."""
        return tuple(self._events)

    @property
    def clock(self) -> SimulationClock:
        """Return the simulation clock used by this bus."""
        return self._clock

    @property
    def registered_nodes(self) -> tuple[VirtualCanNode, ...]:
        """Return registered nodes in deterministic registration order."""
        return tuple(self._nodes.values())

    @property
    def pending_count(self) -> int:
        """Return the number of queued transmission requests."""
        return len(self._pending_transmissions)

    def register(self, node: VirtualCanNode) -> None:
        """Register a node whose normalized name is not already in use."""
        if not isinstance(node, VirtualCanNode):
            raise TypeError(f"node must be a VirtualCanNode, got {type(node).__name__}")

        if node.name in self._nodes:
            raise ValueError(f"node name {node.name!r} is already registered")

        self._nodes[node.name] = node
        self._events.append(BusEvent("registered", self._clock.now, node.name))

    def deregister(self, node: VirtualCanNode) -> None:
        """Deregister a node and cancel its pending transmission requests."""
        self._require_registered(node)

        del self._nodes[node.name]
        self._events.append(BusEvent("deregistered", self._clock.now, node.name))
        for sender, frame in self._pending_transmissions:
            if sender is node:
                self._events.append(BusEvent("cancelled", self._clock.now, node.name, frame))
        self._pending_transmissions = [
            request for request in self._pending_transmissions if request[0] is not node
        ]

    def request_transmission(self, sender: VirtualCanNode, frame: CanFrame) -> None:
        """Queue a frame from a registered sender at the current simulation time."""
        self._require_registered(sender)

        if not isinstance(frame, CanFrame):
            raise TypeError(f"frame must be a CanFrame, got {type(frame).__name__}")

        if frame.timestamp != self._clock.now:
            raise ValueError(
                f"frame timestamp must equal current simulation time {self._clock.now}, "
                f"got {frame.timestamp}"
            )

        self._pending_transmissions.append((sender, frame))
        self._events.append(BusEvent("requested", self._clock.now, sender.name, frame))

    def process_next(self) -> CanFrame | None:
        """Deliver one winner ordered by request time, numeric ID, then arrival.

        Contenders at the earliest timestamp remain pending after losing. Each
        call is one arbitration round; it does not advance the simulation clock.
        """
        if not self._pending_transmissions:
            return None

        winner_index = min(
            range(len(self._pending_transmissions)),
            key=lambda index: (
                self._pending_transmissions[index][1].timestamp,
                self._pending_transmissions[index][1].identifier,
            ),
        )
        sender, frame = self._pending_transmissions.pop(winner_index)
        for contender, pending in self._pending_transmissions:
            if pending.timestamp == frame.timestamp:
                self._events.append(BusEvent("lost", self._clock.now, contender.name, pending))

        for node in self._nodes.values():
            if node is not sender:
                node.receive(frame)

        recipients = tuple(node.name for node in self._nodes.values() if node is not sender)
        self._events.append(BusEvent("delivered", self._clock.now, sender.name, frame, recipients))

        return frame

    def _require_registered(self, node: VirtualCanNode) -> None:
        """Raise when a value is not the exact registered node instance."""
        if not isinstance(node, VirtualCanNode):
            raise TypeError(f"node must be a VirtualCanNode, got {type(node).__name__}")

        if self._nodes.get(node.name) is not node:
            raise ValueError(f"node {node.name!r} is not registered")
