# CAN Fundamentals — Software Requirements

## Purpose

This document defines the testable software requirements implemented during the CAN Fundamentals learning milestone.

The implementation is intentionally limited to concepts covered in `docs/learning_notes/01_CAN_Fundamentals.md`.

Real CAN transmission, detailed frame construction, DBC processing and physical-bus behavior are outside the scope of this milestone.

---

## Identifier requirements

### CAN-FND-REQ-001 — Standard identifier validation

The software shall classify integer identifiers from `0x000` through `0x7FF`, inclusive, as valid standard CAN identifiers.

Integer values below `0x000` or above `0x7FF` shall be classified as invalid standard CAN identifiers.

### CAN-FND-REQ-002 — Extended identifier validation

The software shall classify integer identifiers from `0x00000000` through `0x1FFFFFFF`, inclusive, as valid extended CAN identifiers.

Integer values below `0x00000000` or above `0x1FFFFFFF` shall be classified as invalid extended CAN identifiers.

---

## Arbitration requirement

### CAN-FND-REQ-003 — Identifier priority

When comparing two valid CAN identifiers of the same identifier format, the software shall classify the numerically smaller identifier as having the higher arbitration priority.

Detailed mixed standard-versus-extended arbitration is outside the scope of this milestone.

---

## Signal-conversion requirement

### CAN-FND-REQ-004 — Raw-to-physical conversion

The software shall calculate a physical signal value using:

```text
physical_value = raw_value × factor + offset
```

Bit packing, byte order and DBC-based decoding are outside the scope of this milestone.

---

## Timing requirements

### CAN-FND-REQ-005 — Cycle-time conversion

For a positive message cycle time expressed in milliseconds, the software shall calculate the nominal transmission frequency in hertz using:

```text
frequency_hz = 1000 / cycle_time_ms
```

A cycle time of zero or less shall be rejected.

### CAN-FND-REQ-006 — Communication-timeout evaluation

The software shall report a communication timeout when the elapsed time since the last valid message is greater than or equal to the configured timeout threshold.

The exact boundary for this learning project is therefore:

```text
elapsed_time >= timeout_threshold
```

Negative elapsed times or non-positive timeout thresholds shall be rejected.

---

## Protocol-limit requirement

### CAN-FND-REQ-007 — Maximum payload size

The software shall define the following maximum application payload sizes:

* Classic CAN: 8 bytes
* CAN FD: 64 bytes

The software shall be able to determine whether a requested payload length is valid for the selected protocol type.

Detailed frame fields and Data Length Code encoding are outside the scope of this milestone.

---

## Traceability

| Requirement       | Planned module         | Planned test file           |
| ----------------- | ---------------------- | --------------------------- |
| `CAN-FND-REQ-001` | `can_identifier.py`    | `test_can_identifier.py`    |
| `CAN-FND-REQ-002` | `can_identifier.py`    | `test_can_identifier.py`    |
| `CAN-FND-REQ-003` | `arbitration.py`       | `test_arbitration.py`       |
| `CAN-FND-REQ-004` | `signal_conversion.py` | `test_signal_conversion.py` |
| `CAN-FND-REQ-005` | `timing.py`            | `test_timing.py`            |
| `CAN-FND-REQ-006` | `timing.py`            | `test_timing.py`            |
| `CAN-FND-REQ-007` | `protocol_limits.py`   | `test_protocol_limits.py`   |

---

## Out of scope

The following topics are not implemented in this milestone:

* Detailed Classic CAN frame fields
* Frame serialization
* Bit stuffing
* CRC calculation
* ACK behavior
* CAN error frames
* Signal bit packing
* Endianness
* DBC loading
* `python-can`
* Virtual or physical bus transmission
* Cyclic transmission processes
* Real-time scheduling
* Restbus simulation
* UDS diagnostics
