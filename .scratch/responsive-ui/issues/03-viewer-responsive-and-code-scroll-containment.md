# 03 - Visualizador Responsivo e Isolamento de Rolagem de Código

Status: open
Type: task
Blocked by: 01

## Question

Como configurar o visualizador de código (`src/inkbin/templates/viewer.html`) e seus estilos em `src/inkbin/static/css/ink-editorial.css` para conter estritamente a rolagem horizontal no bloco `<pre><code>` (sem transbordar a viewport global), condensar a barra de ações e metadados de forma fluida em telas mobile e tablet?

## Scope

1. Confinamento da rolagem horizontal em `src/inkbin/static/css/ink-editorial.css`:
   - Assegurar que `.code-viewer`, `pre` e `code` possuam `max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; word-break: normal; white-space: pre;`.
   - Garantir que tabelas de numeração de linhas ou blocos monolíticos de texto não empurrem a largura da tela.
2. Ações do visualizador (`.viewer-actions`):
   - Em telas móveis (`<= 639px`), condensar botões secundários exibindo ícone + `aria-label`/`title` acessíveis ou organizá-los em barra com quebra flexível natural (`flex-wrap: wrap; gap: var(--space-2);`).
   - Manter botões críticos (Copiar Código, Novo, Excluir) destacados com alvos de toque adequados.
3. Linha de metadados:
   - Tornar o cabeçalho de título e badges de metadados (linguagem, data, expiração, visualizações) responsivo com wrap flexível sem estourar o container.
