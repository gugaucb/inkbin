# 02 - Workflow de CI para Testes e Linting

Status: open
Type: task
Blocked by: none

## Question

Como estruturar o workflow de CI do GitHub Actions (`.github/workflows/ci.yml`) para executar linters (`ruff check .`) e a suíte completa de testes automatizados (`pytest`) em cada push e pull request direcionados à branch `main` antes de qualquer publicação?

## Scope

1. Criar `.github/workflows/ci.yml` disparado em `push` e `pull_request` para a branch `main`.
2. Configurar ambiente com `actions/checkout@v4` e `actions/setup-python@v5` com Python 3.11 e cache do `pip`.
3. Instalar dependências completas do projeto incluindo extras de desenvolvimento (`pip install .[dev]`).
4. Executar verificação estática com Ruff: `ruff check .` e `ruff format --check .`.
5. Executar suíte de testes com Pytest: `pytest tests/ -v`.
