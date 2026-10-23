# 06 - Histórico local de pastes anônimos via localStorage e suíte de testes E2E

Type: task
Status: open
Blocked by: 04, 05

## Question

Como implementar o histórico local de pastes criados pelo navegador (RF003) no frontend via localStorage/cookies e estruturar a suíte completa de testes de integração assíncronos com pytest e httpx?

## Context & Requirements

- RF003 - Histórico local de pastes:
  - Ao criar um paste com sucesso no frontend, salvar localmente no `localStorage` do navegador um registro com `{ slug, title, created_at, language, admin_delete_token }`.
  - Exibir a lista na barra lateral (`AppSidebar`) ou em aba "Meus Pastes Recentes" com ação rápida para abrir ou copiar.
- Cobertura de testes automatizados com `pytest` e `pytest-asyncio`:
  - Testes unitários para o gerador Base62 e mitigação de colisão.
  - Testes de integração para os endpoints da API (`POST /api/pastes`, `GET /api/pastes/{slug}`, `GET /raw/{slug}`).
  - Teste de limite de tamanho de payload (>1MB rejeitado com 413/422).
  - Teste de rate limit (requisições excedentes retornam 429).
  - Testes de renderização HTML das páginas principais e conformidade visual básica.
