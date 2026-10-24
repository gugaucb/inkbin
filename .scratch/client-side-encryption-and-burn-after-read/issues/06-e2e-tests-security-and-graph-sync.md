# 06 - Testes Automatizados End-to-End, Segurança e Sincronização do Grafo

Status: resolved
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

## Answer

1. Testes automatizados desenvolvidos e validados:
   - `tests/test_burn_after_read.py`:
     - Implementado teste de criação de paste com `burn_after_read=True`.
     - Implementado teste de interceptação da tela intermediária (`burn_confirmation.html`) prevenindo leituras acidentais por bots e rastreadores.
     - Implementado teste de revelação confirmada (`POST /p/{slug}/reveal` e `GET /api/pastes/{slug}?confirm_burn=true`) garantindo expurgo atômico permanente do banco e do cache.
     - Implementado teste de requisição subsequente retornando 404 Not Found.
     - Implementado teste de expiração por tempo (`test_burn_after_read_time_expiration`) verificando que um paste queimado respeita expiração anterior caso não revelado.
   - `tests/test_content_formats.py`:
     - Testes de submissão e integridade de payloads em `plaintext`, `aes-256-gcm` e `base64`.
     - Teste de validação Pydantic rejeitando formatos não suportados com HTTP 422 Unprocessable Entity.
   - `tests/test_i18n.py`:
     - Verificação completa de paridade de chaves entre `en.json`, `pt-br.json` e `cn.json` para todas as seções de segurança, criptografia, interstitial de burn e badges do visualizador.
   - `tests/test_web_ui.py`:
     - Testes de renderização dos controles de criptografia no editor e badges/interstitial no visualizador.
2. Suíte de testes:
   - Execução de `./.venv/bin/pytest`: 91 testes aprovados com 100% de sucesso.
3. Grafo de conhecimento:
   - Executado `graphify update .` com re-extração de AST em todos os arquivos alterados e sincronização de `graphify-out/graph.json`, `graphify-out/graph.html` e `graphify-out/GRAPH_REPORT.md`.
