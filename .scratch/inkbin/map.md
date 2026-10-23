# Map: Inkbin MVP

## Destination

Entrega da plataforma open-source Inkbin (Fase 1 - MVP): serviço de alto desempenho para publicação anônima de textos/códigos, geração de slugs Base62 ofuscados, visualização com syntax highlighting e modo raw, interface editorial monocromática (INK Design System v2) e infraestrutura containerizada com Docker Compose (FastAPI, PostgreSQL e Redis).

## Notes

- **Domínio**: Inkbin — plataforma open-source de publicação anônima e segura de código e textos (`GLOSSARY.md`).
- **Modo de execução**: *Execution carried into the map* — este esforço mapeia as decisões de arquitetura e governa os tickets de implementação direta.
- **Design System**: INK Design System v2 (`docs/agents/INK_Design_System_v2.md`) — direção editorial monocromática, tipografia Inter/JetBrains Mono, sem cores de destaque cromáticas, foco em WCAG 2.1 AA.
- **Stack Tecnológica**:
  - Backend: Python 3.11+, FastAPI, Uvicorn, Pydantic v2
  - Persistência: PostgreSQL com `asyncpg` e SQLAlchemy 2.0 (fallback SQLite para testes locais)
  - Cache & Concorrência: Redis assíncrono (`redis-py`) com fallback in-memory
  - Interface: Server-rendered Jinja2 + Vanilla CSS (`ink-tokens.css`) + Prism/Highlight.js
  - Infraestrutura: Dockerfile multi-stage e `docker-compose.yml`
- **Skills relevantes**: `architecture-patterns`, `codebase-design`, `tdd`, `domain-modeling`.

## Decisions so far

- **[01 - Estruturação do repositório open-source](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/.scratch/inkbin/issues/01-scaffold-and-docker.md)**: Estabelecido layout padrão `src/inkbin/`, `pyproject.toml` com dependências assíncronas e dev tools, `Dockerfile` multi-stage e `docker-compose.yml` para FastAPI + Postgres + Redis. Endpoint `/health` e suíte pytest operacional.
- **[02 - Modelagem de dados e slugs Base62](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/.scratch/inkbin/issues/02-database-schema-and-base62-slug.md)**: Entidade `Paste` em SQLAlchemy 2.0 com expiração e visualizações, gerador criptográfico Base62 (7 chars), `Admin Delete Token` com hash SHA-256 e serviço com retry automático para colisões de slug.

## Not yet specified

- **Fase 2 — Proteção e Validação por Senha (RF004, RF005)**: Hash de senhas via Argon2/bcrypt, tela de bloqueio com validação de senha, rate limiting de tentativas (5 tentativas com bloqueio temporário de 15min) e sessão temporária por cookie (24h).
- **Fase 3 — Gerenciamento e Ciclo de Vida (RF006, RF007)**: Endpoint e interface de exclusão antecipada autenticada via `Admin Delete Token`, e worker/cron assíncrono para expurgo automático de pastes expirados (1h, 1d, 1w, 1m).
- **Moderação e Detecção de Abuso (RN006)**: Fluxo de denúncia de conteúdo inapropriado, hashing de conteúdo para identificação de duplicatas/spam e interface administrativa simplificada.

## Out of scope

- Autenticação obrigatória ou sistema complexo de contas para publicação (a criação é anônima por princípio).
- Edição de conteúdo de pastes após publicação (pastes são estritamente imutáveis conforme RN002).
- Armazenamento em S3 ou storage de objetos para a Fase 1 (conteúdos de até 1MB são armazenados em PostgreSQL TOAST com compressão).
