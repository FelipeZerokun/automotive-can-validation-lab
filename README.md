# Automotive CAN Validation Lab

A bilingual learning and engineering project for building practical knowledge of automotive CAN communication, software validation and requirements-based testing.

The project is developed incrementally: each technical concept is first studied in English and German, then translated into small software requirements, Python implementations and automated tests.

> **Current milestone:** `CAN Fundamentals`
> **Status:** In progress
> **Current version:** `0.1.0`

---

## Project overview

The purpose of this repository is to develop a small virtual automotive communication and validation environment while learning the underlying engineering concepts step by step.

The project is not being created as a finished CAN or HIL system from the beginning. New functionality is added only after the corresponding theory has been studied and understood.

The intended learning flow is:

```text
Theory
  ↓
Software requirement
  ↓
Test case
  ↓
Python implementation
  ↓
Automated verification
  ↓
Documentation
```

This approach connects automotive communication theory with professional software-development and validation practices.

---

## Deutsche Kurzbeschreibung

Dieses Repository ist ein zweisprachiges Lern- und Entwicklungsprojekt zu den Themen Automotive-CAN-Kommunikation, Softwarevalidierung und anforderungsbasiertes Testen.

Das Projekt wird schrittweise entwickelt. Zuerst wird ein technisches Thema auf Englisch und Deutsch erarbeitet. Anschließend werden daraus kleine Softwareanforderungen, Python-Implementierungen und automatisierte Tests abgeleitet.

Neue Funktionen werden erst implementiert, nachdem die dazugehörigen theoretischen Grundlagen behandelt wurden.

---

## Current learning milestone

### CAN 01 — Fundamentals / Grundlagen

The current milestone covers the fundamental concepts of CAN communication:

* Why vehicles use communication networks
* CAN nodes, ECUs, controllers and transceivers
* Broadcast and multi-master communication
* Frames, messages and signals
* Standard and extended CAN identifiers
* Identifier-based arbitration priority
* Dominant and recessive bits
* Cyclic and event-based messages
* Cycle times and communication timeouts
* Raw and physical signal values
* Classic CAN and CAN FD at a high level
* Vehicle communication versus diagnostics

The complete bilingual learning note is available here:

* [`docs/learning_notes/01_can_fundamentals/01_CAN_Fundamentals.md`](docs/learning_notes/01_can_fundamentals/01_CAN_Fundamentals.md)

---

## Currently implemented

The software currently provides:

* Validation of 11-bit standard CAN identifiers
* Validation of 29-bit extended CAN identifiers
* Boundary-value tests for valid and invalid identifiers
* Traceability between CAN fundamentals requirements and automated tests
* A modern Python project structure using a `src` layout
* Automated testing with `pytest`

Example:

```python
from automotive_can_validation.can_identifier import (
    is_valid_standard_identifier,
)

is_valid_standard_identifier(0x100)  # True
is_valid_standard_identifier(0x7FF)  # True
is_valid_standard_identifier(0x800)  # False
```

---

## Current requirements

The software requirements for this milestone are documented in:

* [`requirements/CAN_FUNDAMENTALS_REQUIREMENTS.md`](requirements/CAN_FUNDAMENTALS_REQUIREMENTS.md)

The current implementation begins with:

| Requirement       | Description                              |
| ----------------- | ---------------------------------------- |
| `CAN-FND-REQ-001` | Validate standard 11-bit CAN identifiers |
| `CAN-FND-REQ-002` | Validate extended 29-bit CAN identifiers |

Additional fundamentals requirements will be implemented gradually during this milestone.

---

## Project structure

```text
automotive-can-validation-lab/
├── .vscode/
│   └── settings.json
├── docs/
│   ├──architecture.md
│   ├──project_learning_map.md
│   └── learning_notes/
│       └── 01_CAN_Fundamentals
│           ├──01_CAN_Fundamentals.md
│           └──assets
├── requirements/
│   └── CAN_FUNDAMENTALS_REQUIREMENTS.md
├── src/
│   └── automotive_can_validation/
│       ├── __init__.py
│       └── can_identifier.py
├── tests/
│   └── test_can_identifier.py
├── .gitignore
├── pyproject.toml
└── README.md
```

### Directory purpose

* `docs/` contains bilingual technical learning notes.
* `requirements/` contains testable software and validation requirements.
* `src/` contains the actual Python package.
* `tests/` contains automated tests for the implemented behavior.
* `.vscode/` contains shared VS Code project settings.
* `pyproject.toml` defines the Python project, dependencies and test configuration.

---

## Development environment

The project currently uses:

* Python 3.11 or newer
* VS Code
* PowerShell on Windows
* Python virtual environments with `venv`
* `pytest`
* `pytest-cov`
* Git

The main development environment is Windows. Ubuntu will be used later for Linux-specific CAN tools such as SocketCAN.

---

## Local setup

### 1. Open the project directory

```powershell
cd "path\to\automotive-can-validation-lab"
```

### 2. Create a virtual environment

On Windows:

```powershell
py -V:3.12 -m venv .venv
```

On Ubuntu:

```bash
python3 -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Ubuntu:

```bash
source .venv/bin/activate
```

### 4. Install the project and development tools

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The `-e` option installs the project in editable mode, so changes inside `src/` are immediately available without reinstalling the package.

---

## Running the tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Run only the CAN identifier tests:

```powershell
python -m pytest tests/test_can_identifier.py -v
```

Run the tests with coverage:

```powershell
python -m pytest --cov=automotive_can_validation --cov-report=term-missing
```

---

## Testing approach

Tests are written around observable software behavior.

For each feature, the project should normally include:

* Normal valid inputs
* Lower and upper boundary values
* Values immediately outside the valid range
* Invalid or unsupported inputs
* Clear references to the related software requirement

Example relationship:

```text
CAN theory:
Standard identifiers contain 11 bits.

Requirement:
CAN-FND-REQ-001

Implementation:
is_valid_standard_identifier()

Tests:
test_lowest_standard_identifier_is_valid()
test_highest_standard_identifier_is_valid()
test_negative_standard_identifier_is_invalid()
test_identifier_above_standard_range_is_invalid()
```

---

## Scope boundaries

The following functionality is intentionally not implemented yet:

* Detailed Classic CAN frame construction
* Data-frame, remote-frame, error-frame or overload-frame handling
* Bit stuffing
* CRC calculation
* ACK behavior
* Signal bit packing
* Byte order and endianness
* DBC loading
* CAN message encoding or decoding
* `python-can`
* Virtual or physical CAN transmission
* Cyclic transmission processes
* Communication-timeout monitoring logic
* Restbus simulation
* UDS diagnostics
* HIL integration

These topics will be added only after their corresponding theory lessons have been completed.

---

## Planned learning progression

The repository is expected to evolve through separate learning milestones:

```text
0.1.x — CAN fundamentals
0.2.x — Classic CAN frame structure
0.3.x — Signals, scaling and byte order
0.4.x — DBC-based encoding and decoding
0.5.x — Virtual CAN communication
0.6.x — Cyclic transmission and timeout monitoring
0.7.x — Requirements-based ECU validation
```

This roadmap describes the intended direction. It does not claim that these features are already implemented.

---

## Learning objectives

Through this project, I aim to develop practical foundational knowledge in:

* Automotive CAN communication
* Requirements-based development
* Test-case design
* Boundary-value testing
* Python project organization
* Automated testing with `pytest`
* Technical documentation
* Requirements traceability
* Git and GitHub workflows
* German and English automotive terminology

---

## Project status

This repository is an active learning project.

The current implementation represents only the concepts already covered in the CAN fundamentals lesson. The codebase will remain intentionally small until the current milestone has been fully understood, implemented and tested.

---

## Author

**Felipe Rojas**

Mechatronics engineer with a Master of Engineering in Artificial Intelligence for Smart Sensors and Actuators, developing practical knowledge for automotive software, integration and validation roles in Germany.
