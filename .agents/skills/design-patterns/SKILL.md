---
name: design-patterns
description: Shared vocabulary for applying Gang of Four patterns to design deep modules, isolate seams, and improve testability. Use when facing concrete implementation variation (2+ variants), complex creation logic, tangled cross-module communication, or dynamic state transitions.
---

# Design Patterns

Design patterns are not trophies, blueprints to enforce, or architectural dogma. They are **proven solutions to recurring friction** at module seams. This skill maps classic Gang of Four (GoF) patterns directly to the core principles of **Depth**, **Seams**, **Locality**, and **Testability**.

A design pattern earns its keep only when it increases **leverage** for callers (more capability behind a smaller interface) and concentrates complexity into **locality** for maintainers. If a pattern introduces indirection without real variation, it is a shallow module and must be rejected.

Consult the vocabulary in `codebase-design` for foundational terms (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**).

## When to invoke

Reach for `/design-patterns` (or let the agent invoke it autonomously during design and refactoring) when the code exhibits specific architectural friction:

1. **Implementation Variation:** Multiple concrete mechanisms exist (or are immediately imminent) to perform a capability, and the caller must not know which mechanism is running.
2. **Creation Complexity:** Object assembly, validation invariants, or wiring requires significantly more knowledge than using the resulting object (a creation seam is needed).
3. **Tangled Communication:** Peer modules depend directly on each other in an N-to-N mesh, destroying locality and making isolated testing impossible.
4. **Access Control or State Transitions:** You must intercept, cache, audit, or transition execution state without polluting core business logic.

## When NOT to invoke (Warnings against premature use)

Do **NOT** reach for a design pattern if the problem can be solved with a simple function, an object literal, a callback, or a direct `if/else`. Indirection always carries cognitive load and maintenance costs; it only pays for itself when real variation exists.

- **The Single-Implementation Ban:** Never introduce an abstract factory, strategy interface, or adapter for a single concrete implementation. One adapter is a *hypothetical seam*—indirection masquerading as architecture.
- **No Pattern-First Design:** Never start with "We need a Factory here." Start with the friction: what is caller code struggling with? What seam is leaking?
- **TypeScript Idioms over Enterprise Boilerplate:** Never construct multi-class hierarchies when a higher-order function, a closure, or a plain TypeScript type alias achieves the same seam with zero ceremony.

---

## The Vocabulary (Mapped to Problems)

Patterns are organized by the **architectural friction they resolve**, not by academic classification.

### 1. Managing Creation Seams (Creational)

*Isolate instantiation complexity so caller code remains clean and focused on usage. When instantiation logic changes, only one place in the codebase edits.*

| Pattern | When to use (The Problem) | Depth & Anti-Pattern Warning |
| :--- | :--- | :--- |
| **Factory Method** | The caller needs an instance but must delegate the exact concrete choice to submodules or runtime configuration. | **The Variation Test:** If there is only one concrete implementation, do not use. It is pure pass-through overhead (a shallow module). |
| **Abstract Factory** | You must produce families of related, interdependent objects without binding callers to concrete classes. | Keep the factory interface small. Never create an Abstract Factory for a single object type. |
| **Builder** | Object creation involves many sequential steps, intricate validation rules, or numerous optional configurations. | The Builder interface must be fluent and completely encapsulate internal validation invariants. Do not expose intermediate unvalidated state. |
| **Prototype** | Creating an instance from scratch is costlier or more complex than cloning a pre-configured template (e.g., state trees). | In modern JS/TS, prefer native structured cloning (`structuredClone`) or immutable utility libraries over custom class-based `clone()` hierarchies. |
| **Singleton** | Strictly mandatory to enforce exactly one shared instance with coordinated state (e.g., connection pools). | **High Risk.** In modern JS/TS, prefer module-scoped exports (`export const db = ...`). Never use Singletons as hidden global variables to bypass dependency injection. |

### 2. Managing Seams and Adapters (Structural)

*Compose modules behind narrow, deep interfaces or bridge incompatible boundaries without contaminating the domain core.*

| Pattern | When to use (The Problem) | Depth & Anti-Pattern Warning |
| :--- | :--- | :--- |
| **Adapter** | An external third-party or legacy module presents an interface incompatible with your domain's required seam. | The adapter translates across the seam; it must **not** introduce new domain business logic. |
| **Facade** | A subsystem consists of multiple shallow, entangled modules, but callers only need a clean, high-level capability. | **Canonical Deep Module.** A great facade hides vast subsystem complexity behind a tiny, intuitive interface. Maximizes leverage. |
| **Decorator** | Need to dynamically attach cross-cutting responsibilities (logging, metrics, retries) to individual objects without subclassing. | Beware the "decorator onion": deeply nested decorators make error traces and stack debugging illegible. Keep wrapping shallow. |
| **Proxy** | Need transparent control over object access (lazy loading, caching, permissions, rate-limiting) at the seam. | The Proxy must be strictly transparent to the caller, adhering identically to the target interface. |
| **Composite** | Callers must treat individual items and tree-like groups of items uniformly through the exact same interface. | Ensure the shared interface is genuinely meaningful for both leaves and composites. Never force methods that throw "Not Implemented" on leaves. |
| **Bridge** | An abstraction and its implementation vary independently along orthogonal dimensions. | Avoid unless multi-dimensional variation is proven. Prefer simple composition before splitting into dual class hierarchies. |
| **Flyweight** | The application creates tens of thousands of fine-grained objects causing memory exhaustion, and state splits into intrinsic (shared) and extrinsic (context). | **High Risk to Locality.** Shared mutable state causes silent side-effects. Reach for Flyweight only after memory profiling confirms necessity. |

### 3. Managing Communication and State (Behavioral)

*Govern how modules interact across seams, preserving low coupling and straightforward testability.*

| Pattern | When to use (The Problem) | Depth & Anti-Pattern Warning |
| :--- | :--- | :--- |
| **Strategy** | Multiple algorithms or business policies exist for a task and must be swappable at runtime or in tests. | **In TypeScript, prefer higher-order functions or callbacks** (`type Strategy = (data: T) => R`) over heavy class hierarchies. |
| **Observer** | A module must broadcast state changes to multiple subscribers without knowing their concrete identities. | **High Testability Risk.** Uncontrolled event cascades are notoriously hard to debug. Prefer explicit return values, callbacks, or typed event streams. |
| **Command** | Need to decouple request invokers from executors, enabling queued jobs, transactional logging, or undo/redo. | The Command object should be a lightweight data payload (a message/token), not a dump of execution logic. |
| **State** | A module's behavior changes drastically based on internal lifecycle state, causing massive nested `if/else` conditionals. | Each state is an adapter satisfying the same interface. The context delegates execution; it does not decide branching inline. |
| **Chain of Responsibility** | A request can be handled by multiple candidate handlers in a pipeline, and sender doesn't care which handles it. | **High Risk of Obscure Flow.** Stepping through dynamic chains in a debugger is painful. Use only when the pipeline order is truly dynamic. |
| **Mediator** | Direct N-to-N relationships between peer modules create an unmaintainable dependency knot. | The Mediator coordinates message passing; it must **not** become a "God Object" holding domain business rules. |
| **Memento** | Need to capture and externalize an object's internal snapshot (e.g. undo history) without violating encapsulation. | The Memento must remain opaque to external modules. Only the originating module reads or unpacks the state. |
| **Iterator** | Need to traverse a custom collection's elements sequentially without exposing its underlying internal structure. | In modern JS/TS, implement native iterable protocols (`[Symbol.iterator]` or generator functions `yield*`). |
| **Template Method** | An algorithm's high-level skeleton is fixed, but specific steps vary across variants. | **Prefer Composition (Strategy) over Inheritance (Template Method).** Subclassing creates rigid compile-time coupling and complicates testing. |
| **Visitor** | Need to execute new operations across a heterogeneous composite structure without modifying the element classes. | **High Risk.** Breaks encapsulation across elements. Use only when the object structure is frozen and operations change frequently. |
| **Interpreter** | Need to evaluate sentences in a small, well-defined domain-specific grammar. | Rarely needed in application code. Reach for established parser libraries before hand-rolling an interpreter. |

---

## Principles

1. **The Variation Test:** Do not introduce a pattern (especially Factory, Strategy, or Adapter) unless you can point to at least **two** real or strongly anticipated concrete implementations. One implementation is a hypothetical seam—unnecessary indirection.
2. **Composition over Inheritance:** Patterns relying on deep inheritance (Template Method) tightly couple code at compile-time. Prefer patterns built on composition and dependency injection (Strategy, Adapter, Decorator) to keep seams swappable and testable.
3. **TypeScript & Modern Idiomatic Simplicity:** Many GoF patterns were workarounds for missing language features in 1990s C++ and Java. In modern TypeScript:
   - A **Strategy** is a function type: `type PriceRule = (cart: Cart) => Money`.
   - A **Singleton** is a module export: `export const authClient = ...`.
   - An **Iterator** is `[Symbol.iterator]()`.
   Do not introduce class scaffolding when a plain function or object literal yields a deeper module.
4. **The Interface is the Test Surface:** Any pattern applied must make the module *easier* to test through its public interface. If testing requires mocking private pattern classes or jumping through setup hoops, the pattern was misapplied.
5. **The Deletion Test:** Mentally delete the pattern. If complexity vanishes, it was pass-through ceremony. If complexity reappears scattered across callers, the pattern was providing genuine leverage.

---

## Rejected Framings

- **"Using Pattern X because it's standard best practice":** Rejected. Patterns are targeted remedies for specific design friction, not decorations.
- **Patternitis (Ceremony Inflation):** Creating 5 classes (AbstractFactory, Factory, ProductInterface, ConcreteProduct, FactoryProvider) where a simple configuration dictionary and a factory function solve the problem in 10 lines.
- **Singleton as a Dependency Shortcut:** Reaching for a Singleton to avoid passing parameters or injecting dependencies. This obscures dependencies, breaks locality, and ruins test isolation.
- **Inheritance for Code Sharing:** Subclassing or using Template Method purely to reuse helper methods. Extract pure utility functions or compose a collaborator instead.

---

## Relationships

- A **Strategy** or **Adapter** is a concrete **Adapter** sitting at a **Seam** (as defined in `codebase-design`).
- A **Facade** is the direct realization of a **Deep Module**: a narrow interface encapsulating broad internal complexity.
- A **Factory** isolates an internal creation seam; test its validity with the **Deletion Test**.
