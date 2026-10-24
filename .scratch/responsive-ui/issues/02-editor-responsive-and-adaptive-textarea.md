# 02 - Editor Responsivo e Altura Adaptativa de Paste Content

Status: resolved
Type: task
Blocked by: 01

## Question

Como reestruturar o formulário do editor (`src/inkbin/templates/editor.html`) e o elemento `#paste-content` (`.editor-textarea`) em `src/inkbin/static/css/ink-editorial.css` para substituir a altura fixa de 480px por uma altura adaptativa baseada em viewport no mobile, organizar os campos de título, linguagem, expiração e senha em disposição fluida e garantir visibilidade imediata do botão "Publicar Texto" sem rolagem forçada?

## Scope

1. Redefinir a regra `.editor-textarea` em `src/inkbin/static/css/ink-editorial.css`:
   - Em desktop: manter altura de trabalho confortável (`height: 480px;`).
   - Em mobile (`@media (max-width: 639px)`): altura adaptativa proporcional `height: clamp(200px, 36vh, 320px); min-height: 180px; resize: vertical;`.
   - Em tablet (`@media (min-width: 640px) and (max-width: 1023px)`): altura intermediária `height: clamp(300px, 45vh, 420px);`.
2. Otimizar a grade de campos do formulário no mobile (`editor.html`):
   - `.form-row`: permitir quebra fluida em coluna única (`flex-direction: column; width: 100%;`) em telas menores que 640px.
   - Seletores de Linguagem e Expiração ocupando 100% da largura em coluna única com altura de toque de 44px.
   - Ajustar o campo de senha para largura total sem transbordar o container.
3. Ajustar o rodapé do formulário:
   - Garantir que a linha de ação com a dica anônima e o botão de submissão `#submit-btn` se adeque a telas pequenas (quebrando em coluna ou alinhando o botão à direita com largura total se necessário).
   - Inserir suporte a `padding-bottom: env(safe-area-inset-bottom, 16px)` para dispositivos móveis com barra de navegação virtual.

## Answer

Reestruturado o formulário e a área de texto do editor:
- `.editor-textarea` atualizada para altura adaptativa: no desktop permanece com 480px; em tablets varia com `clamp(300px, 45vh, 420px)`; em mobile varia proporcionalmente com `height: clamp(200px, 36vh, 320px); min-height: 180px; resize: vertical;`.
- Em mobile (`<= 639px`), `.editor-header-fields` colapsa fluidamente em coluna única com largura de 100%, campos de texto e seletores com altura de toque de 44px e fonte de 16px para evitar auto-zoom indesejado no iOS Safari.
- A barra de contadores `.editor-toolbar` e `.editor-stats` adapta-se fluidamente em coluna/wrap.
- O rodapé `.editor-footer-actions` inverte para coluna no mobile, colocando o botão `#submit-btn` como alvo prioritário de toque total e centralizando a dica de publicação anônima.
