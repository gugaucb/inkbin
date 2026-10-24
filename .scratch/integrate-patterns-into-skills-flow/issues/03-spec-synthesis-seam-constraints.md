# 03: Spec Synthesis and Seam Validation Constraints

**What to build:** Update `to-spec` so that generated specifications explicitly evaluate dependency directions and seam choices against `architecture-patterns` and `design-patterns`, forbidding pass-through multi-layer indirection for standard CRUD while ensuring domain models remain shielded from framework drivers.

**Blocked by:** 02: Grilling and Stateful Interview Adversarial Gates

**Status:** closed

- [x] Update `to-spec` step 2 ("Sketch out the seams") to enforce the Dependency Rule (dependencies pointing inward toward high-policy business rules).
- [x] Require the Implementation Decisions section of the spec template to evaluate module depth and reject anemic 5-layer pass-through architectures for simple data operations.
- [x] Ensure that any proposed GoF structural or behavioral adapter in the spec satisfies the Variation Test (at least 2 concrete implementations).
- [x] Verify that spec instructions prohibit speculative code scaffolding while keeping existing high-level test seams.
