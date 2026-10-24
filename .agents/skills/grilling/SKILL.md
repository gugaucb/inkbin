---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Adversarial gates

When the design tree touches architecture, boundaries, or seams, the agent must challenge speculative complexity rather than accepting it:

- **The Cost of Asynchrony & Modular Monolith**: If a proposal introduces message queues, event sourcing, pub/sub, or microservices, challenge it immediately. Demand justification against the Cost of Asynchrony (impact on stack traces, causal tracing, eventual consistency, and deterministic test feedback loops). Recommend the simplest synchronous modular monolith structure with direct function calls at module seams.
- **The Variation Test & Single-Implementation Ban**: If a proposal introduces an abstract interface, factory, strategy, or adapter, require proof of at least **two concrete implementations today**. If only one implementation exists or is planned, flag it as a hypothetical seam and recommend removing the pass-through indirection in favor of a concrete function or module export.
- **The Dependency Rule**: If business logic imports database drivers, ORM decorators, or web framework entities, challenge the inverted dependency direction and recommend shielding the domain core behind a clean seam.
- **Default to Depth**: In recommended answers, always default to the simplest deep module structure (a lot of capability hidden behind a small, intuitive synchronous interface).

