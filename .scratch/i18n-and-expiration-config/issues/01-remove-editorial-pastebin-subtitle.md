# 01 - Remoção do Subtítulo 'Editorial Pastebin' e Ajuste do Cabeçalho da Sidebar

Status: closed
Type: task
Blocked by: none

## Question

Como remover a frase "Editorial Pastebin" do cabeçalho da sidebar em `src/inkbin/templates/base.html` mantendo a hierarquia visual, alinhamento e proporções monocromáticas do INK Design System v2?

## Scope

1. Localizar o bloco `.sidebar-header` em `src/inkbin/templates/base.html`.
2. Remover o elemento `<div class="brand-subtitle">Editorial Pastebin</div>`.
3. Garantir que a âncora de marca `.brand-title` preserve seu espaçamento adequado, ícone `ti-terminal` e o texto `INKBIN`.
4. Verificar se nenhuma regra de CSS ou layout quebre com a remoção.
