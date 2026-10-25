# 04: Verificação E2E, Validação de Configuração e Atualização do Knowledge Graph

**What to build:**
Executar a validação sintática das configurações do Caddy e Docker Compose, testar o comportamento de cabeçalhos de proxy reverso (`X-Forwarded-Proto` e `Host`), assegurar que a suíte de testes unitários e de integração continue passando integralmente e atualizar o grafo de conhecimento com `graphify update .`.

**Blocked by:** 03: Variáveis de Ambiente e Documentação para Portainer e Produção

**Status:** closed

- [x] `docker compose config` e `docker compose --profile production config` validados com sucesso.
- [x] Validação sintática do `Caddyfile` confirmada.
- [x] Teste unitário e de integração em `tests/test_api_pastes.py` validando o comportamento de URLs com esquemas seguros (`https`) e headers de proxy.
- [x] Suíte completa do `pytest` 100% aprovada.
- [x] Execução de `graphify update .` para sincronizar o grafo de conhecimento.
