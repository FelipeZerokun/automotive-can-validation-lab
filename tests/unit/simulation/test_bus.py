"""Tests for deterministic virtual CAN bus delivery."""

import pytest

from automotive_can_validation_lab.protocol.frame import CanFrame
from automotive_can_validation_lab.simulation import (
    SimulationClock,
    VirtualCanBus,
    VirtualCanNode,
)


def make_frame(identifier: int, timestamp: float = 0.0) -> CanFrame:
    """Create a valid standard frame for bus tests."""
    return CanFrame(identifier, False, b"", timestamp)


def test_starts_with_clock_and_no_nodes_or_pending_transmissions() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)

    assert bus.clock is clock
    assert bus.registered_nodes == ()
    assert bus.pending_count == 0


@pytest.mark.parametrize("invalid_clock", [None, 0.0, "clock"])
def test_rejects_invalid_clock(invalid_clock: object) -> None:
    with pytest.raises(TypeError, match="clock must be a SimulationClock"):
        VirtualCanBus(invalid_clock)  # type: ignore[arg-type]


def test_registers_nodes_in_registration_order() -> None:
    bus = VirtualCanBus(SimulationClock())
    first = VirtualCanNode("powertrain")
    second = VirtualCanNode("instrument-cluster")

    bus.register(first)
    bus.register(second)

    assert bus.registered_nodes == (first, second)


@pytest.mark.parametrize("invalid_node", [None, "powertrain", 123])
def test_register_rejects_non_node(invalid_node: object) -> None:
    bus = VirtualCanBus(SimulationClock())

    with pytest.raises(TypeError, match="node must be a VirtualCanNode"):
        bus.register(invalid_node)  # type: ignore[arg-type]


def test_rejects_registering_same_node_twice() -> None:
    bus = VirtualCanBus(SimulationClock())
    node = VirtualCanNode("powertrain")
    bus.register(node)

    with pytest.raises(ValueError, match="already registered"):
        bus.register(node)

    assert bus.registered_nodes == (node,)


def test_rejects_duplicate_node_name() -> None:
    bus = VirtualCanBus(SimulationClock())
    registered = VirtualCanNode("powertrain")
    duplicate = VirtualCanNode(" powertrain ")
    bus.register(registered)

    with pytest.raises(ValueError, match="already registered"):
        bus.register(duplicate)

    assert bus.registered_nodes == (registered,)


def test_deregisters_registered_node() -> None:
    bus = VirtualCanBus(SimulationClock())
    first = VirtualCanNode("powertrain")
    second = VirtualCanNode("instrument-cluster")
    bus.register(first)
    bus.register(second)

    bus.deregister(first)

    assert bus.registered_nodes == (second,)


@pytest.mark.parametrize("invalid_node", [None, "powertrain", 123])
def test_deregister_rejects_non_node(invalid_node: object) -> None:
    bus = VirtualCanBus(SimulationClock())

    with pytest.raises(TypeError, match="node must be a VirtualCanNode"):
        bus.deregister(invalid_node)  # type: ignore[arg-type]


def test_deregister_rejects_unregistered_node() -> None:
    bus = VirtualCanBus(SimulationClock())
    node = VirtualCanNode("powertrain")

    with pytest.raises(ValueError, match="is not registered"):
        bus.deregister(node)


def test_deregister_does_not_accept_different_instance_with_same_name() -> None:
    bus = VirtualCanBus(SimulationClock())
    registered = VirtualCanNode("powertrain")
    same_name = VirtualCanNode("powertrain")
    bus.register(registered)

    with pytest.raises(ValueError, match="is not registered"):
        bus.deregister(same_name)

    assert bus.registered_nodes == (registered,)


def test_request_queues_frame_without_delivering_immediately() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)
    sender = VirtualCanNode("powertrain")
    receiver = VirtualCanNode("instrument-cluster")
    bus.register(sender)
    bus.register(receiver)
    frame = make_frame(0x100, clock.now)

    bus.request_transmission(sender, frame)

    assert bus.pending_count == 1
    assert receiver.received_frames == ()


def test_request_rejects_unregistered_sender() -> None:
    bus = VirtualCanBus(SimulationClock())
    sender = VirtualCanNode("powertrain")

    with pytest.raises(ValueError, match="is not registered"):
        bus.request_transmission(sender, make_frame(0x100))

    assert bus.pending_count == 0


def test_request_rejects_non_node_sender() -> None:
    bus = VirtualCanBus(SimulationClock())

    with pytest.raises(TypeError, match="node must be a VirtualCanNode"):
        bus.request_transmission("powertrain", make_frame(0x100))  # type: ignore[arg-type]

    assert bus.pending_count == 0


def test_request_rejects_non_frame_without_changing_queue() -> None:
    bus = VirtualCanBus(SimulationClock())
    sender = VirtualCanNode("powertrain")
    bus.register(sender)

    with pytest.raises(TypeError, match="frame must be a CanFrame"):
        bus.request_transmission(sender, b"\x00")  # type: ignore[arg-type]

    assert bus.pending_count == 0


def test_request_rejects_frame_from_different_simulation_time() -> None:
    clock = SimulationClock(1.0)
    bus = VirtualCanBus(clock)
    sender = VirtualCanNode("powertrain")
    bus.register(sender)

    with pytest.raises(ValueError, match="must equal current simulation time"):
        bus.request_transmission(sender, make_frame(0x100, timestamp=0.0))

    assert bus.pending_count == 0


def test_process_next_returns_none_when_no_transmission_is_pending() -> None:
    bus = VirtualCanBus(SimulationClock())

    assert bus.process_next() is None


def test_process_next_broadcasts_to_other_registered_nodes() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)
    sender = VirtualCanNode("powertrain")
    first_receiver = VirtualCanNode("instrument-cluster")
    second_receiver = VirtualCanNode("logger")
    for node in (sender, first_receiver, second_receiver):
        bus.register(node)
    frame = make_frame(0x100, clock.now)
    bus.request_transmission(sender, frame)

    processed = bus.process_next()

    assert processed is frame
    assert bus.pending_count == 0
    assert sender.received_frames == ()
    assert first_receiver.received_frames == (frame,)
    assert second_receiver.received_frames == (frame,)


def test_deregistered_node_does_not_receive_frame() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)
    sender = VirtualCanNode("powertrain")
    receiver = VirtualCanNode("instrument-cluster")
    bus.register(sender)
    bus.register(receiver)
    bus.deregister(receiver)
    frame = make_frame(0x100, clock.now)
    bus.request_transmission(sender, frame)

    bus.process_next()

    assert receiver.received_frames == ()


def test_deregistering_sender_cancels_its_pending_transmissions() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)
    sender = VirtualCanNode("powertrain")
    receiver = VirtualCanNode("instrument-cluster")
    bus.register(sender)
    bus.register(receiver)
    bus.request_transmission(sender, make_frame(0x100, clock.now))

    bus.deregister(sender)

    assert bus.pending_count == 0
    assert bus.process_next() is None
    assert receiver.received_frames == ()


def test_deregistering_sender_preserves_other_senders_pending_transmissions() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)
    removed_sender = VirtualCanNode("powertrain")
    remaining_sender = VirtualCanNode("body-control")
    receiver = VirtualCanNode("instrument-cluster")
    for node in (removed_sender, remaining_sender, receiver):
        bus.register(node)
    removed_frame = make_frame(0x100, clock.now)
    remaining_frame = make_frame(0x200, clock.now)
    bus.request_transmission(removed_sender, removed_frame)
    bus.request_transmission(remaining_sender, remaining_frame)

    bus.deregister(removed_sender)

    assert bus.pending_count == 1
    assert bus.process_next() is remaining_frame
    assert receiver.received_frames == (remaining_frame,)
