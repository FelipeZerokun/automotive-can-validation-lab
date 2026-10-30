# Deterministic virtual CAN bus

Milestone 2 connects logical CAN frames and virtual nodes without real-time
sleeping or hardware. Run `uv run python examples/milestone_2_bus.py`.

## Processing contract

- Create `VirtualCanBus(SimulationClock())` and register `VirtualCanNode` objects.
  Names must be unique; only the exact registered instance can transmit or leave.
- `request_transmission(sender, frame)` queues a request. Its frame timestamp
  must equal the current clock time. Future scheduling is not provided.
- `process_next()` delivers one frame, or returns `None` when idle. It chooses
  the earliest request timestamp, then the lowest numeric identifier. Equal
  timestamps and IDs retain request arrival order, including duplicate requests.
- Queue all simultaneous requests before calling `process_next()`. Requests
  submitted after delivery cannot retroactively contend with a delivered frame.
- Every other currently registered node receives the winner in registration
  order. The sender does not receive its own frame. Losing contenders remain
  queued and compete again on the next call without being resubmitted.
- Earlier timestamp groups drain before later groups, even if later frames have
  lower identifiers. Multiple pending requests from one sender participate
  independently; no controller transmit-mailbox model is simulated.
- Processing never advances the clock. Frames retain their original request
  timestamps, even if the caller advances the clock before delivery.
- Deregistering a node cancels all its pending requests. Registering a new node
  with the same name does not restore them. Receive histories remain available.

## Structured events

`bus.events` returns a tuple snapshot of frozen `BusEvent` records. Each record
contains `kind`, the current simulation `timestamp`, `node_name`, an optional
immutable `frame`, and a tuple of recipient names. The public event type is
exported from `automotive_can_validation_lab.simulation`.

Kinds are `registered`, `deregistered`, `requested`, `cancelled`, `lost`, and
`delivered`. Deregistration is logged before its cancellations. Each arbitration
round records same-timestamp losers in request order, followed by the winner's
`delivered` event. A repeatedly losing request can have multiple `lost` events.
Only delivery events list recipients; their node name identifies the sender.
Invalid operations and idle processing do not add events. History is in memory
and grows for the lifetime of the bus; create a new bus for an independent run.

## Demonstration

The body controller queues `0x200`, then the powertrain queues `0x100`, both at
simulation time zero. The cluster receives `0x100` followed by `0x200`:

```text
Delivered 0x100; pending=1
Delivered 0x200; pending=0
powertrain received: 0x200
body-control received: 0x100
instrument-cluster received: 0x100, 0x200
Events: registered, registered, registered, requested, requested, lost, delivered, delivered
```

## Model boundaries

This milestone implements the roadmap's simplified numeric-ID priority rule
for both standard and extended frames. It does not simulate bit-level mixed
format arbitration, equal-ID collisions, transmission duration, bus occupancy,
ACK/error frames, electrical behavior, or controller error counters. Equal-ID
arrival ordering and timestamp-group processing are explicit simulation rules.
Signal subscriptions, periodic ECU behavior, and timeouts belong to later
milestones. All registered nodes currently receive broadcasts except the sender.

## Verification

The test suite checks three-node delivery, deterministic repeated histories,
priority and retry, equal-ID and duplicate requests, identifier boundaries,
chronological ordering, cancellation, validation errors, and immutable logs.
Run `uv run python -m pytest`, `uv run ruff check .`, and
`uv run ruff format --check .` before committing.
