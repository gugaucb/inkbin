# 06: End-to-End Workflow Validation and Graph Sync

**What to build:** Validate the integrated workflow end-to-end, confirming that `ask-matt` routes queries accurately, `grill-with-docs` applies pattern constraints, `to-spec` enforces dependency checks, `code-review` flags architectural smells, and the knowledge graph is updated via `graphify update .`.

**Blocked by:** 01: Router Integration and Agent Context Pointers, 02: Grilling and Stateful Interview Adversarial Gates, 03: Spec Synthesis and Seam Validation Constraints, 04: Architecture Survey and Deepening Candidate Cards, 05: Code Review Standards Baseline and Anti-Pattern Detection

**Status:** ready-for-agent

- [ ] Verify frontmatter, links, and markdown syntax across all updated skills in `.agents/skills/`.
- [ ] Test scenario: query `ask-matt` with macro-architectural and pattern-selection prompts to verify correct routing recommendations.
- [ ] Test scenario: simulate a review diff containing an inverted dependency and confirm that `code-review` flags it under the Standards axis.
- [ ] Run `graphify update .` to ensure the project knowledge graph incorporates all modified agent skills and documentation.
