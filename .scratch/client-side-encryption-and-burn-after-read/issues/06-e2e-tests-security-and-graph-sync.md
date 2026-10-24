# 06 - Testes Automatizados End-to-End, Segurança e Sincronização do Grafo

Status: open
Type: task
Blocked by: 05

## Question

Como validar a suíte de testes ponta a ponta (API, banco de dados, ciclo de vida de Burn after read, formatos de conteúdo, internacionalização) garantindo 100% de aprovação e sincronizar o grafo de conhecimento (`graphify-out/`)?

## Scope

1. Desenvolver testes automatizados completos:
   - `tests/test_burn_after_read.py`:
     - Teste de criação com `burn_after_read=True`.
     - Teste de interceptação da tela intermediária (`GET /p/<slug>` sem confirmação retorna status 200 com HTML do `burn_confirmation.html`).
     - Teste de revelação confirmada (`POST /p/<slug>/reveal` retorna o conteúdo e expurga o registro do banco).
     - Teste de requisição subsequente retornando 404 Not Found imediatamente.
     - Teste de expiração por tempo vs. expurgo antecipado por leitura.
   - `tests/test_content_formats.py`:
     - Teste de submissão de `aes-256-gcm` e `base64` via API.
     - Validação de integridade do payload e esquemas Pydantic.
     - Rejeição de formatos não suportados com HTTP 422.
   - `tests/test_i18n.py`:
     - Validação de que todas as novas chaves de tradução estão presentes em `en.json`, `pt-br.json` e `cn.json`.
2. Executar suíte completa do pytest (`pytest`) garantindo que nenhum teste de regressão seja quebrado.
3. Executar `graphify update .` para sincronizar o grafo de conhecimento com as novas rotas, esquemas, migrações e documentação.
