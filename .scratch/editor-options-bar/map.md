# Map: Redesenho da Barra de Opções e Segurança do Editor

## Destination

Consolidação e redesign dos controles de expiração, formato (AES-256-GCM / Base64 em radiobuttons), destruição pós-leitura e proteção por senha em uma barra de opções (`.editor-options-bar`) posicionada diretamente abaixo do `.editor-container`, acompanhada de marcadores explicativos ciano e integração com INK Design System v2 e i18n (`en`, `pt-br`, `cn`) conforme `.scratch/editor-options-bar/spec.md`.

## Notes

- **Domínio**: Inkbin — UI Editorial, Privacidade Sem Rastreadores e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — o esforço define e implementa o template, folha de estilos, lógica cliente e testes automatizados.
- **Modelo de Domínio**: `GLOSSARY.md` (`Client-Side Encryption`, `Burn After Read`, `Base64 Encoding`, `Protected Paste`).
- **Referência Visual**: Layout com seletor `Expires in` integrado à esquerda, opções inline com checkboxes/radios com acento ciano quando ativos, e lista explicativa com marcadores de ponto ciano (`•`).
- **Skills relevantes**: `codebase-design`, `architecture-patterns`, `tdd`.

## Decisions so far

- 01: [01-i18n-catalogs-and-descriptions.md](issues/01-i18n-catalogs-and-descriptions.md) — Cadastradas chaves de tradução com 100% de paridade em `en`, `pt-br` e `cn` para opções (`Expires in`, `Password`, `Encrypt in browser`, `Burn after read`, `Base64`) e descrições detalhadas.
- 02: [02-template-markup-and-reorganization.md](issues/02-template-markup-and-reorganization.md) — Reorganizado `editor.html` com cabeçalho limpo (Título/Linguagem) e inclusão da nova barra `.editor-options-bar` diretamente abaixo do `.editor-container`.
- 03: [03-editorial-styling-and-ink-tokens.md](issues/03-editorial-styling-and-ink-tokens.md) — Aplicados estilos CSS para a barra de opções, controle de expiração, indicadores ciano `#00d4b8` e marcadores de ponto ciano com responsividade móvel.
- 04: [04-client-js-interactivity-and-state.md](issues/04-client-js-interactivity-and-state.md) — Implementada lógica cliente em `ink-editor.js` para alternância de radio/checkbox, revelação de senha, renderização das explicações ativas com ponto ciano e sincronização de formato.
- 05: [05-tests-and-knowledge-graph-sync.md](issues/05-tests-and-knowledge-graph-sync.md) — Validada suíte completa de testes com 92/92 aprovados (100%) e sincronizado grafo de conhecimento via `graphify update .`.

## Not yet specified

- **Atalhos de teclado para alternar opções**: Teclas de atalho específicas (ex: Alt+E para encrypt, Alt+B para burn) na interface de edição.
- **Seletor de expiração personalizada em minutos**: Suporte a entrada manual de minutos para expiradores efêmeros customizados.

## Out of scope

- Criptografia assimétrica PGP/GPG multi-destinatário.
- Quebra de compatibilidade da API `/api/pastes` existente.
