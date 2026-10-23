# 01 - Estruturação do repositório open-source com Docker Compose e pyproject.toml

Type: task
Status: open
Blocked by: none

## Question

Como estruturar os arquivos canônicos de projeto open-source (`pyproject.toml`, `src/inkbin/`, `Dockerfile`, `docker-compose.yml`, scripts de inicialização e variáveis `.env.example`) integrando FastAPI, PostgreSQL e Redis com ambiente de desenvolvimento e produção reprodutíveis?

## Context & Requirements

- Estrutura de diretórios `src/` layout padrão Python (`src/inkbin/`).
- `pyproject.toml` com dependências de produção (`fastapi`, `uvicorn`, `sqlalchemy[asyncio]`, `asyncpg`, `redis`, `jinja2`, `pydantic-settings`, etc.) e dev/testes (`pytest`, `pytest-asyncio`, `httpx`, `ruff`).
- `Dockerfile` eficiente em múltiplos estágios para Python 3.11+.
- `docker-compose.yml` orquestrando três serviços:
  1. `app`: aplicação FastAPI (hot-reload no dev montando volume local).
  2. `db`: PostgreSQL 16 (com healthcheck).
  3. `redis`: Redis 7 (com healthcheck).
- `.env.example` documentando as variáveis de ambiente necessárias.
