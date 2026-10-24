# 05: Code Review Standards Baseline and Anti-Pattern Detection

**What to build:** Extend the Standards sub-agent smell baseline in `code-review` to detect architectural violations (such as domain models importing HTTP or database drivers directly) and design pattern ceremony inflation (such as single-implementation factories or singleton abuse).

**Blocked by:** 01: Router Integration and Agent Context Pointers

**Status:** closed

- [x] Add architectural smell checks to `code-review` step 3 baseline: "Inverted Dependency" (core business logic directly importing web frameworks, ORMs, or external client libraries).
- [x] Add design pattern smell checks to `code-review` step 3 baseline: "Patternitis / Single-Implementation Seam" (introducing abstract factories, strategies, or adapters for only 1 concrete implementation).
- [x] Add "Singleton Abuse" smell (using singletons as hidden global variables bypassing dependency injection).
- [x] Ensure that the sub-agent prompt instructions in step 4 pass these newly defined smells to the Standards sub-agent.
