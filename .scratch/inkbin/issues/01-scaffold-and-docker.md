# 01 - Estruturação do repositório open-source com Docker Compose e pyproject.toml

Type: task
Status: resolved
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

## Answer

Estrutura inicial canônica estabelecida com sucesso:
1. `pyproject.toml`: Configurado com layout `src/` (`src/inkbin`), dependências assíncronas modernas (`fastapi`, `uvicorn`, `sqlalchemy>=2.0`, `asyncpg`, `aiosqlite`, `redis`, `jinja2`, `pydantic-settings`), e ferramentas de qualidade (`pytest`, `pytest-asyncio`, `httpx`, `ruff`).
2. `Dockerfile`: Implementação multi-stage build (estágio builder com compilação e estágio runner minimalista sobre Python 3.11-slim, com usuário sem privilégios `inkbin` e healthcheck HTTP).
3. `docker-compose.yml`: Orquestração completa dos serviços `app` (porta 8000), `db` (Postgres 16 Alpine com healthcheck via `pg_isready`) e `redis` (Redis 7 Alpine com healthcheck via `redis-cli ping`).
4. `.env.example`: Variáveis padronizadas para banco, cache, rate limit e portas.
5. Código e testes: Módulo `inkbin.config` com `pydantic-settings`, `inkbin.main` com endpoint `/health`, e suíte de testes inicial em `tests/test_health.py` executando com 100% de sucesso.
