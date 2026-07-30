# Automotive CAN Validation Lab - New Project Brief

## Use this document

This project is intentionally starting from zero. Give this document, the project README, and the milestone roadmap to the first Codex chat working in the new repository.

There is no existing implementation, environment configuration, `AGENTS.md`, CI workflow, or dependency decision to preserve.

## Project identity

- **Project name:** Automotive CAN Validation Lab
- **Repository name:** `automotive-can-validation-lab`
- **Project type:** Learning-first, portfolio-quality automotive software simulation
- **Primary objective:** Learn Controller Area Network (CAN) communication by building a tested virtual automotive network containing several simulated ECUs.

## Final vision

The completed project will simulate a small vehicle network with a virtual CAN bus, a powertrain ECU, body-control ECU, instrument cluster, diagnostic tester, and validation runner.

It must demonstrate:

- Classical CAN frames, IDs, broadcast communication, and arbitration
- Periodic ECU messages, subscriptions, freshness, and timeout handling
- DBC-based signal encoding and decoding
- A small educational ISO-TP/UDS diagnostic flow
- Automated validation scenarios and fault injection
- Professional engineering practices: packaging, tests, linting, documentation, CI, and reproducibility

## Learning and engineering approach

- Build one small, working increment at a time.
- Explain the relevant CAN and software-engineering concepts before or while implementing them.
- Add tests and documentation with every feature.
- Prefer a deterministic simulation clock to real time.
- Keep protocol models, bus simulation, ECU behaviour, signal decoding, diagnostics, and validation code in separate modules.
- Use fictional CAN identifiers, DBC signals, ECU data, and diagnostic values.
- Prioritize clarity and correctness over feature count.

## Initial technical direction

Use Python for the initial project because it gives a fast learning and test-feedback loop.

The expected baseline is:

| Concern | Initial direction |
|---|---|
| Packaging and dependencies | `pyproject.toml` and `uv` |
| Test framework | pytest |
| Coverage | pytest-cov |
| Formatting and linting | Ruff |
| Type checking | Start with Pylance in VS Code; select a CI type checker later if useful |
| Continuous integration | GitHub Actions |
| Signal/DBC handling | `cantools` when the DBC milestone begins |
| Virtual CAN integration | Linux SocketCAN `vcan` after the pure-Python simulator works |
| C++ | Add only later as a focused extension, not at project initialization |
| Docker/Dev Container | Add only when the project needs reproducible Linux or SocketCAN tooling |

The developer should select the actual supported Python version after checking the local environment and dependency compatibility. Do not guess or pin an unavailable version.

## Environment assumptions

- Development computer: Windows
- Editor: VS Code with the Codex extension
- Preferred runtime environment for later CAN, ROS, C++, Docker, and SocketCAN work: WSL/Ubuntu

The project must not assume WSL, Docker, or a CAN adapter is already installed. Begin with a normal Python environment. Add platform-specific integration only after the core simulator is tested.

## Scope boundaries

### In scope

- Classical CAN first
- Standard and extended CAN identifiers
- Frame validation and logging
- Virtual bus broadcast and arbitration
- Simulated ECUs and periodic messages
- DBC signals
- Small, explicitly educational ISO-TP and UDS subset
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

1. **Milestone 0 - Engineering foundation**
2. **Milestone 1 - CAN fundamentals and frame model**
3. **Milestone 2 - Deterministic virtual CAN bus**
4. **Milestone 3 - Virtual automotive ECUs**
5. **Milestone 4 - Signal and DBC layer**
6. **Milestone 5 - Diagnostic communication**
7. **Milestone 6 - ECU validation framework**
8. **Milestone 7 - Integrated Automotive CAN Validation Lab**

The detailed goals, deliverables, and definitions of done belong in `automotive_can_validation_lab_milestones.md`. Do not skip a milestone unless the user explicitly changes the roadmap.

## First Codex request

Use the following message in the new project chat:

```markdown
I am starting the Automotive CAN Validation Lab repository from zero.

Read these documents before making changes:
- README.md
- docs/automotive_can_validation_lab_milestones.md
- docs/automotive_can_validation_lab_project_brief.md

There is no existing code, environment, CI, or AGENTS.md to preserve.

Please implement **Milestone 0 only**. First inspect the empty repository and the available environment. Then propose and implement a minimal professional Python baseline with:

1. A sensible source and test layout
2. `pyproject.toml` and reproducible dependency management with `uv`
3. pytest, coverage, and Ruff configuration
4. A minimal smoke test
5. GitHub Actions CI for test, lint, and formatting checks
6. Clear README setup and verification commands

Explain the decisions briefly. Do not start CAN frame or bus implementation until Milestone 0 passes locally.
```

## When to create AGENTS.md

Do not create `AGENTS.md` before the project commands are known. At the end of Milestone 0, create a concise `AGENTS.md` that contains only verified information, such as:

- The environment setup command
- Test, coverage, lint, and format-check commands
- Source and test locations
- The rule that each milestone requires tests and documentation
- The rule that CAN IDs and signal data are fictional unless documented otherwise

## Definition of progress

For every milestone, completion requires all of the following:

1. The intended behaviour is implemented.
2. Unit tests cover normal, boundary, and failure behaviour where relevant.
3. Formatting, linting, and tests pass locally.
4. CI runs the same essential checks.
5. Documentation explains the CAN concept and how to run the demonstration.
6. The next milestone is not started until the current milestone's definition of done is met.

## Files to transfer into the new repository

```text
README.md
docs/automotive_can_validation_lab_milestones.md
docs/automotive_can_validation_lab_project_brief.md
```

These documents are sufficient to begin from zero. The new chat should inspect the actual machine and repository before choosing final versions, commands, or optional tooling.
