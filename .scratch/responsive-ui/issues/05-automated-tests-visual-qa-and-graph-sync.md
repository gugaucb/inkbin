# 05 - Testes Automatizados, QA de Responsividade e Sincronização do Grafo

Status: open
Type: task
Blocked by: 02, 03, 04

## Question

Como validar a estabilidade de toda a suíte de testes automatizados (`pytest`), verificar a ausência de regressões no HTML/CSS e sincronizar o grafo de conhecimento da base via `graphify update .`?

## Scope

1. Executar a suíte de testes com `pytest tests/` e certificar que todos os testes passem com 100% de sucesso.
2. Criar ou atualizar testes em `tests/test_web_ui.py` para validar a presença de classes responsivas, metatags viewport e integridade dos templates.
3. Verificar conformidade com WCAG 2.2 AA (alvos de clique de pelo menos 40px–44px em mobile e contraste mínimo).
4. Sincronizar o grafo de conhecimento executando `graphify update .` para atualizar a documentação arquitetural.
