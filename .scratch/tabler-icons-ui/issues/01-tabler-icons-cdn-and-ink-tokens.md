# 01 - Tabler Icons CDN e Tokens Canônicos INK

Status: resolved
Type: task
Blocked by: none

## Question

Como estruturar o carregamento do Tabler Icons (@tabler/icons-webfont@3.29.0) e definir tokens canônicos no INK Design System (ink-tokens.css e ink-editorial.css) garantindo proporção, traço consistente de 2px e herança de cor monocromática sem quebrar o layout?

## Scope

1. Adicionar a tag `<link>` com `@tabler/icons-webfont@3.29.0` via jsDelivr no cabeçalho de `src/inkbin/templates/base.html`.
2. Registrar tokens canônicos em `src/inkbin/static/css/ink-tokens.css`:
   - `--icon-size-sm: 16px;`
   - `--icon-size-md: 18px;`
   - `--icon-size-lg: 20px;`
   - `--icon-stroke: 2px;`
3. Ajustar `src/inkbin/static/css/ink-editorial.css` com classes e regras para elementos `i.ti` e `[class*="ti-"]`, garantindo alinhamento vertical flex, tamanho padrão `--icon-size-md`, `stroke-width: var(--icon-stroke)` e herança `currentColor`.

## Answer

Implementada a infraestrutura base do Tabler Icons:
- Tag `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.29.0/dist/tabler-icons.min.css">` inserida em `src/inkbin/templates/base.html`.
- Tokens canônicos `--icon-size-sm: 16px;`, `--icon-size-md: 18px;`, `--icon-size-lg: 20px;` e `--icon-stroke: 2px;` registrados em `src/inkbin/static/css/ink-tokens.css`.
- Regras de reset, herança `currentColor`, alinhamento vertical flex e animação `@keyframes spin` adicionadas a `src/inkbin/static/css/ink-editorial.css`.
- Testes automatizados adicionados e validados em `tests/test_web_ui.py`.

