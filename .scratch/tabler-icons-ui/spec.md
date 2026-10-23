# Spec: Tabler Icons na Interface Gráfica do Inkbin

## 1. Visão Geral
Incorporação da biblioteca de ícones [Tabler Icons](https://github.com/tabler/tabler-icons) (`@tabler/icons-webfont`) em todas as páginas, componentes, formulários e modais da aplicação editorial Inkbin.

A iniciativa atende à diretriz do usuário de incluir ícones nos botões e, quando aplicável, nos labels de campos ou substituir rótulos de texto por ícones em botões utilitários secundários, mantendo conformidade estrita com o **INK Design System v2** (direção puramente monocromática, espessura de traço de 1.75px–2px, sem cores cromáticas e acessibilidade WCAG 2.1 AA).

## 2. Requisitos Funcionais e Visuais

### 2.1 Entrega e Tipografia de Ícones (RF01)
- Carregamento de `@tabler/icons-webfont@3.29.0` via CDN jsDelivr em `base.html`.
- Registro de tokens canônicos em `ink-tokens.css`:
  - `--icon-size-sm: 16px;` (badges e metadados densos)
  - `--icon-size-md: 18px;` (botões e campos de formulário)
  - `--icon-size-lg: 20px;` (ações de topo e títulos)
  - `--icon-stroke: 2px;` (espessura de contorno canônica)
- Estilização em `ink-editorial.css` garantindo herança de cor (`color: currentColor`), alinhamento vertical flex e sem desconfigurar alvos de clique (mínimo 36px–40px).

### 2.2 Navegação e Topbar (RF02)
- Header da Sidebar: ícone editorial representativo (`ti-terminal` ou `ti-file-text`) junto à marca `INKBIN`.
- Seção Ações da Sidebar: substituir o caractere bruto `＋` por `<i class="ti ti-plus"></i>` no link "Novo texto".
- Histórico Local da Sidebar: incluir `<i class="ti ti-clock"></i>` ou `<i class="ti ti-file-code"></i>` nos itens recentes renderizados dinamicamente pelo `ink-editor.js`.
- Rodapé da Sidebar: incluir `<i class="ti ti-shield-check"></i>` junto ao aviso "Sem rastreamento · Anônimo".
- Topbar: botão "Novo texto" com `<i class="ti ti-plus"></i>`.

### 2.3 Formulário de Criação (RF03)
- Labels com ícones identificadores:
  - Título do texto: `<i class="ti ti-heading"></i>`
  - Linguagem / Sintaxe: `<i class="ti ti-code"></i>`
  - Prazo de expiração: `<i class="ti ti-clock"></i>`
  - Senha de proteção: `<i class="ti ti-lock"></i>`
- Barra de estatísticas do editor:
  - Contador de caracteres: `<i class="ti ti-letter-case"></i>`
  - Contador de bytes: `<i class="ti ti-database"></i>`
- Botão de submissão:
  - `<button type="submit" id="submit-btn" class="btn btn-primary"><i class="ti ti-upload"></i> Publicar texto</button>`

### 2.4 Leitor de Texto / Viewer (RF04)
- Metadados:
  - Badge de linguagem: `<i class="ti ti-code"></i>`
  - Data de publicação: `<i class="ti ti-calendar"></i>`
  - Contador de visualizações: `<i class="ti ti-eye"></i>`
  - Expiração: `<i class="ti ti-hourglass"></i>`
- Ações no cabeçalho do viewer:
  - Copiar código: botão com `<i class="ti ti-copy"></i> Copiar código` (transição para `ti-check` ao copiar).
  - Ver Raw: botão com `<i class="ti ti-file-code"></i> Ver Raw` ou ícone puro em telas compactas.
  - Novo texto: botão secundário com `<i class="ti ti-plus"></i> Novo`.
  - Excluir: botão com `<i class="ti ti-trash"></i> Excluir`.
  - Denunciar: botão com `<i class="ti ti-flag"></i> Denunciar`.
- Para botões secundários com apenas ícone (quando aplicável): obrigatório `aria-label="..."` e `title="..."`.

### 2.5 Modais e Telas Especiais (RF05)
- Modal de Sucesso:
  - Título com `<i class="ti ti-circle-check"></i>`.
  - Botão de copiar URL com `<i class="ti ti-copy"></i>`.
  - Admin Delete Token com `<i class="ti ti-key"></i>`.
  - Botão de abrir publicação com `<i class="ti ti-external-link"></i>`.
- Modal de Denúncia:
  - Título com `<i class="ti ti-flag"></i>`.
  - Botão cancelar com `<i class="ti ti-x"></i>` e confirmar com `<i class="ti ti-send"></i>`.
- Tela de Exclusão (`delete_confirmation.html`):
  - Badge destrutiva com `<i class="ti ti-alert-triangle"></i>`.
  - Botão confirmar exclusão com `<i class="ti ti-trash"></i> Excluir definitivamente`.
  - Botão voltar com `<i class="ti ti-arrow-left"></i> Cancelar e voltar`.
- Tela de Desbloqueio (`password_challenge.html`):
  - Badge com `<i class="ti ti-lock"></i>`.
  - Botão desbloquear com `<i class="ti ti-lock-open"></i> Desbloquear texto`.
  - Botão voltar com `<i class="ti ti-arrow-left"></i> Voltar ao início`.
- Telas de Erro 404 e 451:
  - 404: ícone destacado `<i class="ti ti-file-x"></i>` e botão com `<i class="ti ti-plus"></i> Criar novo texto`.
  - 451: ícone destacado `<i class="ti ti-shield-alert"></i>` e botão com `<i class="ti ti-arrow-left"></i> Voltar à página inicial`.

## 3. Critérios de Aceite
1. Todos os botões principais mantêm contraste e legibilidade, exibindo ícone alinhado de 18px.
2. Botões compactos que substituírem texto por ícone contêm `aria-label` descritivo e foco visível.
3. Não há cores cromáticas adicionadas aos ícones: todos respeitam a paleta neutra e usam `currentColor`.
4. Os testes automatizados em `tests/` continuam passando sem regressão.
