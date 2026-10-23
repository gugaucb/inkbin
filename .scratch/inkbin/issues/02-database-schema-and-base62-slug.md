# 02 - Modelagem de dados e algoritmo de geração de slugs Base62 com mitigação de colisão

Type: prototype
Status: open
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
