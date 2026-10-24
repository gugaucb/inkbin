# Issue 03: Estilização Editorial e Tokens INK

Type: task
Status: resolved
Blocked by: 02

## Answer

Implementados todos os estilos editoriais em `ink-editorial.css`: seletor compacto de expiração com label superior e chevron, toggles e radiobuttons estilizados com acento ciano vibrante (`#00d4b8`), container retrátil de senha com borda tracejada e lista dinâmica de explicações com marcadores de ponto ciano (`•`) de alto contraste, além de regras completas de responsividade mobile (grid de 2 colunas e 1 coluna em telas estreitas). 17 testes de UI aprovados (100%).

## Question

Como aplicar os estilos visuais em `ink-editorial.css` para reproduzir o design da referência (caixa compacta de expiração, checkboxes/radios com indicador ciano ativo, lista com marcadores de ponto ciano e responsividade móvel)?

## Details

- Estilos para `.editor-options-bar`:
  - Alinhamento flex com suporte a wrap.
  - Estilização do seletor de expiração compacto com borda sutil, cantos arredondados, label em fonte pequena superior e select nativo estilizado.
  - Estilização dos itens de opção (`.option-item` / `.option-label`):
    - Checkbox / Radio estilizado com cantos arredondados, borda neutra e fundo escuro.
    - Estado ativo com preenchimento ciano/teal (`#00d4b8` / `#14b8a6` / `#22d3ee`) e checkmark/ponto visível.
    - Hover e estados de foco acessíveis via teclado.
  - Estilização do campo retrátil de senha (`.password-reveal-container`).
  - Estilização de `.editor-options-explanations`:
    - Marcador com ponto ciano (`•`) de alto contraste.
    - Tipografia secundária nítida e alinhamento espaçado.
  - Responsividade para telas estreitas (`<= 899px` e `<= 639px`).
