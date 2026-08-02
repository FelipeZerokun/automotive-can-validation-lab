# CAN fundamentals and frame model

This document defines the concepts and software contract used by Milestone 1 of
the Automotive CAN Validation Lab. The implementation is an educational logical
model of a Classical CAN data frame, not a physical CAN controller.

## Message-oriented broadcast communication

CAN is a shared broadcast network. A transmitting node places a frame on the
bus, and every connected node can observe it. Frames carry identifiers rather
than source or destination addresses. Receiving nodes decide which identifiers
are relevant to them.

When multiple nodes begin transmitting simultaneously, the identifier also
participates in non-destructive arbitration. Dominant bits overwrite recessive
bits, so a numerically lower identifier has higher priority. Arbitration belongs
to the virtual-bus simulation in Milestone 2; Milestone 1 only validates and
stores the identifier.

## Logical Classical CAN data frame

```text
+-----+-------------+---------+----------+------+-----+-----+
| SOF | Arbitration | Control | Data     | CRC  | ACK | EOF |
+-----+-------------+---------+----------+------+-----+-----+
                         |       |
                         |       +-- 0 to 8 payload bytes
                         +---------- includes the DLC
```

- **SOF (Start of Frame):** marks the beginning of a frame.
- **Arbitration field:** carries the identifier and arbitration-related bits.
- **Control field:** includes the Data Length Code (DLC), which describes the
  payload length for this model.
- **Data field:** contains zero through eight bytes in Classical CAN.
- **CRC field:** allows receivers to detect transmission errors.
- **ACK field:** allows receivers to acknowledge a correctly received frame.
- **EOF (End of Frame):** marks the end of the frame.

The lab's `CanFrame` stores the application-visible identifier, frame format,
payload, and simulation timestamp. CRC calculation, acknowledgement, bit
stuffing, and electrical signaling are outside this model.

## Standard and extended identifiers

| Format | Identifier width | Inclusive range | Display width |
|---|---:|---:|---:|
| Standard | 11 bits | `0x000` to `0x7FF` | 3 hexadecimal digits |
| Extended | 29 bits | `0x00000000` to `0x1FFFFFFF` | 8 hexadecimal digits |

`is_extended` selects which range applies. It does not convert an identifier
from one format to the other.

## `CanFrame` contract

`CanFrame` is an immutable value object with the following fields:

| Field | Accepted input | Stored value | Validation |
|---|---|---|---|
| `identifier` | `int`, excluding `bool` | `int` | Must fit the selected 11-bit or 29-bit range |
| `is_extended` | `bool` | `bool` | Must be exactly a Boolean value |
| `data` | `bytes`, `bytearray`, or `memoryview` | `bytes` | Must contain zero through eight bytes |
| `timestamp` | `int` or `float`, excluding `bool` | `float` | Finite and non-negative, measured in simulation seconds |

Mutable payload inputs are copied to `bytes`. Changing the original
`bytearray` after construction therefore cannot change an existing frame.

The timestamp is simulation time in seconds rather than wall-clock time. This
keeps later bus simulations repeatable and permits integer or fractional time
values without reading the computer's clock.

## Validation errors

- Raise `TypeError` when a field has an unsupported input type.
- Raise `ValueError` when the type is supported but the value is outside its
  permitted range.
- Error messages identify the invalid field and its expected constraint.

## Equality and immutability

Two frames are equal when all four normalized fields are equal. A frame's
fields cannot be reassigned after construction. Hashability follows from the
same immutable value semantics, allowing frames to be used in sets and as
dictionary keys.

## Stable log representation

Standard frames use three identifier digits and extended frames use eight.
Payload bytes use uppercase hexadecimal separated by spaces. Timestamps use six
digits after the decimal point:

```text
CanFrame(id=0x123, format=standard, dlc=2, data=AA 55, timestamp=1.250000s)
CanFrame(id=0x00000123, format=extended, dlc=0, data=, timestamp=0.000000s)
```

The DLC in this representation is derived from `len(data)`; it is not stored as
a separate field that could disagree with the payload.

## Scope boundary

This model deliberately does not simulate wire timing, electrical levels,
transceiver behavior, bit stuffing, CRC generation, acknowledgement errors,
error frames, remote frames, overload frames, or CAN FD payloads. Those
omissions keep Milestone 1 focused on a safe logical Classical CAN data-frame
model.
