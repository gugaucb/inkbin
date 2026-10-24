# 02 - Marcação Semântica e Componente Editorial na Página Principal

Status: resolved
Type: task
Blocked by: 01

## Question

Como estruturar a marcação HTML semântica da seção de garantias e recursos em `src/inkbin/templates/editor.html` utilizando o vocabulário visual do INK Design System v2 e ícones Tabler, mantendo o formulário do editor como foco primário e garantindo acessibilidade (WCAG 2.1 AA)?

## Scope

1. Adicionar `<section class="platform-features-section" aria-labelledby="features-section-title">` em `src/inkbin/templates/editor.html` logo abaixo do formulário de criação (`#paste-form`).
2. Criar um grid de micro-cards (`.feature-card`) contendo:
   - Ícone vetorial Tabler associado (`ti-ghost`, `ti-lock`, `ti-clock`, `ti-terminal-2`, `ti-shield-check`, `ti-code`, `ti-user-off`, `ti-trash`) com `aria-hidden="true"`.
   - Título do pilar com tipografia editorial concisa.
   - Breve descrição objetiva derivada das chaves i18n (`t('features....')`).
3. Manter a hierarquia de cabeçalhos semânticos e tags semânticas (evitando poluição na leitura por leitores de tela).
4. Posicionar o componente de forma não intrusiva abaixo do rodapé de publicação (`.editor-footer-actions`).

## Answer

Adicionada a seção `<section class="platform-features-section" aria-labelledby="features-section-title">` em `src/inkbin/templates/editor.html` posicionada abaixo do formulário de submissão do editor. A vitrine contém o cabeçalho editorial com ícone `ti-shield-check` e um grid semântico de 8 micro-cards (`.feature-card`), cada um estruturado com seu respectivo ícone Tabler (`ti-ghost`, `ti-lock`, `ti-clock`, `ti-terminal-2`, `ti-shield-check`, `ti-code`, `ti-user-off`, `ti-trash`) marcado com `aria-hidden="true"`, título editorial e descrição localizada via Jinja2 `t('features.*')`. O teste `test_editor_platform_features_showcase_markup` foi adicionado em `tests/test_web_ui.py` cobrindo toda a marcação e acessibilidade.
