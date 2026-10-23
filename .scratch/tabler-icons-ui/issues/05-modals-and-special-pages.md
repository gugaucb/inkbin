# 05 - Ícones em Modais e Telas Especiais

Status: open
Type: task
Blocked by: 02, 03, 04

## Question

Como aplicar ícones Tabler em modais (sucesso de criação, denúncia de abuso) e telas especiais (exclusão por token, desafio de senha e páginas 404/451)?

## Scope

1. Modal de Sucesso em `src/inkbin/templates/editor.html`:
   - Ícone de sucesso no título: `<i class="ti ti-circle-check"></i>`.
   - Botões de cópia de URL e Admin Delete Token com `<i class="ti ti-copy"></i>`.
   - Botão "Abrir publicação" com `<i class="ti ti-external-link"></i>`.
2. Modal de Denúncia em `src/inkbin/templates/viewer.html`:
   - Ícone no título: `<i class="ti ti-flag"></i>`.
   - Botões de Cancelar (`ti-x`) e Enviar denúncia (`ti-send`).
3. Tela de Exclusão `src/inkbin/templates/delete_confirmation.html`:
   - Badge destrutiva com `<i class="ti ti-alert-triangle"></i>`.
   - Botão voltar com `<i class="ti ti-arrow-left"></i>` e confirmar exclusão com `<i class="ti ti-trash"></i>`.
4. Tela de Desafio de Senha `src/inkbin/templates/password_challenge.html`:
   - Badge com `<i class="ti ti-lock"></i>`.
   - Botão voltar com `<i class="ti ti-arrow-left"></i>` e botão desbloquear com `<i class="ti ti-lock-open"></i>`.
5. Páginas 404 (`404.html`) e 451 (`451.html`):
   - Ícones ilustrativos centrais: `ti-file-x` (404) e `ti-shield-alert` (451).
   - Botões de navegação com `ti-plus` e `ti-arrow-left`.
