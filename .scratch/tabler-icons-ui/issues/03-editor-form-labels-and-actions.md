# 03 - Ícones em Labels e Ações do Formulário de Criação

Status: resolved
Type: task
Blocked by: 01

## Question

Como integrar os ícones do Tabler nos rótulos de campos (labels), na toolbar de métricas e no botão principal de submissão do editor em editor.html?

## Scope

1. Em `src/inkbin/templates/editor.html`:
   - Incluir ícones nos `<label class="field-label">`:
     - Título do texto: `<i class="ti ti-heading"></i>`
     - Linguagem / Sintaxe: `<i class="ti ti-code"></i>`
     - Prazo de expiração: `<i class="ti ti-clock"></i>`
     - Senha de proteção: `<i class="ti ti-lock"></i>`
   - Na toolbar de estatísticas do editor:
     - Contador de caracteres com `<i class="ti ti-letter-case"></i>`.
     - Contador de bytes com `<i class="ti ti-database"></i>`.
   - No botão de envio `.btn-primary`:
     - `<button type="submit" id="submit-btn" class="btn btn-primary"><i class="ti ti-upload"></i> <span>Publicar texto</span></button>`.
   - Ajustar no `ink-editor.js` o estado de loading do botão (`submitBtn.innerHTML = '<i class="ti ti-loader animate-spin"></i> Publicando...'`).

## Answer

Implementados ícones no formulário do editor:
- Rótulos dos campos (`.field-label`) enriquecidos com `ti-heading`, `ti-code`, `ti-clock` e `ti-lock`.
- Toolbar de métricas enriquecida com `ti-letter-case` e `ti-database`, preservando reatividade em tempo real no JS.
- Botão de envio primário estruturado com `ti-upload` e transição para `ti-loader` com rotação via CSS durante envio assíncrono.
- Validação automática de integridade e testes no `tests/test_web_ui.py`.

