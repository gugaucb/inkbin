# Spec: Integration of Design Patterns and Architecture Patterns into the Skills Flow

Status: completed

## Problem Statement

The developer and project maintainers have established two rich foundational skills—one governing macroscopic module boundaries and dependency directions (`architecture-patterns`) and another governing GoF patterns at module seams under strict variation constraints (`design-patterns`). However, within the agent's active operational workflow (which starts with `grill-me` or `grill-with-docs` and is routed via `ask-matt`), these skills are never invoked or consulted.

Because these skills remain disconnected from the core workflow:
1. Architectural and design proposals developed during grilling interviews frequently introduce unvetted layers of indirection, premature asynchrony, or anemic pass-through abstractions without being challenged.
2. Specifications produced by the agent fail to formalize dependency directions or verify the Variation Test (requiring at least two concrete implementations before introducing an adapter seam).
3. Code reviews evaluate general code smells but miss critical architectural leaks, such as domain logic importing infrastructure adapters or enterprise pattern ceremony inflation.

## Solution

Seamlessly connect `architecture-patterns` and `design-patterns` into the lifecycle of the agent skills workflow:
1. **Routing and Discovery**: Incorporate both skills into the central skill router under foundational vocabulary, ensuring the agent and the developer know precisely when to reach for them.
2. **Adversarial Grilling**: Wire architectural and pattern validation directly into the grilling interview process, empowering the agent to stress-test proposals against the Dependency Rule, the Cost of Asynchrony, and the Single-Implementation Ban.
3. **Specification Formalization**: Require feature specifications to validate seam choices and dependency flow against architectural principles during synthesis.
4. **Codebase Upkeep**: Equip architectural survey workflows to evaluate candidate refactorings using macro-patterns (like Strangler Fig and Hexagonal seams) and micro-patterns (like Facade and Strategy).
5. **Continuous Review**: Augment automated code review baselines to detect inverted dependency directions and premature pattern abstraction before code lands on the main branch.

## User Stories

1. As an engineer asking the router which skill fits my architectural problem, I want to be directed to the architecture patterns skill, so that I can choose the appropriate subsystem boundaries and dependency directions.
2. As an engineer asking the router which skill fits a complex object wiring or swappable policy problem, I want to be directed to the design patterns skill, so that I can apply idiomatic solutions to friction at seams.
3. As an engineer proposing a new feature in a grilling interview, I want the agent to challenge me if my proposal introduces microservices or message queues prematurely, so that the application remains a simple modular monolith.
4. As an engineer proposing an abstract interface in a grilling interview, I want the agent to verify if two or more concrete implementations exist today, so that hypothetical seams are rejected immediately.
5. As an architect participating in grilling rounds, I want the agent to verify that domain concepts remain shielded from external framework drivers, so that business logic remains pure and testable.
6. As a developer having a spec generated from an interview, I want the spec to explicitly evaluate dependency directions in its implementation decisions, so that implementers do not leak HTTP or database concerns into core domain models.
7. As a developer having a spec generated, I want the spec to prohibit pass-through boilerplate layers for standard data operations, so that only genuine domain depth is enclosed in ports and adapters.
8. As an engineer breaking a spec into tickets, I want tickets to declare clear seams at the highest possible level, so that implementers can drive fast, deterministic unit and integration tests.
9. As a developer implementing a ticket, I want the agent to favor language idioms (such as function types, closures, or module exports) over heavy class hierarchies, so that the codebase remains idiomatic and lightweight.
10. As a developer running an architecture review survey, I want candidate deepening opportunities to suggest structural patterns like Facade or Strangler Fig where appropriate, so that refactorings have clear blueprints.
11. As a tech lead running an automated code review on a pull request, I want the standards reviewer to flag direct imports of database drivers or framework entities inside the domain core, so that architectural boundaries are preserved.
12. As a tech lead running an automated code review, I want the standards reviewer to detect and flag single-implementation factories or speculative decorators, so that unnecessary indirection is eliminated.
13. As an agent navigating the repository, I want clear context pointers with positive triggers in the repository agent rules, so that I load pattern skills only when relevant decisions are actively being made.
14. As a developer, I want all pattern skills to remain aligned with the core vocabulary of deep modules and seams, so that the team speaks one unified design language.

## Implementation Decisions

- **Router Module Updates**:
  - The central router's vocabulary tier will be expanded to declare architecture patterns (governing macro-structure and dependency flow) and design patterns (governing seam-level GoF solutions) alongside domain modeling and codebase design.
  - Clear branch triggers will be established so that callers encountering subsystem boundary decisions or implementation variation are routed efficiently.

- **Interview and Grilling Module Updates**:
  - The stateful interview skill will be updated to consult architectural rules whenever subsystem borders, data persistence, or asynchronous communication are introduced.
  - The interview protocol will incorporate explicit adversarial challenge prompts: testing for at least two concrete adapters, checking the cost of asynchrony on deterministic tests, and ensuring domain shielding.

- **Specification Synthesis Module Updates**:
  - The specification generation skill will update its seam evaluation criteria: existing high-level seams must be preferred, dependencies must point inward toward business policy, and anemic multi-layer indirection for standard CRUD operations must be rejected.
  - The implementation decisions section of generated specs must explicitly state how proposed module interfaces satisfy depth and locality without speculative generality.

- **Architecture Survey Module Updates**:
  - The codebase architecture survey skill will incorporate pattern classifications into candidate cards, highlighting where deep module facades or strangler boundaries provide high leverage.

- **Review and Standards Module Updates**:
  - The code review standards evaluator will be provided with specific architectural violation checks: detecting the Dependency Rule breach (domain importing infrastructure) and detecting pattern inflation (such as single-implementation factories or unnecessary singletons).

- **Documentation and Agent Guidance**:
  - The repository's primary agent guide will be updated to explicitly register both skills within the agent skills directory, establishing clear context pointers so subsequent agent sessions recognize them autonomously.

## Testing Decisions

- **What Makes a Good Test**:
  - A good test exercises observable behavior and routing fidelity: verifying that agents presented with architectural dilemmas actively reference and apply the principles (Dependency Rule, Variation Test, Single-Implementation Ban) without regressing into pass-through ceremony.
  - Structural tests verify frontmatter validity, schema compliance, context pointer sharpness, and link integrity across all skill definition files.

- **Modules to be Tested**:
  - Router skill dispatch behavior when given scenario-based architectural and design queries.
  - Specification synthesis behavior to ensure generated specs include seam rationale and dependency checks.
  - Code review standards prompt evaluation against sample diffs containing architectural boundary leaks.

- **Prior Art**:
  - Pre-existing skill definitions and issue tracker workflows under the project agents documentation.
  - Specification formats previously proven in the project feature issue tracker.

## Out of Scope

- Modifying the external upstream skill repository; all adjustments are maintained within this project's local agent environment.
- Altering the fundamental deep-module design definitions (module, interface, depth, seam, adapter, leverage, locality), which remain the foundational source of truth.
- Forcing mandatory pattern adoption on simple, cohesive functions that do not exhibit architectural friction.

## Further Notes

- By embedding these rules directly into the interview, specification, and review phases, the agent ecosystem becomes self-regulating, preventing architectural drift and boilerplate accumulation across all future feature builds.
