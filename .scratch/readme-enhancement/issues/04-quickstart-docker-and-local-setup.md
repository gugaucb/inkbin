# 04: Guias de Execução Rápida, Docker e Configuração de Ambiente

**What to build:** Disponibilizar no README.md um guia de início rápido e autohospedagem à prova de falhas para desenvolvedores e operadores, cobrindo a execução instantânea via Docker Compose, a inicialização local em ambiente virtual com fallback SQLite (zero-config) e a tabela de referência de variáveis de ambiente do `.env.example`.

**Blocked by:** 02: Cabeçalho Editorial, Badges de Status e Galeria Visual

**Status:** resolved

- [x] Detalhar o fluxo de execução via Docker Compose (`docker compose up --build`), incluindo mapeamento de portas e teste de integridade com healthcheck (`/health`).
- [x] Detalhar o fluxo de desenvolvimento local em ambiente virtual Python (passo a passo com `venv`, `pip install -e ".[dev]"` e inicialização com `uvicorn src.inkbin.main:app --reload`).
- [x] Explicar o mecanismo de fallback automático: uso transparente de SQLite (`aiosqlite`) e cache em memória quando PostgreSQL ou Redis não estiverem configurados.
- [x] Criar tabela descritiva completa com todas as variáveis de ambiente suportadas (`DATABASE_URL`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`, `MAX_PASTE_BYTES`, `APP_ENV`, `SECRET_KEY`, `BASE_URL`).

## Answer

Adicionadas ao `README.md`:
1. Subseção "Opção 1: Docker Compose" contendo comandos de inicialização em cluster, verificação de integridade via `/health` e acompanhamento de logs.
2. Subseção "Opção 2: Desenvolvimento Local (Zero-Config com SQLite)" explicando a ativação de ambiente virtual e execução com hot-reload.
3. Documentação do fallback automático transparente para SQLite e cache/rate limiting em memória caso PostgreSQL ou Redis não estejam disponíveis.
4. Tabela detalhada de todas as variáveis de ambiente com tipo, valores padrão e descrições técnicas.

