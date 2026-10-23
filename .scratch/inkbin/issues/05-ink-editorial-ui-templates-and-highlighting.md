# 05 - Interface editorial INK com Jinja2, tokens CSS e syntax highlighting

Type: prototype
Status: open
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
