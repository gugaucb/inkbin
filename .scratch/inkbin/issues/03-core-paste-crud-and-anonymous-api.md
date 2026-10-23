# 03 - Implementação da API assíncrona de criação anônima e recuperação de pastes

Type: task
Status: resolved
Blocked by: 02

## Question

Como implementar os endpoints assíncronos FastAPI para criação anônima de pastes e recuperação rápida (JSON e texto puro/raw), garantindo limites estritos de tamanho, incremento seguro de visualizações e entrega do token de administração?

## Context & Requirements

- `POST /api/pastes`:
  - Entrada: `title` (opcional, máx 200 chars), `content` (obrigatório, não vazio, máx 1MB), `language` (opcional), `expiration` (enum: `1h`, `1d`, `1w`, `1m`, `never`).
  - Saída: `slug`, `url`, `admin_delete_token`, `expires_at`, `created_at`.
  - Geração segura de `admin_delete_token` retornado apenas na resposta de criação (o banco armazena apenas o hash).
- `GET /api/pastes/{slug}`:
  - Recupera metadados e conteúdo do paste.
  - Incremento atômico de `views_count`.
  - Tratamento de erro 404 para slugs inexistentes ou expirados.
- `GET /raw/{slug}`:
  - Resposta com cabeçalho `Content-Type: text/plain; charset=utf-8` retornando o conteúdo bruto sem wrappers.

## Answer

Endpoints assíncronos da API pública implementados e validados:
1. `src/inkbin/schemas.py`: `ExpirationEnum` com conversão de timedelta para timestamp UTC (`1h`, `1d`, `1w`, `1m`, `never`), `PasteCreateRequest` com validação de payload não vazio e teto de 1MB, e DTOs de resposta `PasteCreateResponse` e `PasteDetailResponse`.
2. `POST /api/pastes`: Criação anônima rápida com cálculo de expiração, geração de URL pública e retorno exclusivo do `admin_delete_token` em texto puro. Validação estrita de limites de payload (413/422).
3. `GET /api/pastes/{slug}`: Busca assíncrona com verificação de expiração, incremento atômico de `views_count` via SQL update direto e retorno detalhado de metadados.
4. `GET /raw/{slug}`: Resposta rápida `PlainTextResponse` com cabeçalho `Content-Type: text/plain; charset=utf-8` e incremento de visualização.
5. Cobertura de testes completa em `tests/test_api_pastes.py` cobrindo sucesso, 404 para inexistente/expirado, incremento de views, teto de 1MB e rota raw.
