# 02 - Marcação Semântica e Componente Editorial na Página Principal

Status: open
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
