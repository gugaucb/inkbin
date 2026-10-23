# 02 - Ícones na Sidebar e Topbar de Navegação

Status: open
Type: task
Blocked by: 01

## Question

Como aplicar ícones Tabler na barra lateral canônica (AppSidebar) e na barra superior (Topbar), enriquecendo a marca, ações de criação e histórico local no navegador?

## Scope

1. Em `src/inkbin/templates/base.html`:
   - Substituir o caractere `＋` pelo ícone `<i class="ti ti-plus"></i>` no link `.nav-link` de "Novo texto".
   - Adicionar o ícone `ti-terminal` ou `ti-file-text` junto à marca `INKBIN` no cabeçalho da sidebar.
   - Adicionar `<i class="ti ti-shield-check"></i>` no rodapé da sidebar ("Sem rastreamento · Anônimo").
   - Na `.topbar`, enriquecer o botão de ação rápida "Novo texto" com `<i class="ti ti-plus"></i>`.
2. Em `src/inkbin/static/js/ink-editor.js`:
   - Na função `renderHistoryList`, incluir `<i class="ti ti-file-text"></i>` ou `<i class="ti ti-code"></i>` nos itens do histórico recente para melhor hierarquia visual.
