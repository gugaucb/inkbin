# 03 - Criptografia Client-Side (Web Crypto API) e Integração no Editor

Status: open
Type: task
Blocked by: 01, 02

## Question

Como implementar a interface de seleção no editor (`src/inkbin/templates/editor.html`), a engine criptográfica cliente via Web Crypto API no JavaScript (`src/inkbin/static/js/main.js`) para AES-256-GCM, o encoder de Base64, e a geração do link compartilhado com fragmento `#key` no modal de confirmação?

## Scope

1. Atualizar o formulário do editor em `src/inkbin/templates/editor.html`:
   - Adicionar o campo seletor de formato `paste-content-format` (`plaintext`, `aes-256-gcm`, `base64`) com ícones Tabler (`ti-lock`, `ti-code`, `ti-binary`).
   - Adicionar o checkbox/toggle `paste-burn-after-read` estilizado nos padrões do INK Design System com rótulo e ícone (`ti-flame` ou `ti-fire`).
   - Exibir hint reativo para a opção Base64 ("Base64 é uma codificação e não criptografia").
2. Implementar módulo criptográfico no cliente em `src/inkbin/static/js/main.js`:
   - Função `generateAesKey()`: `crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, true, ["encrypt", "decrypt"])`.
   - Função `encryptText(text, key)`: gera IV de 12 bytes (`crypto.getRandomValues`), cifra texto UTF-8, combina `IV + ciphertext` e codifica em Base64.
   - Função `exportKeyToBase64Url(key)`: exporta chave bruta e codifica em Base64URL seguro para uso em URLs.
   - Função de codificação Base64 para a opção `base64`.
3. Interceptar a submissão do formulário:
   - Se `aes-256-gcm`: executa cifragem no navegador, envia o payload cifrado para a API, armazena temporariamente a chave gerada.
   - Se `base64`: codifica o texto em Base64 e envia com `content_format="base64"`.
   - Se `burn_after_read`: envia `burn_after_read: true`.
4. Atualizar o modal de sucesso:
   - Ao receber a resposta da API, se o formato for `aes-256-gcm`, compor a URL final: `${data.url}#${keyBase64Url}`.
   - Atualizar tanto o campo de input do link, botão de cópia, link "Abrir paste" e geração do QR Code para conter a URL completa com `#key`.
   - Exibir o aviso editorial de segurança do paste criptografado.
