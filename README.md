# Order Matching Engine — Systems Design Project

This repository contains a **production-inspired order matching engine**
that demonstrates the **evolution of a financial system** from a
correctness-first concurrent design to a modern, event-driven,
auditable, and crash-recoverable architecture.

The project is intentionally focused on **systems fundamentals**:
correctness, determinism, auditability, and architectural clarity —
not UI or external integrations.

---

## Repository Structure

ORDER-MATCHING-ENGINE/
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── scalability.md
│   └── replay_and_audit.md
│
├── v1_order_matching_engine/
│   ├── main.py
│   ├── concurrency/
│   ├── engine/
│   ├── models/
│   ├── tests/
│   └── utils/
│
├── v2_event_driven_engine/
│   ├── main.py
│   │
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── event_engine.py
│   │   ├── order_book.py
│   │   ├── trade.py
│   │   ├── events.py
│   │   ├── event_log.py
│   │   ├── wal_event_store.py
│   │   ├── audit_event.py
│   │   └── audit_logger.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   └── order.py
│   │
│   └── data/
│       ├── events.wal
│       └── audit.log



Each version is **self-contained**, runnable, and documented.

---

## Project Motivation

Financial trading systems require guarantees that typical application
software does not:

- Fairness (price–time priority)
- Determinism under concurrency
- Auditability and compliance
- Recoverability after failure

This project models how such systems are **designed and evolved in practice**.

---

## Version Overview

### V1 — Concurrent Order Matching Engine

**Goal:** Prove correctness and fairness under concurrency.

**Key characteristics**
- Multi-threaded order submission
- Global lock protecting shared state
- Price–time priority matching
- FIFO fairness per price level
- Deterministic behavior

**Why V1 exists**
V1 establishes a correctness baseline.  
It prioritizes safety and clarity over scalability and mirrors how
early or baseline trading engines are built.

📄 See: `v1_concurrent_engine/README.md`

---

### V2 — Event-Driven Matching Engine (Audit + WAL)

**Goal:** Remove lock contention through architecture and add
real-world guarantees such as audit and crash recovery.

**Key characteristics**
- Event-driven, single-writer matching core
- Lock-free multi-producer submission
- Immutable event sourcing
- Human-readable audit logging
- Write-Ahead Log (WAL) for durability
- Deterministic replay and recovery
- Explicit order lifecycle state machine
- Safe order cancellation

**Why V2 exists**
Instead of optimizing locks, V2 removes them by design.
This mirrors how real exchanges and financial systems are structured.

📄 See: `v2_event_driven_engine/README.md`

---

## High-Level Architecture (V2)

Client Threads
│
▼
+---------------------+
| Lock-Free Queue |
+---------------------+
│
▼
+------------------------------+
| Single Matching Engine |
| (Deterministic, One Writer) |
+------------------------------+
│
├── Trades
├── Event Store (WAL)
└── Audit Log

Only one thread mutates shared state.
Correctness is enforced by architecture, not by locks.

---

## Core Concepts Demonstrated

### 1. Price–Time Priority
Orders are matched by best price first, then FIFO within a price level.

### 2. Determinism
Given the same sequence of events, the engine produces identical results.

### 3. Event Sourcing
Orders, trades, and cancellations are recorded as immutable events.
State is derived from events, not stored as truth.

### 4. Audit vs Replay
- **Replay** reconstructs state for machines (recovery, debugging)
- **Audit logs** explain actions for humans and regulators

These concerns are intentionally separated.

### 5. Write-Ahead Logging (WAL)
All events are written to disk before being applied,
allowing crash recovery and deterministic restart.

---

## Documentation

Detailed design explanations are provided in the `docs/` directory:

- `architecture.md` — system evolution and design decisions
- `scalability.md` — scalability limits and real-world strategies
- `replay_and_audit.md` — replay guarantees and audit model

These documents are written for **engineers and interviewers**.

---

## What This Project Demonstrates

- Concurrency fundamentals
- Event-driven system design
- Deterministic state machines
- Audit and compliance thinking
- Crash recovery via WAL
- Professional system evolution

This is not a feature-driven project.
It is a **systems design and correctness project**.

---

## Intended Audience

- Backend / infrastructure engineers
- Financial systems engineers
- Interviewers evaluating system design depth
- Students learning how real systems are built

---

## Status

- V1: Complete and frozen
- V2: Complete (audit + WAL + recovery)
- Documentation: Complete

This repository is **ready for review and discussion**.

## How to Run

```bash
python main.py
