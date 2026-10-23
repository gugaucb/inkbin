# 05 - Internacionalização do JavaScript do Cliente e Exclusão no Histórico Local

Status: open
Type: task
Blocked by: 04

## Question

Como internacionalizar todas as strings e mensagens manipuladas via JavaScript no cliente (`src/inkbin/static/js/ink-editor.js`) e adicionar a funcionalidade de exclusão individual e total de itens no "Histórico Local" mantendo acessibilidade e atualização reativa do DOM?

## Scope

1. Expor as traduções necessárias para o cliente via objeto global `window.__INK_I18N__` ou `data-` attributes injetados no `base.html`.
2. Internacionalizar mensagens em `src/inkbin/static/js/ink-editor.js`:
   - Contadores dinâmicos de caracteres e bytes ("caracteres", "máx");
   - Feedback de cópia nos botões ("Copiado!", "Código copiado!");
   - Mensagens de erro e alertas de rede.
3. Implementar a exclusão no "Histórico Local":
   - Em cada item renderizado por `renderHistoryList()`, adicionar botão de remoção individual com ícone `ti-x`, atributo `aria-label` e `title` traduzidos;
   - Ao clicar no botão de exclusão, impedir a navegação do link pai, remover o paste correspondente do array no `localStorage` e renderizar novamente a lista;
   - Adicionar botão "Limpar histórico" / "Clear history" com confirmação rápida para esvaziar todo o histórico local;
   - Exibir mensagem traduzida quando o histórico estiver vazio.
