# Replay and Audit Guarantees

This system explicitly separates **replay** and **audit** concerns.
Although related, they serve different purposes and audiences.

---

## Deterministic Replay

### What Replay Is For
- Crash recovery
- Debugging incidents
- Reconstructing historical state

### How Replay Works
- All events are immutable
- Events are replayed in original order
- State is reconstructed deterministically


Replay is designed for **machines**, not humans.

---

## Audit Logging

### What Audit Is For
- Compliance
- Regulatory review
- Human investigation

### Audit Characteristics
- Append-only
- Human-readable JSON
- Records intent and outcomes

Audit records include:
- Order submission
- Trade execution
- Order cancellation
- Order status transitions

---

## Why Replay ≠ Audit

| Replay | Audit |
|-----|------|
| Machine-focused | Human-focused |
| Reconstructs state | Explains actions |
| Requires engine logic | Readable without code |

Mixing these concerns is a common design mistake.
This project keeps them separate by design.

---

## Industry Alignment

This separation mirrors:
- Banking transaction systems
- Exchange compliance pipelines
- Event-sourced financial platforms

It ensures both correctness and regulatory clarity.
