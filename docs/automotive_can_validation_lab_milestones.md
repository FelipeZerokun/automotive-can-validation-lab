# Automotive CAN Validation Lab — Development Milestones

> A learning-first, test-driven roadmap for building a virtual automotive CAN network and ECU validation environment.

## Project outcome

The completed project will simulate a small automotive network containing several virtual ECUs. It will model Classical CAN communication, message arbitration, signal encoding/decoding, diagnostic interactions, and validation scenarios. The final lab will run its tests automatically in CI and can optionally connect to Linux SocketCAN virtual interfaces.

## Guiding principles

- Start with a small, deterministic Python simulation; do not begin with hardware, AUTOSAR, or a GUI.
- Turn each learned CAN concept into a tested feature.
- Keep protocol logic independent of ECU behaviour and test infrastructure.
- Use fictional CAN identifiers, signals, and ECUs unless a source explicitly permits real data.
- Complete the definition of done for one milestone before starting the next.

## Milestone overview

| # | Milestone | Main result |
|---:|---|---|
| 0 | Engineering foundation | Reproducible, tested Python repository with CI |
| 1 | CAN fundamentals and frame model | Validated Classical CAN frame domain model |
| 2 | Deterministic virtual CAN bus | Broadcast delivery and arbitration simulation |
| 3 | Virtual automotive ECUs | Periodic messages, subscriptions, and timeouts |
| 4 | Signal and DBC layer | Engineering-value encoding and decoding |
| 5 | Diagnostic communication | Educational ISO-TP and UDS subset |
| 6 | ECU validation framework | Executable scenarios and fault injection |
| 7 | Integrated Automotive CAN Validation Lab | Portfolio-quality end-to-end simulation |

---

## Milestone 0 — Engineering foundation

### Purpose

Create the professional baseline before protocol implementation begins.

### Learn

- Python project packaging with `pyproject.toml`
- Virtual environments and locked dependencies
- Automated unit testing and code-quality checks
- GitHub Actions CI fundamentals

### Required tools

- Python 3.12 or the project-selected supported version
- `uv` for dependency and environment management
- pytest and pytest-cov
- Ruff
- VS Code Python, Pylance, Ruff, and Codex extensions

### Deliverables

```text
README.md
pyproject.toml
uv.lock
src/automotive_can_validation_lab/
tests/
.github/workflows/ci.yml
.gitignore
.editorconfig
```

### Definition of done

- `uv run pytest` succeeds.
- `uv run ruff check .` succeeds.
- `uv run ruff format --check .` succeeds.
- GitHub Actions runs those checks on every push and pull request.
- The README explains setup and the first commands to run.

---

## Milestone 1 — CAN fundamentals and frame model

### Purpose

Represent a Classical CAN frame safely and learn its logical fields.

### Learn

- Message-oriented, broadcast CAN communication
- Standard 11-bit versus extended 29-bit identifiers
- Data Length Code (DLC) and the Classical CAN 0–8-byte payload limit
- Logical frame structure: SOF, arbitration, control, data, CRC, ACK, EOF

### Implementation scope

Create an immutable `CanFrame` model with:

```text
identifier
is_extended
data
timestamp
```

Validate identifier ranges and payload size. Provide readable, stable log output.

### Deliverables

- `protocol/frame.py`
- Unit tests for valid and invalid IDs, payload sizes, equality, and representation
- `docs/can-fundamentals.md` with diagrams and definitions

### Definition of done

- A standard frame and an extended frame can be created and logged.
- Invalid identifiers or payloads fail with clear errors.
- Tests cover all frame validation paths.
- The implementation deliberately does not claim to be a complete physical CAN controller.

---

## Milestone 2 — Deterministic virtual CAN bus

### Purpose

Model the key bus-level behaviour without physical hardware.

### Learn

- Multi-master bus behaviour
- Broadcast delivery
- Non-destructive arbitration
- CAN identifier priority
- Deterministic simulation time

### Implementation scope

Create a `VirtualCanBus` that supports:

- Node registration and deregistration
- Transmission requests at a simulation timestamp
- Broadcast delivery to subscribed nodes
- Arbitration when messages start at the same simulated instant
- Structured event logging

### Key rule to simulate

When frames contend for the bus at the same time, the numerically lowest identifier wins arbitration. Losing frames remain pending and may retry later.

### Deliverables

- `simulation/bus.py`
- `simulation/clock.py`
- `simulation/node.py`
- Tests for delivery, ordering, arbitration, and retry behaviour

### Definition of done

- Three nodes exchange frames through the same bus.
- A simultaneous `0x100` and `0x200` transmission sends `0x100` first.
- Every receiving node observes the winning frame.
- Repeated tests produce identical results without relying on real time.

---

## Milestone 3 — Virtual automotive ECUs

### Purpose

Build a small, believable network that makes the bus useful.

### Learn

- ECU responsibilities and publisher/subscriber design
- Periodic versus event-driven messages
- Freshness monitoring and message timeouts
- Separation of application logic from network transport

### ECU set

| ECU | Responsibility | Example published information |
|---|---|---|
| Powertrain ECU | Vehicle motion state | engine RPM, vehicle speed |
| Body Control Module | Body and ignition state | ignition, doors, lights |
| Instrument Cluster | Display and monitoring | decoded values, timeout warnings |
| Diagnostic Tester | Reserved for Milestone 5 | requests and responses |

### Deliverables

- `ecus/powertrain.py`
- `ecus/body_control.py`
- `ecus/instrument_cluster.py`
- A small scenario: ignition on → periodic RPM/speed → cluster update
- Tests for periodic publishing and timeout detection

### Definition of done

- The powertrain ECU publishes a periodic message.
- The cluster decodes and stores the latest value.
- Stopping the message causes a configurable timeout warning.
- All CAN IDs are clearly documented as fictional lab definitions.

---

## Milestone 4 — Signal and DBC layer

### Purpose

Convert raw bytes into meaningful physical values.

### Learn

- Signals inside CAN data payloads
- Start bit, bit length, byte order, signedness
- Scaling, offset, units, and value ranges
- The role of a DBC file in automotive communication

### Implementation scope

Define a small DBC file for the virtual vehicle. Use `cantools` to encode and decode signals rather than implementing a full DBC parser.

Suggested signals:

```text
engine_speed_rpm
vehicle_speed_kph
coolant_temperature_c
ignition_on
driver_door_open
```

### Deliverables

- `dbcs/virtual_vehicle.dbc`
- `signals/codec.py`
- Signal round-trip tests: physical value → frame bytes → physical value
- Documentation describing every virtual frame and signal

### Definition of done

- A DBC definition converts example RPM and speed values correctly.
- Boundary and invalid-value tests exist.
- The cluster receives decoded engineering values, not raw byte arrays.

---

## Milestone 5 — Diagnostic communication

### Purpose

Introduce diagnostic requests and responses as a separate ECU interaction pattern.

### Learn

- Request/response communication over CAN
- ISO-TP segmentation concepts
- UDS service/request/positive-response structure
- Diagnostic session and data-identifier concepts

### Educational scope

Implement only a small, clearly documented subset:

- ISO-TP single-frame messages first
- UDS `0x10` Diagnostic Session Control
- UDS `0x22` Read Data By Identifier
- One or two virtual DIDs, such as ECU serial number and software version

### Deliverables

- `diagnostics/isotp.py`
- `diagnostics/uds.py`
- `ecus/diagnostic_tester.py`
- Tests for successful and rejected requests

### Definition of done

- A tester sends a request to a virtual ECU.
- The ECU returns a valid simulated response.
- Unknown identifiers return a documented negative response.
- The README labels this as an educational subset, not a production UDS implementation.

---

## Milestone 6 — ECU validation framework

### Purpose

Turn the simulation into a validation tool instead of only a demo.

### Learn

- Requirements-based testing
- Test scenarios and observable system behaviour
- Fault injection
- Validation reports and CI-friendly results

### Implementation scope

Define scenarios as Python objects first. Introduce YAML only when it makes scenarios easier to read and maintain.

Required validation cases:

- Engine RPM appears within a configured time after ignition.
- The cluster detects an RPM message timeout.
- A lower-priority frame loses arbitration.
- A dropped frame produces the expected fault state.
- A diagnostic request returns the correct virtual ECU identifier.

### Deliverables

- `validation/scenarios/`
- `validation/runner.py`
- Structured event log in JSON or text
- Pytest results and coverage in CI

### Definition of done

- At least five independent validation scenarios run automatically.
- Each scenario has an explicit requirement, setup, action, expected result, and failure message.
- A failure points to a meaningful validation assertion rather than only a stack trace.

---

## Milestone 7 — Integrated Automotive CAN Validation Lab

### Purpose

Integrate the previous milestones into a polished portfolio demonstration.

### Final demonstration scenario

```text
Ignition turns on
→ Body Control Module publishes ignition state
→ Powertrain ECU begins periodic RPM and speed messages
→ Instrument Cluster decodes and monitors signals
→ Validation runner injects a missing-message fault
→ Cluster reports stale data
→ Diagnostic Tester reads ECU identification
→ Automated report records the result
```

### Required deliverables

- End-to-end command-line demonstration
- Architecture diagram
- Complete protocol and signal documentation
- GitHub Actions pipeline
- Coverage report and test badges, if desired
- Docker or Dev Container configuration only if it materially improves reproducibility

### Optional extensions

- CAN FD message support
- SocketCAN `vcan` interface bridge on Linux/WSL
- CAN logging and replay
- A C++ ECU implementation communicating with the Python simulation boundary
- A small visual dashboard
- Hardware CAN adapter integration

### Definition of done

- A new developer can clone the repository, follow the README, and run the integrated simulation and tests.
- CI is green.
- The project demonstrates both CAN concepts and professional software-engineering practice.

---

## Technology decisions

| Concern | Initial choice | Reason |
|---|---|---|
| Main language | Python | Fast learning loop, clear tests, strong CAN tooling |
| Dependency management | `uv` + `pyproject.toml` | Reproducible environments and locked dependencies |
| Testing | pytest + pytest-cov | Clear unit and scenario testing |
| Formatting/linting | Ruff | One fast tool for formatting and linting |
| Signal/DBC support | `cantools` | Use an established library rather than writing a DBC parser |
| Virtual CAN integration | Linux SocketCAN `vcan` | Hardware-free CAN frame integration testing |
| C++ | Later, as a focused ECU or performance exercise | Avoid premature mixed-language complexity |
| Configuration | Typed Python settings and small YAML files | Hydra is unnecessary until ML-style experiment sweeps are required |

## Explicitly out of scope at the start

- Electrical/voltage-level physical-bus simulation
- Real vehicle data or manufacturer DBC files
- Complete UDS, ECU flashing, or security access
- AUTOSAR
- J1939, CAN XL, or CANopen
- Real CAN hardware
- A GUI-first implementation

## Working agreement for every milestone

Before a milestone is considered complete:

1. The feature is implemented in small, reviewable commits.
2. Unit tests cover success, boundary, and failure behaviour.
3. Ruff and pytest pass locally and in CI.
4. The README or documentation explains the relevant CAN concept.
5. The user can run a short demonstration command.

