---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

# Grill with Docs

Call the Skill tool for "grilling" and "domain-modeling".

During the interview:
- Consult `architecture-patterns` whenever subsystem boundaries, database persistence, or asynchronous messaging are proposed. Enforce the Dependency Rule and Modular Monolith baseline.
- Consult `design-patterns` whenever object creation, swappable policies, or adapters are suggested. Enforce the Variation Test (2+ concrete implementations required today).
- Record hardened decisions as ADRs under `docs/adr/` and ubiquitous domain terms in `GLOSSARY.md`.
