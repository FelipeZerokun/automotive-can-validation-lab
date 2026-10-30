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


def test_arbitration_and_retry_are_repeatable_across_three_nodes() -> None:
    histories = []
    for _ in range(3):
        bus = VirtualCanBus(SimulationClock())
        high, low, observer = (VirtualCanNode(name) for name in ("high", "low", "observer"))
        for node in (high, low, observer):
            bus.register(node)
        high_frame, low_frame = make_frame(0x200), make_frame(0x100)
        bus.request_transmission(high, high_frame)
        bus.request_transmission(low, low_frame)
        assert bus.process_next() is low_frame
        assert bus.pending_count == 1
        assert high.received_frames == (low_frame,)
        assert observer.received_frames == (low_frame,)
        assert bus.process_next() is high_frame
        assert low.received_frames == (high_frame,)
        assert observer.received_frames == (low_frame, high_frame)
        assert bus.pending_count == 0
        assert bus.clock.now == 0.0
        snapshot = bus.events
        assert bus.process_next() is None
        assert bus.events == snapshot
        assert [event.kind for event in snapshot] == [
            "registered",
            "registered",
            "registered",
            "requested",
            "requested",
            "lost",
            "delivered",
            "delivered",
        ]
        assert snapshot[5].frame is high_frame
        assert snapshot[6].recipients == ("high", "observer")
        histories.append(snapshot)
    assert histories[0] == histories[1] == histories[2]


def test_earlier_timestamp_precedes_later_higher_priority_frame() -> None:
    clock = SimulationClock()
    bus = VirtualCanBus(clock)
    sender = VirtualCanNode("sender")
    bus.register(sender)
    early = make_frame(0x700)
    bus.request_transmission(sender, early)
    clock.advance_to(1.0)
    later = make_frame(0x001, 1.0)
    bus.request_transmission(sender, later)
    assert bus.process_next() is early
    assert bus.process_next() is later
    assert not any(event.kind == "lost" for event in bus.events)
    assert bus.events[-2].timestamp == 1.0
    assert bus.events[-2].frame.timestamp == 0.0
    assert bus.events[-1].recipients == ()


def test_equal_identifiers_preserve_arrival_order_including_duplicate_requests() -> None:
    bus = VirtualCanBus(SimulationClock())
    sender = VirtualCanNode("sender")
    bus.register(sender)
    first = CanFrame(0x123, True, b"first", 0)
    second = CanFrame(0x123, False, b"second", 0)
    for frame in (first, second, first):
        bus.request_transmission(sender, frame)
    assert bus.process_next() is first
    assert bus.process_next() is second
    assert bus.process_next() is first
    assert bus.pending_count == 0


def test_arbitration_uses_numeric_identifier_for_extended_frames() -> None:
    bus = VirtualCanBus(SimulationClock())
    sender = VirtualCanNode("sender")
    bus.register(sender)
    frames = [CanFrame(0x1FFFFFFF, True, b"", 0), make_frame(0x7FF), make_frame(0)]
    for frame in frames:
        bus.request_transmission(sender, frame)
    assert [bus.process_next() for _ in frames] == list(reversed(frames))


def test_deregister_cancels_arbitration_loser_and_logs_cancellation() -> None:
    bus = VirtualCanBus(SimulationClock())
    loser, winner = VirtualCanNode("loser"), VirtualCanNode("winner")
    bus.register(loser)
    bus.register(winner)
    frame = make_frame(0x200)
    bus.request_transmission(loser, frame)
    bus.request_transmission(winner, make_frame(0x100))
    bus.process_next()
    bus.deregister(loser)
    assert bus.pending_count == 0
    assert bus.events[-1].kind == "cancelled"
    assert bus.events[-1].frame is frame
    assert bus.events[-1].node_name == "loser"
    bus.register(VirtualCanNode("loser"))
    assert bus.process_next() is None


def test_events_are_immutable_snapshots_and_rejections_do_not_log() -> None:
    from dataclasses import FrozenInstanceError

    bus = VirtualCanBus(SimulationClock())
    sender = VirtualCanNode("sender")
    assert bus.events == ()
    bus.register(sender)
    snapshot = bus.events
    with pytest.raises(FrozenInstanceError):
        snapshot[0].node_name = "changed"
    with pytest.raises(ValueError):
        bus.register(sender)
    with pytest.raises(ValueError):
        bus.request_transmission(sender, make_frame(0x100, 1.0))
    assert bus.events == snapshot
    bus.request_transmission(sender, make_frame(0x100))
    assert len(snapshot) == 1
    assert len(bus.events) == 2
