# 03 Internacionalização e Acessibilidade

Type: task  
Status: resolved  
Blocked by: 02  

## Question
Como prover suporte completo aos três idiomas suportados (`en`, `pt-br`, `cn`) para os novos rótulos, dicas e atributos acessíveis de leitura de tela do QR Code?

## Plan
1. Atualizar `src/inkbin/locales/en.json` com `modal.qr_code_label`, `modal.qr_code_hint` e `modal.qr_code_aria`.
2. Atualizar `src/inkbin/locales/pt-br.json` com as traduções em português brasileiro.
3. Atualizar `src/inkbin/locales/cn.json` com as traduções em chinês simplificado.
4. Garantir que o contêiner de imagem possua `role="img"` e `aria-label` descritivo (WCAG 2.1 AA).

## Answer
- Chaves de internacionalização adicionadas nos 3 arquivos de catálogo JSON (`en.json`, `pt-br.json`, `cn.json`).
- O contêiner `#modal-qrcode` recebeu `role="img"` e `aria-label="{{ t('modal.qr_code_aria') }}"`.
- Atributos `aria-hidden="true"` aplicados nos ícones decorativos da seção.
