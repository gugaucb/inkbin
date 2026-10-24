# 01 Vendor QRCode.js e Estilos INK

Type: task  
Status: resolved  

## Question
Como disponibilizar a biblioteca QRCode.js sem dependências externas e estilizar o container do QR Code respeitando o INK Design System v2?

## Plan
1. Disponibilizar a biblioteca JavaScript minificada em `src/inkbin/static/js/qrcode.min.js`.
2. Adicionar as regras de estilização em `src/inkbin/static/css/ink-editorial.css`:
   - `.modal-qr-section`
   - `.modal-qr-container`
   - `.qr-code-box`
   - `.qr-hint-text`
3. Assegurar que a *quiet zone* seja preservada com fundo branco `#ffffff` para alta legibilidade por câmeras móveis.

## Answer
- A biblioteca QRCode.js (19KB) foi vendoreada localmente em `src/inkbin/static/js/qrcode.min.js`, garantindo operação offline e ausência de chamadas adicionais de rede.
- As classes CSS necessárias foram adicionadas em `ink-editorial.css`, incorporando fundo `--surface-subtle`, bordas `--border-default`, e container `.qr-code-box` com fundo `#ffffff` e raio `var(--radius-md)`.
