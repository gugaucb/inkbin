# 04 - Testes Automatizados, Validação de i18n e Sincronização do Grafo

Status: open
Type: task
Blocked by: 03

## Question

Como validar automaticamente a integridade das novas chaves de internacionalização, a renderização semântica da seção de recursos nos templates HTML e a conformidade visual e técnica com a suíte de testes existente (`pytest`) e o grafo de conhecimento (`graphify update .`)?

## Scope

1. Adicionar/expandir testes em `tests/test_i18n.py` ou `tests/test_views.py` validando que:
   - A página principal (`GET /`) renderiza a seção `platform-features-section` com sucesso em todos os locales suportados (`en`, `pt-br`, `cn`).
   - Todas as chaves `features.*` existem e não produzem fallbacks quebrados.
2. Executar a suíte completa de testes (`pytest`) para garantir 100% de aprovação sem regressões.
3. Executar `graphify update .` para manter a base de conhecimento sincronizada.
