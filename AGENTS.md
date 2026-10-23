## Agent skills

### Issue tracker

Issues and specs are tracked as local markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical triage roles mapped to standard labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout (`GLOSSARY.md` and `docs/adr/` at root). See `docs/agents/domain.md`.

### Knowledge graph (graphify)

Codebase, docs, SQL schemas, configs, and PDFs mapped into a queryable graph (`graphify-out/`). Query via `graphify query "<question>"`, trace paths with `graphify path "<A>" "<B>"`, or explain nodes with `graphify explain "<concept>"`. Build via `graphify .` and sync via `graphify update .`. See `docs/agents/graphify.md`.

### Design system (INK)

Monochrome editorial UI specifications, tokens (`ink-tokens.css`), component contracts, typography, responsive layout blueprints, and WCAG accessibility rules. See `docs/agents/INK_Design_System_v2.md`.
