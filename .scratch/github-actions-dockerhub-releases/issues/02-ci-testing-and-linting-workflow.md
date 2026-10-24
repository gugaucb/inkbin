# 02 - Workflow de CI para Testes e Linting

Status: resolved
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

## Answer

Criado o workflow de integração contínua `.github/workflows/ci.yml` configurado para ser disparado em eventos de `push` e `pull_request` visando a branch `main`. O job `test-and-lint` executa em runner `ubuntu-latest`, provisiona Python 3.11 com cache de dependências `pip`, instala o pacote completo com extras de desenvolvimento via `pip install .[dev]`, e valida a qualidade do código com `ruff check .`, `ruff format --check .` e `pytest tests/ -v` (92 testes passando com 100% de cobertura funcional). As pequenas discrepâncias de formatação e imports não utilizados foram corrigidas e validadas localmente.
