# Automotive CAN Validation Lab

> A test-driven virtual environment for learning, simulating, and validating automotive Controller Area Network (CAN) communication.

## Overview

**Automotive CAN Validation Lab** is an educational software-engineering project that models a simplified automotive CAN network with multiple virtual Electronic Control Units (ECUs).

The project combines CAN protocol fundamentals, automotive communication concepts, simulation, automated testing, and CI/CD practices. Its objective is to evolve from small, understandable CAN components into an integrated virtual vehicle network validation environment.

Repository name: `automotive-can-validation-lab`

## Goals

- Learn CAN communication concepts through implementation.
- Simulate message-based communication between virtual ECUs.
- Model CAN arbitration, periodic transmission, message reception, and timeouts.
- Decode and encode vehicle signals using DBC-style definitions.
- Implement a limited diagnostic communication workflow.
- Validate expected ECU behaviour through automated scenarios and fault injection.
- Apply professional software-development practices: packaging, tests, linting, documentation, CI, and reproducible environments.

## Core Concepts

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

## Planned Architecture

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
