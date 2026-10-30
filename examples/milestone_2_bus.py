"""Demonstrate deterministic arbitration, broadcast, and retry with three nodes."""

from automotive_can_validation_lab.protocol.frame import CanFrame
from automotive_can_validation_lab.simulation import SimulationClock, VirtualCanBus, VirtualCanNode


def main() -> None:
    bus = VirtualCanBus(SimulationClock())
    powertrain = VirtualCanNode("powertrain")
    body = VirtualCanNode("body-control")
    cluster = VirtualCanNode("instrument-cluster")
    for node in (powertrain, body, cluster):
        bus.register(node)
    bus.request_transmission(body, CanFrame(0x200, False, b"\x01", bus.clock.now))
    bus.request_transmission(powertrain, CanFrame(0x100, False, b"\x02", bus.clock.now))
    while (frame := bus.process_next()) is not None:
        print(f"Delivered 0x{frame.identifier:03X}; pending={bus.pending_count}")
    for node in (powertrain, body, cluster):
        identifiers = ", ".join(f"0x{frame.identifier:03X}" for frame in node.received_frames)
        print(f"{node.name} received: {identifiers}")
    print("Events: " + ", ".join(event.kind for event in bus.events))


if __name__ == "__main__":
    main()
