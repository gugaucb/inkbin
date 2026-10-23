# 04 - Ícones em Ações e Metadados do Visualizador

Status: resolved
Type: task
Blocked by: 01

## Question

Como enriquecer os metadados e os botões de ação do visualizador (viewer.html) com Tabler Icons, aplicando ícones + texto em ações principais e ícones compactos acessíveis em ações secundárias?

## Scope

1. Em `src/inkbin/templates/viewer.html`:
   - Metadados:
     - Badge de linguagem: `<i class="ti ti-code"></i> {{ paste.language }}`
     - Data: `<i class="ti ti-calendar"></i> Publicado em {{ formatted_date }}`
     - Visualizações: `<i class="ti ti-eye"></i> {{ paste.views_count }} visualizações`
     - Expiração: `<i class="ti ti-hourglass"></i> Expira em: {{ formatted_expires }}`
   - Botões de Ação na barra `.viewer-actions`:
     - Botão Copiar: `<button id="copy-code-btn" class="btn btn-primary"><i class="ti ti-copy"></i> <span>Copiar código</span></button>` (com alternância dinâmica para `ti-check` e feedback visual em `ink-editor.js`).
     - Botão Raw: `<a href="/raw/..." class="btn btn-secondary" title="Ver conteúdo bruto (raw)" aria-label="Ver código bruto"><i class="ti ti-file-code"></i> <span>Ver Raw</span></a>`.
     - Botão Novo: `<a href="/" class="btn btn-secondary" title="Criar nova publicação" aria-label="Criar nova publicação"><i class="ti ti-plus"></i> <span>Novo texto</span></a>`.
     - Botão Excluir: `<a href="/p/.../delete" class="btn btn-secondary" title="Excluir este paste" aria-label="Excluir este paste"><i class="ti ti-trash"></i> <span>Excluir</span></a>`.
     - Botão Denunciar: `<button id="open-report-btn" class="btn btn-secondary" title="Denunciar publicação" aria-label="Denunciar publicação"><i class="ti ti-flag"></i> <span>Denunciar</span></button>`.
   - Adicionar regras responsivas em `ink-editorial.css` para que em telas menores as ações secundárias possam recolher o label de texto mantendo o ícone e o `aria-label`.

## Answer

Implementados ícones na tela do visualizador (viewer):
- Metadados enriquecidos com `ti-code`, `ti-calendar`, `ti-eye` e `ti-hourglass`.
- Barra de ações estruturada com `ti-copy`, `ti-file-code`, `ti-plus`, `ti-trash` e `ti-flag`.
- Alternância dinâmica de `ti-copy` para `ti-check` com feedback temporal no JavaScript.
- Adicionados atributos de acessibilidade WCAG (`aria-label` e `title`) em todos os botões e regras responsivas em `ink-editorial.css` para recolhimento limpo de labels em telas compactas (<= 640px).
- Testes validados em `tests/test_web_ui.py`.

