# 03 - Criptografia Client-Side (Web Crypto API) e Integração no Editor

Status: resolved
Type: task
Blocked by: 01, 02

## Question

Como implementar a interface de seleção no editor (`src/inkbin/templates/editor.html`), a engine criptográfica cliente via Web Crypto API no JavaScript (`src/inkbin/static/js/ink-editor.js`) para AES-256-GCM, o encoder de Base64, e a geração do link compartilhado com fragmento `#key` no modal de confirmação?

## Scope

1. Atualizar o formulário do editor em `src/inkbin/templates/editor.html`:
   - Adicionar o campo seletor de formato `paste-content-format` (`plaintext`, `aes-256-gcm`, `base64`) com ícones Tabler (`ti-shield-lock`, `ti-code`, `ti-binary`).
   - Adicionar o checkbox/toggle `paste-burn-after-read` estilizado nos padrões do INK Design System com rótulo e ícone (`ti-flame`).
   - Exibir hint reativo para a opção Base64 ("Base64 é uma codificação e não criptografia").
2. Implementar módulo criptográfico no cliente em `src/inkbin/static/js/ink-editor.js`:
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

## Answer

Implementados com sucesso os controles do editor e a engine Web Crypto client-side:
1. Formulário em `editor.html` enriquecido com seletor `paste-content-format`, checkbox estilizado `paste-burn-after-read` com ícone `ti-flame`, hint reativo informativo `base64-warning-hint` e container de aviso de segurança `#modal-encrypted-notice`.
2. Módulo de criptografia e codificação adicionado a `ink-editor.js` implementando geração de chaves AES-256-GCM, cifragem autenticada com IV de 12 bytes aleatórios, exportação/importação Base64URL e conversões UTF-8 seguras.
3. Submissão do formulário interceptada para cifrar payloads ou codificar em Base64 transparentemente no navegador antes do envio `POST /api/pastes`.
4. Modal de sucesso compõe o link com o fragmento `#key` na URL (garantia Zero-Knowledge), atualiza campos de cópia, links e QR Code móvel, e renderiza aviso editorial enfático sobre a retenção da chave exclusivamente pelo usuário.
5. Estilos editoriais adicionados a `ink-editorial.css` e testes de interface validados em `tests/test_web_ui.py`.
