# Map: Tabler Icons UI no Inkbin

## Destination

Modernização e refinamento visual de toda a interface do Inkbin (Editor, Visualizador, Sidebar, Navegação, Modais e Telas de Status) através da incorporação da biblioteca Tabler Icons (@tabler/icons-webfont), com enriquecimento iconográfico em botões, campos e metadados, e substituição criteriosa de texto por ícones acessíveis (WCAG 2.1 AA) em botões secundários conforme especificado em .scratch/tabler-icons-ui/spec.md.

## Notes

- **Domínio**: Inkbin — UI Editorial Monocromática e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — este esforço governa as decisões e a implementação direta dos tickets no código fonte e templates Jinja2.
- **Biblioteca de Ícones**: [Tabler Icons](https://github.com/tabler/tabler-icons) (`@tabler/icons-webfont@3.29.0` via jsDelivr).
- **Design System & Estilo**: INK Design System v2 — ícones herdando `currentColor`, sem cores cromáticas, traço padrão de 2px, dimensões padronizadas via tokens (`--icon-size-sm`, `--icon-size-md`, `--icon-size-lg`).
- **Acessibilidade**: WCAG 2.1 AA obrigatório em qualquer botão exclusivamente iconográfico (`aria-label`, `title`, alvos de toque >= 36-40px e foco visível).
- **Skills relevantes**: `codebase-design`, `architecture-patterns`, `tdd`, `domain-modeling`.

## Decisions so far

- **01 Tabler Icons CDN e Tokens Canônicos INK**: Carregamento de `@tabler/icons-webfont@3.29.0` via jsDelivr em `base.html`, registro de `--icon-size-*` em `ink-tokens.css` e reset/regras de herança em `ink-editorial.css`. ([01-tabler-icons-cdn-and-ink-tokens.md](issues/01-tabler-icons-cdn-and-ink-tokens.md))
- **02 Ícones na Sidebar e Topbar de Navegação**: Adição de `ti-terminal` na marca, `ti-plus` nas ações da sidebar e topbar, `ti-shield-check` no rodapé e `ti-file-text` na listagem de histórico recente. ([02-sidebar-and-topbar-icons.md](issues/02-sidebar-and-topbar-icons.md))
- **03 Ícones em Labels e Ações do Formulário de Criação**: Inclusão de `ti-heading`, `ti-code`, `ti-clock` e `ti-lock` nos labels, `ti-letter-case` e `ti-database` nos contadores e `ti-upload`/`ti-loader` no botão principal. ([03-editor-form-labels-and-actions.md](issues/03-editor-form-labels-and-actions.md))
- **04 Ícones em Ações e Metadados do Visualizador**: Inclusão de `ti-code`, `ti-calendar`, `ti-eye` e `ti-hourglass` nos metadados, e `ti-copy`/`ti-check`, `ti-file-code`, `ti-plus`, `ti-trash` e `ti-flag` nas ações com acessibilidade e recolhimento responsivo. ([04-viewer-actions-and-metadata.md](issues/04-viewer-actions-and-metadata.md))

## Not yet specified

- **Pacote de SVGs locais embutidos (Offline/Air-gapped)**: Caso seja requerido rodar a plataforma completamente isolada de redes externas sem CDN, migrar o webfont para arquivos locais servidos diretamente por `src/inkbin/static/`.
- **Componente customizado de Tooltip Flutuante**: Avaliar se botões com apenas ícone necessitam de balão de dica estilizado via CSS caso o atributo `title` nativo do navegador não ofereça a estética desejada.

## Out of scope

- Cores cromáticas (vermelho, azul, verde) nos ícones (a identidade é estritamente monocromática baseada no INK Design System).
- Conjuntos de ícones externos não compatíveis com a grade e estética do Tabler Icons.
- Alterações em regras de negócio de persistência ou endpoints da API REST (este esforço é focado na camada gráfica e de experiência de usuário).
