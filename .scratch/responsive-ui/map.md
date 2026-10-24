# Map: Responsividade Multiplataforma no Inkbin

## Destination

Implementação e refinamento da responsividade multiplataforma em todas as telas e componentes do Inkbin (Editor, Visualizador, Navegação, Modais e Telas Auxiliares) segundo os breakpoints do INK Design System v2, corrigindo alturas rígidas (como #paste-content) e eliminando rolagens forçadas em dispositivos móveis e tablets conforme .scratch/responsive-ui/spec.md.

## Notes

- **Domínio**: Inkbin — UI Editorial Monocromática e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — o esforço define decisões e implementação de responsividade diretamente nos templates Jinja2 e folhas de estilo CSS.
- **Breakpoints canônicos**: Mobile `<= 639px`, Tablet `640–1023px`, Desktop `1024–1439px`, Wide `>= 1440px`.
- **Regras de Usabilidade**: Confinamento estrito de rolagem horizontal em blocos de código; alvos de toque móveis >= 44x44px; campos e botões acessíveis sem overflow horizontal global.
- **Skills relevantes**: `codebase-design`, `architecture-patterns`, `tdd`, `domain-modeling`.

## Decisions so far

- [01 - Breakpoints Globais, Tokens de Viewport e Container Base](issues/01-global-breakpoints-and-layout-container.md): padronizados tokens canônicos do INK v2, layout responsivo da topbar (56px mobile / 64px desktop), drawer retrátil com backdrop e contenção de overflow global.
- [02 - Editor Responsivo e Altura Adaptativa de Paste Content](issues/02-editor-responsive-and-adaptive-textarea.md): altura adaptativa proporcional em `.editor-textarea` com `clamp()` e `vh`, campos do formulário em coluna fluida com alvo de toque de 44px e botão de publicação visível sem rolagem forçada.
- [03 - Visualizador Responsivo e Isolamento de Rolagem de Código](issues/03-viewer-responsive-and-code-scroll-containment.md): contenção rigorosa de overflow-x com touch scrolling em `<pre><code>` preservando quebras originais, metadados com wrap flexível e condensação elegante de ações do leitor em telas móveis.

## Not yet specified

- **Modo de Escrita Sem Distrações (Zen Mode)**: Avaliar inclusão de expansão para tela cheia ocupando 100% da viewport em tablets ou desktops.
- **Pré-visualização Markdown Split-Screen**: Avaliar renderização simultânea lado a lado do código/preview em viewports ultrawide (>= 1440px).

## Out of scope

- Construção de aplicativo nativo móvel ou empacotamento PWA com Service Worker offline (o escopo é web responsiva moderna).
- Alterações em regras de negócio de banco de dados, rotas de API ou modelos de persistência.
