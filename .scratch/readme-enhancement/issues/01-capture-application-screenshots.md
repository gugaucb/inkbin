# 01: Captura e Curadoria de Screenshots da Aplicação

**What to build:** Capturar e organizar screenshots em alta definição e de estética editorial escura da interface do Inkbin em funcionamento (Editor View, Viewer View, Desafio de Senha e Modal de Confirmação/Exclusão com Admin Delete Token), salvando os arquivos no repositório em `docs/assets/screenshots/` para exibição na documentação e no README.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Criar o diretório `docs/assets/screenshots/` no repositório.
- [x] Obter screenshots nítidos e representativos da interface atual com Tabler Icons e INK Design System:
  - `editor-view.png`: Formulário principal com campos de título, linguagem, expiração, senha e contadores em tempo real.
  - `viewer-view.png`: Visualizador de código com cabeçalho, numeração de linhas, badge de expiração e botões de ação.
  - `password-challenge.png`: Tela de desafio de senha para pastes protegidos.
  - `admin-delete-modal.png`: Modal de sucesso pós-criação exibindo o link público e o Admin Delete Token, ou tela de exclusão.
- [x] Otimizar o tamanho e peso das imagens para não onerar o clone do repositório mantendo alta legibilidade.

## Answer

Todas as 4 capturas de tela foram geradas via Playwright em alta definição com device scale 1.5x e tema editorial INK v2:
- `docs/assets/screenshots/editor-view.png` (135KB): Formulário completo com destaque tipográfico, contadores em tempo real e campos de proteção.
- `docs/assets/screenshots/viewer-view.png` (132KB): Visualizador de código com cabeçalho de metadados, botões de ação e visualização de código.
- `docs/assets/screenshots/password-challenge.png` (85KB): Tela de desafio de senha para pastes protegidos com Argon2id.
- `docs/assets/screenshots/admin-delete-modal.png` (146KB): Modal pós-criação contendo URL pública e Admin Delete Token com botões de cópia rápida.

