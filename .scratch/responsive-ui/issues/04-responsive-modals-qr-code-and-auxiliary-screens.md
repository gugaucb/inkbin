# 04 - Modais Responsivos, QR Code e Telas Auxiliares

Status: open
Type: task
Blocked by: 01

## Question

Como otimizar os modais (sucesso com QR Code e denúncia de abuso) e as telas auxiliares (`password_challenge.html`, `delete_confirmation.html`, `404.html`, `451.html`) para que se ajustem perfeitamente a larguras estreitas (320px–480px) sem cortes laterais e com usabilidade tátil?

## Scope

1. Responsividade dos modais em `src/inkbin/static/css/ink-editorial.css`:
   - `.modal-dialog`: ajustar largura para `width: min(92vw, 480px); max-width: 100%; margin: 16px auto;`.
   - `.modal-body`: padding flexível (`--space-4` no mobile e `--space-6` no desktop).
   - `.modal-qr-container`: caixa do QR code centralizada e redimensionável sem vazar da tela.
   - Agrupamento de inputs e botões de cópia (URL e Admin Delete Token) para quebrarem em coluna única se a largura for inferior a 340px.
2. Telas de Desafio de Senha e Exclusão:
   - Formulários em `password_challenge.html` e `delete_confirmation.html` com cards centralizados, preenchimento fluído de 100% da largura útil e botões acessíveis.
3. Telas de Erro (404 e 451):
   - Tipografia responsiva com ícones e mensagens centralizadas legíveis em celulares.
