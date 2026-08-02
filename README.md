# Automotive CAN Validation Lab

[![CI](https://github.com/FelipeZerokun/automotive-can-validation-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeZerokun/automotive-can-validation-lab/actions/workflows/ci.yml)

> A test-driven virtual environment for learning, simulating, and validating
> automotive Controller Area Network (CAN) communication.

## Overview

**Automotive CAN Validation Lab** is a learning-first software-engineering
project that models a simplified automotive CAN network with multiple virtual
Electronic Control Units (ECUs).

The project combines CAN protocol fundamentals, automotive communication,
deterministic simulation, automated testing, and continuous integration. It
evolves through small, working milestones from a validated CAN frame model into
an integrated virtual vehicle-network validation environment.

Repository: `automotive-can-validation-lab`

## Project status

| Milestone | Result | Status |
|---:|---|---|
| 0 | Reproducible Python repository with automated CI | Complete |
| 1 | Validated Classical CAN frame model | In progress |
| 2 | Deterministic virtual CAN bus | Planned |
| 3 | Virtual automotive ECUs | Planned |
| 4 | Signal encoding and DBC integration | Planned |
| 5 | Educational ISO-TP and UDS subset | Planned |
| 6 | ECU validation scenarios and fault injection | Planned |
| 7 | Integrated Automotive CAN Validation Lab | Planned |

See the [project brief](docs/automotive_can_validation_lab_project_brief.md)
and [development roadmap](docs/automotive_can_validation_lab_milestones.md).
Milestone 1 concepts and the frame contract are documented in
[CAN fundamentals and frame model](docs/can-fundamentals.md).

## Goals

- Learn CAN communication concepts through implementation.
- Simulate message-based communication between virtual ECUs.
- Model CAN arbitration, periodic transmission, message reception, and timeouts.
- Decode and encode vehicle signals using DBC-style definitions.
- Implement a limited, educational diagnostic communication workflow.
- Validate expected ECU behaviour through automated scenarios and fault
  injection.
- Apply professional engineering practices: packaging, tests, linting,
  documentation, CI, and reproducible environments.

## Core concepts

The project will cover:

- Classical CAN frames and identifiers
- Standard and extended CAN IDs
- CAN arbitration and priority
- Broadcast communication between ECUs
- Signal encoding, decoding, scaling, and endianness
- ECU periodic messages and timeout monitoring
- Error handling and fault scenarios
- CAN FD concepts
- ISO-TP and a small educational subset of UDS diagnostics
- Linux SocketCAN and virtual CAN (`vcan`) integration

## Language strategy

Python is the reference implementation for Milestones 1 through 7. It is used
for the CAN protocol model, deterministic bus simulation, virtual ECUs, DBC
handling, diagnostics, validation scenarios, tests, and reports.

C++ is intentionally deferred until the integrated Python lab is complete. A
later focused extension may implement one virtual ECU in C++ and connect it to
the Python validation environment through Linux SocketCAN `vcan`:

```text
Python simulation and validation
              ↕
       SocketCAN vcan0
              ↕
      Optional C++ ECU
```

This provides a realistic process and communication boundary without
duplicating the entire lab in two languages or introducing mixed build systems
before they provide a clear learning benefit.

## Planned architecture

```text
Virtual CAN Bus
│
├── Powertrain ECU
│   └── Publishes engine RPM and vehicle speed
│
├── Body Control Module
│   └── Publishes ignition, door, and lighting status
│
├── Instrument Cluster
│   └── Receives, decodes, and monitors vehicle signals
│
├── Diagnostic Tester
│   └── Sends diagnostic requests and validates responses
│
└── Validation Runner
    └── Executes test scenarios and fault-injection cases
```

## Repository layout

```text
.
├── .github/workflows/                 GitHub Actions CI
├── docs/                              Project brief and milestone roadmap
├── src/automotive_can_validation_lab/ Python package
├── tests/                             Automated tests
├── pyproject.toml                     Project and tool configuration
└── uv.lock                            Locked dependency resolution
```

Feature-specific modules are added only when their milestone begins.

## Development setup

### Prerequisites

- Git
- Python 3.12
- [`uv`](https://docs.astral.sh/uv/)

Create and synchronize the locked project environment:

```powershell
uv sync --locked --all-groups
```

Run the automated tests with coverage:

```powershell
uv run python -m pytest
```

Run the lint check:

```powershell
uv run ruff check .
```

Check formatting:

```powershell
uv run ruff format --check .
```

Apply formatting:

```powershell
uv run ruff format .
```

## Scope

This is an educational automotive simulation. It uses fictional identifiers,
signals, ECU data, and diagnostic values. It does not model electrical bus
characteristics and is not a production CAN controller, diagnostic stack, or
vehicle safety system.
