# 05 - Interface editorial INK com Jinja2, tokens CSS e syntax highlighting

Type: prototype
Status: resolved
Blocked by: 03

## Question

Como implementar a interface web server-rendered utilizando templates Jinja2, tokens do INK Design System v2 (`ink-tokens.css`) e realce de sintaxe com Prism.js / highlight.js, garantindo visual monocromático editorial e pontuação de acessibilidade WCAG 2.1 AA?

## Context & Requirements

- Conexão direta com as diretrizes de [INK Design System v2](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/docs/agents/INK_Design_System_v2.md):
  - Paleta monocromática estrita (`--ink-0` a `--ink-950`).
  - Fontes: `Inter` para interface e `JetBrains Mono` para trechos de código e editor.
  - Densidade editorial, margens generosas e ausência de cores cromáticas de destaque.
- Telas principais:
  1. **Editor / Criação**: Barra lateral compacta (`AppSidebar`), campo de título opcional, textarea com suporte a tabulações e contagem de caracteres/tamanho, seletor de linguagem e prazo de expiração, botão "Publicar".
  2. **Visualização de Paste**: Cabeçalho editorial com título, data/hora formatada em pt-BR, linguagem, contador de visualizações, botões de ação ("Copiar código", "Ver Raw", "Novo Paste").
  3. **Modal de Sucesso / Token**: Exibição da URL pública gerada e do `Admin Delete Token` com aviso claro para o usuário salvar a chave caso queira excluir o paste no futuro.

## Answer

Interface editorial monocromática INK Design System v2 implementada e renderizada via Jinja2:
1. `src/inkbin/static/css/ink-tokens.css`: Especificação canônica dos tokens de primitivos (`--ink-0` a `--ink-950`), semânticos (`--canvas`, `--sidebar-bg`, `--surface`, `--border-default`, `--focus-ring`) e tipografia (`Inter`, `JetBrains Mono`). Zero acentos cromáticos.
2. `src/inkbin/static/css/ink-editorial.css`: Estruturas `app-shell`, `app-sidebar` de 248px, topbar de 64px, container central de 1120px, botões primários monocromáticos e anéis de foco de 2px acessíveis (WCAG 2.1 AA).
3. `src/inkbin/templates/`:
   - `base.html`: Shell com skip link de acessibilidade, sidebar de navegação e histórico, topbar e área de conteúdo.
   - `editor.html`: Formulário com título opcional, seletores de linguagem e expiração, textarea com estatísticas em tempo real e modal com aviso proeminente do `Admin Delete Token`.
   - `viewer.html`: Cabeçalho editorial limpo, metadados formatados em pt-BR, contador de visualizações, botões de cópia rápida e bloco de código monoespaçado.
   - `404.html`: Tratamento de página não encontrada ou expirada.
4. `src/inkbin/static/js/ink-editor.js`: Gerenciamento de eventos de teclado (suporte a Tab no editor sem perder foco), estatísticas de tamanho/caracteres, envio assíncrono e feedback honesto de cópia (`navigator.clipboard`).
5. Testes automatizados em `tests/test_web_ui.py` cobrindo carregamento do editor, viewer, página 404 e arquivos estáticos.
