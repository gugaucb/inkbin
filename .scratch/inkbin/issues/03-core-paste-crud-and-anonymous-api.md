# 03 - Implementação da API assíncrona de criação anônima e recuperação de pastes

Type: task
Status: open
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
