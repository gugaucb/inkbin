# 01 - Modelo de Domínio, Esquema de Banco de Dados e Migração

Status: open
Type: task
Blocked by: none

## Question

Como atualizar o modelo relacional `Paste` (`src/inkbin/models.py`), a migração de esquema incremental (`src/inkbin/db.py`) e os contratos de entrada/saída da API (`src/inkbin/schemas.py`) para suportar os campos `content_format` (`plaintext`, `aes-256-gcm`, `base64`) e `burn_after_read` (`bool`) mantendo total compatibilidade retroativa com os registros existentes?

## Scope

1. Atualizar o modelo `Paste` em `src/inkbin/models.py`:
   - `content_format`: `Mapped[str] = mapped_column(String(20), default="plaintext", nullable=False)`
   - `burn_after_read`: `Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)`
2. Adicionar migração automática incremental em `_sync_migrate_schema` (`src/inkbin/db.py`):
   - Verificar `content_format` nas colunas existentes; se ausente, adicionar com valor padrão `'plaintext'`.
   - Verificar `burn_after_read` nas colunas existentes; se ausente, adicionar com valor padrão `FALSE` (`0` no SQLite).
3. Atualizar esquemas Pydantic em `src/inkbin/schemas.py`:
   - `PasteCreateRequest`: campos `content_format: str = "plaintext"` (com validação para aceitar apenas `plaintext`, `aes-256-gcm`, `base64`) e `burn_after_read: bool = False`.
   - `PasteCreateResponse`: expor `content_format` e `burn_after_read`.
   - `PasteDetailResponse`: expor `content_format` e `burn_after_read`.
4. Atualizar serviço de persistência em `src/inkbin/services.py` para repassar os novos campos na criação do paste.
5. Escrever testes unitários em `tests/test_models.py` e `tests/test_schemas.py` cobrindo a validação e persistência dos novos campos.
