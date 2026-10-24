# 03 - Estilos Responsivos e Otimização para Telas Menores

Status: open
Type: task
Blocked by: 02

## Question

Como implementar os estilos CSS da vitrine em `src/inkbin/static/css/ink-editorial.css` segundo os tokens do INK Design System v2, priorizando de forma contundente a ergonomia visual e de toque em telas menores (`<= 639px`) e tablets (`640–1023px`), eliminando qualquer risco de transbordamento horizontal ou poluição visual?

## Scope

1. Adicionar classes em `src/inkbin/static/css/ink-editorial.css`:
   - `.platform-features-section`: espaçamento superior suave (`margin-top: var(--space-8)`), separador sutil com `border-top: 1px solid var(--border-default)`.
   - `.platform-features-header`: título discreto com texto muted e tipografia condensada.
   - `.platform-features-grid`: layout grid flexível e adaptativo.
   - `.feature-card`: card monocromático com borda suave (`1px solid var(--border-default)`), padding compacto, fundo neutro (`var(--bg-surface)`).
2. Otimização explícita para Telas Menores (Mobile `<= 639px`):
   - Grid em 1 ou 2 colunas compactas (`grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))` ou `1fr` no mobile estreito).
   - Altura contida e padding interno econômico (`--space-3`), permitindo escaneamento ágil.
   - Alvos mínimos de toque seguros e ausência de overflow horizontal (`max-width: 100%`).
3. Layout para Tablets e Desktops:
   - Tablet (`640px–1023px`): 2 a 3 colunas fluidas.
   - Desktop (`>= 1024px`): 4 colunas equilibradas com hover sutil monocromático (`border-color: var(--border-focus)`).
