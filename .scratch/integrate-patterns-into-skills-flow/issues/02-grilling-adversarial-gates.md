# 02: Grilling and Stateful Interview Adversarial Gates

**What to build:** Wire adversarial challenge rules from `architecture-patterns` and `design-patterns` into `grill-with-docs` and the core `grilling` protocol, ensuring the agent stress-tests proposals against premature asynchrony, microservices, inverted dependencies, and single-implementation seams during the interview phase.

**Blocked by:** 01: Router Integration and Agent Context Pointers

**Status:** ready-for-agent

- [ ] Update `grill-with-docs` instructions to invoke or consult `architecture-patterns` whenever subsystem boundaries, database persistence, or asynchronous messaging are proposed.
- [ ] Add explicit adversarial grilling checks: if a proposal introduces message queues, event sourcing, or microservices, the agent must challenge it using the Cost of Asynchrony and Modular Monolith principles.
- [ ] Add Variation Test validation to grilling questions: if a new abstract interface or factory is suggested, require proof of 2+ concrete implementations today.
- [ ] Ensure questions adhere to the design tree format, with recommended answers defaulting to the simplest deep-module structure.
