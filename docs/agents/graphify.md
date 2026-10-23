# Graphify Knowledge Graph

Transforms codebases, documentation, SQL schemas, configurations, and PDFs into a queryable knowledge graph using AST parsing (tree-sitter) and semantic analysis.

## Core Commands

- **Build graph**: `graphify .` (or `graphify <path> --mode deep`)
- **Incremental update**: `graphify update .` (fast, AST-only, no API cost)
- **Query graph**: `graphify query "<question>"` (BFS traversal; add `--dfs` for specific path trace)
- **Trace path**: `graphify path "<NodeA>" "<NodeB>"` (finds shortest path between two concepts/symbols)
- **Explain node**: `graphify explain "<Concept>"` (structural breakdown of a module, class, or symbol)

## Outputs (`graphify-out/`)

- `graph.json`: Structured graph data for GraphRAG and semantic queries
- `GRAPH_REPORT.md`: Audit report with god nodes, surprising connections, and suggested questions
- `graph.html`: Interactive visual graph (open in browser)
- `wiki/` (optional via `--wiki`): Agent-crawlable markdown wiki
- `obsidian/` (optional via `--obsidian`): Obsidian vault with bidirectional backlinks

## Agent Guidelines

1. **Check graph first**: When `graphify-out/graph.json` exists, use `graphify query` or `graphify path` before doing broad file greps.
2. **Keep updated**: After editing code, run `graphify update .` to keep graph topology in sync without incurring LLM token costs.
3. **Skill reference**: Full interactive workflow and flags in `.agents/skills/graphify/SKILL.md` (or run `/graphify`).
