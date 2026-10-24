# 01 - Breakpoints Globais, Tokens de Viewport e Container Base

Status: resolved
Type: task
Blocked by: none

## Question

Como unificar os breakpoints responsivos do INK Design System v2 (`mobile: <= 639px`, `tablet: 640–1023px`, `desktop: 1024–1439px`, `wide: >= 1440px`) e estruturar o container base (`base.html`, `ink-tokens.css`, `ink-editorial.css`) com padding fluido e proteção contra overflow horizontal global?

## Scope

1. Revisar e padronizar breakpoints e variáveis em `src/inkbin/static/css/ink-tokens.css` e `src/inkbin/static/css/ink-editorial.css`.
2. Ajustar `.page-container` e `.app-main` para variarem espaçamentos conforme a viewport:
   - Mobile (`<= 639px`): `padding: var(--space-4);`
   - Tablet (`640px–1023px`): `padding: var(--space-6);`
   - Desktop (`>= 1024px`): `padding: var(--space-8);`
3. Ajustar a barra de topo (`.top-bar` ou cabeçalho móvel) para 56px no mobile e 64px no desktop, garantindo alinhamento do botão da gaveta (`.mobile-nav-toggle`) e marca.
4. Adicionar regras globais para conter estouro de tela (`overflow-x: hidden` no body e `max-width: 100%` nos wrappers principais).

## Answer

Padronizados os breakpoints canônicos do INK Design System v2 em `ink-tokens.css` (`--breakpoint-mobile: 639px`, `--breakpoint-tablet: 1023px`, `--breakpoint-desktop: 1439px`, `--topbar-height-desktop: 64px`, `--topbar-height-mobile: 56px`, `--container-max-width: 1120px`, `--touch-target-min: 44px`).
No `ink-editorial.css`:
- `html, body` e `.main-wrapper` configurados com `overflow-x: hidden` e suporte a `padding-bottom: env(safe-area-inset-bottom, 0px)`.
- `.topbar` adaptativo com 56px de altura em mobile (`<= 639px`) e 64px em tablet/desktop, contendo o botão de gatilho do drawer `#mobile-nav-toggle` com tamanho de toque de 40px/44px.
- `.page-container` estruturado com padding responsivo de 16px no mobile, 24px no tablet, 32px no desktop e 40px lateral no wide (>= 1440px).
- Drawer retrátil `.app-sidebar` com backdrop `#sidebar-backdrop`, acessibilidade com `aria-expanded`, suporte a fechamento com Escape, clique no backdrop e botão `#sidebar-close-btn`.
