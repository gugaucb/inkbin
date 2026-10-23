# Inkbin

Plataforma open-source de alto desempenho e segura para publicação e compartilhamento anônimo de textos e trechos de código com URLs curtas e ofuscadas, seguindo o design system editorial INK.

## Requisitos

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16
- Redis 7

## Inicialização Rápida com Docker

```bash
cp .env.example .env
docker compose up --build
```

Acesse `http://localhost:8000`.

## Desenvolvimento Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
