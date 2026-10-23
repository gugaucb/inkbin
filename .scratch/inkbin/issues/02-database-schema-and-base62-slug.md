# 02 - Modelagem de dados e algoritmo de geração de slugs Base62 com mitigação de colisão

Type: prototype
Status: resolved
Blocked by: 01

## Question

Como modelar a entidade `Paste` no banco de dados (conteúdo até 1MB, título opcional de até 200 chars, linguagem de sintaxe, expiração, contador de visualizações e hash do token de administração) e implementar a geração criptográfica de slugs aleatórios em Base62 (6-8 caracteres) com garantia de unicidade e retry automático?

## Context & Requirements

- Tabela `pastes` com colunas:
  - `id`: UUID ou BigInt interno.
  - `slug`: String(8) indexada e única (`UNIQUE INDEX`).
  - `title`: String(200), opcional.
  - `content`: Text (até 1MB) com validação de payload.
  - `language`: String(50), padrão `plaintext`.
  - `admin_delete_hash`: String com hash seguro do `Admin Delete Token` para autorização de deleção sem login.
  - `views_count`: Integer, padrão 0.
  - `expires_at`: Timestamp com fuso horário (nulo se nunca expirar).
  - `created_at`: Timestamp com fuso horário.
- Gerador de slug em Base62:
  - Alfabeto `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`.
  - Geração via `secrets.choice` com comprimento configurável (padrão 7 caracteres).
  - Loop de retry em caso de colisão de integridade única (limite de 3 tentativas).

## Answer

Implementação de modelagem relacional assíncrona e gerador Base62 concluída:
1. `src/inkbin/models.py`: Entidade `Paste` mapeada via SQLAlchemy 2.0 `DeclarativeBase` e `Mapped`, com colunas `id`, `slug` (`String(8)`, indexada e única), `title` (opcional até 200 chars), `content` (`Text`), `language`, `admin_delete_hash` (`String(128)`), `views_count` (padrão 0), `expires_at` (timezone aware) e `created_at`. Método auxiliar `is_expired()` para verificação imediata de TTL.
2. `src/inkbin/slug.py`: Gerador `generate_slug()` utilizando o alfabeto Base62 canônico e `secrets.choice` criptograficamente seguro.
3. `src/inkbin/security.py`: Funções para emissão de `Admin Delete Token` (`secrets.token_urlsafe(32)`), hashing via SHA-256 e validação com `hmac.compare_digest`.
4. `src/inkbin/services.py`: Serviço transacional `create_paste_record()` com isolamento por savepoints (`begin_nested`) e retry automático de até 3 tentativas em caso de colisão de slug (`SlugCollisionError`).
5. Suíte de testes em `tests/test_slug_and_security.py`, `tests/test_models.py` e `tests/test_services.py` 100% verde.
