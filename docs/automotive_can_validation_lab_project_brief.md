# Automotive CAN Validation Lab — Project Brief

## Purpose

This document is the living project charter for the Automotive CAN Validation
Lab. Use it together with the
[README](../README.md) and
[development roadmap](automotive_can_validation_lab_milestones.md) when
planning or reviewing work.

## Project identity

- **Project name:** Automotive CAN Validation Lab
- **Repository name:** `automotive-can-validation-lab`
- **Project type:** Learning-first, portfolio-quality automotive software
  simulation
- **Primary objective:** Learn Controller Area Network (CAN) communication by
  building a tested virtual automotive network containing several simulated
  ECUs

## Current status

**Milestone 0 — Engineering foundation is complete.**

The verified baseline includes:

- Python 3.12
- `pyproject.toml` and dependency management with `uv`
- A locked environment through `uv.lock`
- A `src`-layout Python package
- pytest and pytest-cov
- Ruff linting and formatting
- GitHub Actions CI on pushes and pull requests
- A public GitHub repository with green CI

**Milestone 1 — CAN fundamentals and frame model is complete.**

The completed milestone provides:

- An immutable Classical CAN frame domain model
- Standard 11-bit and extended 29-bit identifier validation
- Immutable zero-to-eight-byte payload handling
- Validated deterministic simulation timestamps
- Stable human-readable logging
- Unit tests for normal, boundary, and failure behavior
- A runnable standard-and-extended-frame demonstration

**Milestone 2 — Deterministic virtual CAN bus is next.**

## Final vision

The completed project will simulate a small vehicle network with a virtual CAN
bus, a powertrain ECU, body-control ECU, instrument cluster, diagnostic tester,
and validation runner.

It must demonstrate:

- Classical CAN frames, IDs, broadcast communication, and arbitration
- Periodic ECU messages, subscriptions, freshness, and timeout handling
- DBC-based signal encoding and decoding
- A small educational ISO-TP/UDS diagnostic flow
- Automated validation scenarios and fault injection
- Professional engineering practices: packaging, tests, linting,
  documentation, CI, and reproducibility

## Learning and engineering approach

- Build one small, working increment at a time.
- Explain relevant CAN and software-engineering concepts before or while
  implementing them.
- Let the project owner create implementation files unless direct editing is
  explicitly requested.
- Add tests and documentation with every feature.
- Prefer a deterministic simulation clock to real time.
- Keep protocol models, bus simulation, ECU behaviour, signal decoding,
  diagnostics, and validation code in separate modules.
- Use fictional CAN identifiers, DBC signals, ECU data, and diagnostic values.
- Prioritize clarity and correctness over feature count.

## Technical direction

| Concern | Decision |
|---|---|
| Main language | Python 3.12 |
| Packaging and dependencies | `pyproject.toml`, `uv`, and `uv.lock` |
| Test framework | pytest |
| Coverage | pytest-cov |
| Formatting and linting | Ruff |
| Type checking | Pylance in VS Code; reconsider a CI type checker when useful |
| Continuous integration | GitHub Actions |
| Signal/DBC handling | Add `cantools` when the DBC milestone begins |
| Virtual CAN integration | Add Linux SocketCAN `vcan` after the pure-Python simulator works |
| C++ | After the integrated Python lab, optionally implement one ECU that communicates through SocketCAN; do not rewrite the complete lab |
| Docker/Dev Container | Add only when Linux or SocketCAN reproducibility requires it |

## Language strategy

Python is the reference language for Milestones 1 through 7. The complete core
lab—including protocol models, deterministic simulation, virtual ECUs, signal
handling, diagnostics, validation scenarios, and reports—must work in Python
before a second implementation language is introduced.

This choice prioritizes:

- Fast test-driven development and clear domain models
- Deterministic simulation and readable validation scenarios
- Strong CAN and DBC tooling
- Straightforward debugging, logging, and report generation
- One reproducible build and test environment while the architecture evolves

C++ is reserved for a later, focused embedded-style exercise. The preferred
extension is one virtual ECU implemented as a separate C++ process and connected
to the Python lab through Linux SocketCAN `vcan`:

```text
Python validation runner and reference simulation
                      ↕
               SocketCAN vcan0
                      ↕
                One C++ ECU
```

The C++ component should have its own build and unit-test configuration. It
should demonstrate language and integration trade-offs without duplicating
every Python component or requiring Python/C++ bindings.

## Environment assumptions

- Development computer: Windows
- Editor: VS Code
- Python runtime installation: Python Install Manager
- Project and dependency management: `uv`
- Preferred later environment for SocketCAN, ROS, C++, and Docker: WSL/Ubuntu

The project must not assume WSL, Docker, or a CAN adapter is installed. Add
platform-specific integration only after the core simulator is tested.

## Scope boundaries

### In scope

- Classical CAN first
- Standard and extended CAN identifiers
- Frame validation and logging
- Virtual bus broadcast and arbitration
- Simulated ECUs and periodic messages
- DBC signals
- A small, explicitly educational ISO-TP and UDS subset
- Validation scenarios, message timeouts, and simple fault injection

### Explicitly out of scope initially

- Electrical or voltage-level bus simulation
- Real vehicle data, proprietary DBC files, or manufacturer-specific CAN IDs
- Real CAN hardware
- Full UDS, ECU flashing, security access, or cybersecurity implementation
- AUTOSAR
- J1939, CANopen, CAN XL, and full CAN FD implementation
- GUI/dashboard-first development
- A mixed Python/C++ codebase before a clear need exists

## Milestone order

1. **Milestone 0 — Engineering foundation** — complete
2. **Milestone 1 — CAN fundamentals and frame model** — complete
3. **Milestone 2 — Deterministic virtual CAN bus** — next
4. **Milestone 3 — Virtual automotive ECUs**
5. **Milestone 4 — Signal and DBC layer**
6. **Milestone 5 — Diagnostic communication**
7. **Milestone 6 — ECU validation framework**
8. **Milestone 7 — Integrated Automotive CAN Validation Lab**

Do not skip a milestone unless the project owner explicitly changes the
roadmap.

C++ is not required for these eight milestones. Consider the C++ ECU integration
only after Milestone 7 is complete and the Python implementation provides a
stable behavioral reference.

## Definition of progress

For every milestone, completion requires all of the following:

1. The intended behaviour is implemented.
2. Unit tests cover normal, boundary, and failure behaviour where relevant.
3. Formatting, linting, and tests pass locally.
4. CI runs the same essential checks.
5. Documentation explains the CAN concept and how to run the demonstration.
6. The next milestone is not started until the current milestone's definition
   of done is met.
