# 04 - Modais Responsivos, QR Code e Telas Auxiliares

Status: resolved
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

## Answer

Modais e telas auxiliares totalmente responsivos:
- Modais (`.modal-dialog`) ajustados para `width: min(92vw, 480px)` no desktop e `width: min(94vw, 480px)` no mobile, com suporte a rolagem interna em `.modal-body` (`overflow-y: auto; max-height: 90vh/90dvh`).
- QR code (`.modal-qr-container` / `.qr-code-box`) centralizado com imagem/canvas flexível (`max-width: 100%; height: auto;`).
- Grupos de inputs e botões de cópia configurados com `.modal-input-group` que colapsam verticalmente no mobile para garantir alvos de clique confortáveis (44px).
- Telas de autenticação (`password_challenge.html`) e exclusão (`delete_confirmation.html`) refatoradas para `.aux-card` com espaçamento fluido e botões em coluna inversa (`.aux-card-actions`).
- Telas de erro (`404.html` e `451.html`) padronizadas com a classe `.error-card` com tipografia responsiva e quebra de palavras segura.
