# 07 - Atualização da Suíte de Testes e Validação Completa de Cobertura

Status: open
Type: task
Blocked by: 05, 06

## Question

Como atualizar as asserções de UI existentes para o novo padrão de idioma inglês (`en`), introduzir testes automatizados para troca de locale (`pt-br`, `cn`) e validação da variável `EXPIRATION_OPTIONS`, garantindo 100% de sucesso e sincronização do grafo de conhecimento?

## Scope

1. Atualizar testes existentes em `tests/test_web_ui.py`:
   - Adequar asserções que esperam texto em português para os equivalentes traduzidos em inglês padrão (ex: "Publish paste", "Inkbin v0.1.0 · Open Source").
2. Criar novos testes de cobertura para i18n em `tests/test_i18n.py`:
   - Teste de resolução de locale via query param `?lang=pt-br`, cookie `inkbin_locale=cn` e fallback para `en`;
   - Teste de renderização dos templates nas três línguas (`en`, `pt-br`, `cn`);
   - Teste do endpoint de alternância `GET /set-locale/{locale}`.
3. Criar testes para configuração dinâmica de expiração em `tests/test_expiration_options.py`:
   - Teste de validação estrita do payload da API baseado em `settings.EXPIRATION_OPTIONS`;
   - Teste de rejeição HTTP 422 para prazos não habilitados;
   - Teste de fallback padrão quando a expiração é omitida.
4. Executar toda a suíte de testes do projeto via `pytest` e garantir que todos passem sem falhas ou avisos.
5. Executar `graphify update .` para manter o grafo de conhecimento sincronizado.
