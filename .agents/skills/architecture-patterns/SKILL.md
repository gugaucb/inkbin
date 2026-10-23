---
name: architecture-patterns
description: Shared vocabulary for application macro-structure, dependency direction, and module boundaries. Use when structuring a new project, organizing directory layouts, isolating domain logic from frameworks, planning legacy migrations, or when dependencies point toward infrastructure instead of the core.
---

# Architecture Patterns

Architecture patterns are not deployment blueprints, server topologies, or infrastructure dogma. They are **proven strategies for organizing module boundaries and controlling dependency direction**. This skill maps macroscopic architectural patterns directly to the core principles of **Depth**, **Seams**, **Locality**, and **Testability**.

An architectural pattern earns its keep only when it protects the **depth** of domain models, concentrates business change into **locality**, and preserves rapid, synchronous **testability**. If a pattern introduces layers of indirection without protecting a complex core, it produces shallow modules and must be rejected.

Consult `codebase-design` for foundational micro-level terms (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**). While `codebase-design` governs the anatomy of an individual module, `architecture-patterns` governs how modules are grouped into subsystems and how dependencies flow between them.

## When to invoke

Reach for `/architecture-patterns` (or let the agent invoke it autonomously during project structuring and refactoring) when:

1. **Structuring a New Project:** You need to establish the top-level directory layout, module slices, and import boundaries before writing features.
2. **Inverted Dependency Direction:** Business logic directly imports database drivers, ORM entities, HTTP frameworks, or external SDKs, violating the Dependency Rule.
3. **Legacy Migration:** You need to carve out and extract modules from a legacy monolith incrementally without halting ongoing feature delivery.
4. **Divergent Read/Write Complexity:** The query model (cross-table reporting, denormalized views) diverges fundamentally from the command model (strict transactional invariant enforcement).
5. **Multi-Stage Processing:** Complex data transformation pipelines require isolated, independently testable computation stages.

## When NOT to invoke (Warnings against premature use)

Do **NOT** reach for an architectural pattern if the problem can be solved with a simple modular monolith with standard module exports. Indirection across architectural layers carries heavy cognitive and maintenance overhead; it only pays for itself when real domain complexity or external variation exists.

- **Topology Fallacy:** Never use this skill to decide whether a system should be "Microservices", "Serverless", or "Distributed" on Day 1. Deployment topology is an operational concern, not a code architecture concern. Code should start as a **Modular Monolith**.
- **Astronaut Architecture Ban:** Never introduce Clean Architecture or Hexagonal Architecture with 5 layers of pass-through indirection (controller → use case → domain service → port → adapter → repository) for standard CRUD apps. For simple applications, this creates anemic, shallow modules.
- **Speculative CQRS or Event Sourcing Ban:** Never separate read and write pipelines or adopt event streams unless the domain demands an immutable audit timeline or read projections are demonstrably incompatible with write models.
- **Premature Asynchrony Ban:** Never introduce message brokers, event buses, or pub/sub between internal modules when direct synchronous function calls work. Asynchronous borders obscure stack traces, introduce eventual-consistency bugs, and wreck fast TDD feedback loops.

---

## The Vocabulary (Mapped to Problems)

Patterns are organized by the **architectural friction and dependency flow they resolve**, not by academic classification.

### 1. Protecting the Core (Dependency Direction)

*Ensure the business logic (the deepest module) knows nothing about external databases, APIs, or UI frameworks.*

| Pattern | When to use (The Problem) | Depth & Anti-Pattern Warning |
| :--- | :--- | :--- |
| **Hexagonal (Ports & Adapters)** | The core domain must interact with external systems (databases, message queues, third-party APIs) without coupling to their SDKs or wire formats. The core defines the interfaces (Ports/seams); external modules implement them (Adapters). | **The Variation Test:** Do not create ports for components that do not vary. If there is only one Postgres database and no prospect of swapping or faking outside unit tests, an extra port interface is a hypothetical seam—indirection masquerading as architecture. |
| **Clean / Onion Architecture** | High-complexity enterprise domains requiring strict concentric shielding. All source code dependencies point strictly inward toward Domain Entities. Frameworks and drivers live at the outermost rim. | **Shallow Layer Warning:** For standard CRUD applications, this produces 5 layers of boilerplate where each class just forwards calls to the next. Use only when the domain logic is sufficiently deep to justify the isolation cost. |
| **Layered (N-Tier)** | Traditional horizontal separation into Presentation, Application, Domain, and Infrastructure/Persistence layers. | **High Risk of Transaction Script:** If the Application layer simply moves DTOs to the Persistence layer without domain rules, you have built shallow modules. The Domain layer must be the deepest part of the system. |

### 2. Managing Flow and State

*Address scenarios where read and write requirements diverge radically, or where sequential transformations require strict isolation.*

| Pattern | When to use (The Problem) | Depth & Anti-Pattern Warning |
| :--- | :--- | :--- |
| **CQRS (Command Query Responsibility Segregation)** | The model required to process transactional writes (invariants, validations, locking) is fundamentally incompatible with the model required to serve queries (joins, denormalized read views, full-text search). | **Anti-Pattern Warning:** Do not split read and write models if both execute against the same relational schema with similar throughput. That introduces synchronization complexity with zero leverage. |
| **Event Sourcing** | The business requires a verifiable, append-only ledger of every atomic state change rather than just storing current state (e.g., financial ledgers, audit compliance, collaborative undo). | **High Testability & Query Cost:** Reconstructing state and querying historical projections adds significant overhead. If you only need current state plus an audit log, use standard state persistence with an audit table. |
| **Pipe and Filter** | A complex multi-step data processing workflow must be decomposed into independent, reusable, testable stages where the output of one step feeds the next. | **Excellent for Depth:** Each filter is a deep module with a small interface (`(input: T) => R`), trivially testable in complete isolation with deterministic input fixtures. |

### 3. Boundaries and Migration

*Isolate client-specific interfaces or evolve legacy monoliths without full rewrites.*

| Pattern | When to use (The Problem) | Depth & Anti-Pattern Warning |
| :--- | :--- | :--- |
| **BFF (Backend For Frontend)** | Multiple heterogeneous clients (mobile apps, web apps, third-party integrations) have conflicting payload, latency, or protocol requirements, and a single generic backend API creates bloated, shallow endpoints. | **The Logic Leak Warning:** A BFF is strictly an aggregation and translation adapter. It must **not** contain core business domain logic; it coordinates calls to core backend modules. |
| **Strangler Fig** | You must incrementally replace or extract capabilities from an existing legacy monolith without a high-risk, "stop-the-world" rewrite. | **Transitional Nature:** Strangler Fig is a migration strategy, not a permanent architecture. Intercept traffic at the boundary, route to new deep modules, and decommission old paths until the legacy system is gone. |
| **Microkernel (Plugin)** | The system has a minimal, stable core engine, and features or third-party extensions must be added dynamically without modifying the core. | **Coupling Warning:** Plugins must interact strictly through narrow extension seams. If the core needs internal knowledge of specific plugins, you have an entangled monolith, not a microkernel. |

---

## The Four Principles of Code Architecture

1. **Topology is not Architecture:** Microservices, serverless, and Kubernetes are deployment targets. They do not dictate how code is structured. A **Modular Monolith** with well-defined seams is the default starting point. Only extract independent network services when team autonomy (Conway's Law) or radically different scaling/hardware requirements demand physical boundaries.
2. **The Dependency Rule:** Dependencies must always point inward toward high-policy business logic. Domain models must never import database drivers, web frameworks, or UI libraries. If a domain entity imports an ORM decorator or a framework request object, the architecture is broken.
3. **The Cost of Asynchrony:** Event-driven architectures and message brokers decouple components across time, but make debugging, causal tracing, and TDD exponentially harder. Prefer direct synchronous calls at module seams until independent deployment or queue-buffered durability is genuinely required.
4. **Extract, Don't Anticipate:** Do not build a BFF or separate CQRS read models on Day 1 "in case we need them." Build a single deep module inside the modular monolith. Extract it to a dedicated adapter or separate read pipeline only when production divergence forces the split.

---

## Rejected Framings

- **"We need Clean Architecture for this CRUD service":** Rejected. Clean Architecture is built for domains with complex invariants and diverse delivery channels. For basic data manipulation, it generates 5 layers of anemic, shallow code.
- **"We need Microservices to scale":** Rejected. Microservices address organizational scale across independent teams, not code performance. Start with a well-tested modular monolith.
- **"Event-Driven because it decouples modules":** Rejected. Asynchronous boundaries hide contract breakages and eliminate compile-time safety. Use asynchronous messaging for external integration boundaries, not internal module communication.
- **"Layered Architecture means Controller calls Repository directly":** Rejected. That is an anemic Transaction Script. Domain rules must be encapsulated behind a deep module seam, not bypassed for raw table queries.

---

## Relationships

- **`grilling` / `grill-me`:** The primary challenge partner. `architecture-patterns` provides the **vocabulary** and **rules** (Dependency Rule, Cost of Asynchrony); `grilling` provides the **adversarial test**. When a developer or agent proposes an architectural abstraction ("Let's use Hexagonal Architecture + CQRS"), invoke `grilling` to stress-test the justification:
  - *"Does domain complexity demand framework isolation, or are we adding 5 shallow layers out of habit?"*
  - *"What are the 2+ concrete adapters that justify these ports today?"*
  - *"How does this asynchronous boundary affect synchronous TDD feedback loops?"*
- **`codebase-design`:** Defines the anatomy of a *single* module (small interface, deep implementation, clean seam, adapter). `architecture-patterns` defines how modules are grouped into macroscopic subsystems (layers, slices, hexagonal boundaries) and how dependencies flow between them.
- **`design-patterns`:** Operates at the module and object seam level (GoF patterns like Strategy, Adapter, Facade). `architecture-patterns` operates at the application subsystem level (Ports & Adapters, CQRS, Strangler Fig).
- **`domain-modeling`:** Owns the domain core and ubiquitous language in `GLOSSARY.md`. Architectural patterns exist primarily to shield this domain model from framework drift. If an architecture does not protect the terms defined in `GLOSSARY.md`, it has failed.
- **`improve-codebase-architecture`:** Uses the principles of Strangler Fig and Hexagonal seams to discover shallow modules in legacy codebases and propose deepening refactors.
- **`tdd`:** Dictates that architecture must serve fast, deterministic testability. If an architectural choice (e.g., pure Event Sourcing or internal Pub/Sub) makes it impossible to test business logic synchronously in isolation, the architecture fails the testability bar.
- **`prototype`:** When evaluating two competing macro-structures (e.g., Modular Monolith vs Hexagonal Ports), build a throwaway prototype to test whether the seam feels natural before committing the entire repository.
