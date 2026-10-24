# 05 - Visualizador Editorial para Pastes Cifrados (AES-256-GCM) e Codificados (Base64)

Status: resolved
Type: task
Blocked by: 03, 04

## Question

Como implementar a decifração em memória no visualizador (`src/inkbin/templates/viewer.html` e `src/inkbin/static/js/ink-editor.js`) a partir do fragmento `#key` na URL, o tratamento de erro/chave ausente, e a alternância de exibição (Decodificado vs. Bruto) com badge e aviso de transparência para pastes em Base64?

## Scope

1. Atualizar `src/inkbin/templates/viewer.html`:
   - Adicionar atributos de metadados (`data-content-format="{{ paste.content_format }}"`).
   - Para `content_format == "aes-256-gcm"`:
     - Incluir container de aviso para estado de erro / chave ausente (`#crypto-error-notice`) oculto por padrão.
     - Incluir badge de status editorial no cabeçalho: `[ AES-256-GCM Client Encrypted ]`.
   - Para `content_format == "base64"`:
     - Exibir banner editorial de transparência: *"Aviso: Este conteúdo está codificado em Base64. Base64 é uma codificação, não criptografia — qualquer pessoa com o link pode lê-lo."*
     - Adicionar botão de alternância na barra de ferramentas: `[ Visualizar Decodificado ]` / `[ Visualizar Base64 Bruto ]`.
2. Implementar lógica de decifração client-side no visualizador (`ink-editor.js`):
   - Se `data-content-format === "aes-256-gcm"`:
     - Extrair fragmento de URL via `window.location.hash.slice(1)`.
     - Se o fragmento estiver vazio: ocultar bloco de código cifrado, exibir alerta editorial de chave ausente e orientar o leitor a solicitar o link completo com o fragmento `#chave`.
     - Se a chave estiver presente:
       - Importar chave via `crypto.subtle.importKey("raw", keyBytes, { name: "AES-GCM" }, false, ["decrypt"])`.
       - Decodificar o payload Base64 recebido do backend em buffer de bytes.
       - Separar os 12 bytes do IV e o restante (ciphertext + tag).
       - Executar `crypto.subtle.decrypt()`.
       - Ao obter sucesso, substituir o texto cifrado no elemento `<code>` pelo texto decifrado e executar `hljs.highlightElement()`.
       - Se a decifração lançar erro (chave corrompida ou inválida): exibir erro claro de chave incorreta.
3. Implementar lógica de alternância Base64 no visualizador:
   - Manter em memória tanto a versão Base64 bruta quanto o texto decodificado (decodificado com suporte a caracteres UTF-8 multilíngues).
   - Ao clicar no botão de alternância, trocar o conteúdo renderizado mantendo a formatação e contadores de caracteres.
4. Ajustar botão de cópia de código para copiar o texto decifrado/decodificado ativo na tela.

## Answer

Implementado com sucesso o visualizador editorial para AES-256-GCM e Base64:
1. `viewer.html` atualizado com atributos semânticos `data-content-format`, badges editoriais para formatos criptografados e Base64, aviso de transparência Base64 (`.base64-notice-banner`), botão de alternância `#toggle-base64-btn` e container preventivo de chave ausente/inválida `#crypto-error-notice`.
2. Lógica `setupViewerContent()` integrada no ciclo de carregamento da página em `ink-editor.js`:
   - Para `aes-256-gcm`: extrai o fragmento `#key`, importa via Web Crypto API, separa IV de 12 bytes e decifra AES-GCM. Oculta o container de código e exibe orientações claras caso o fragmento esteja ausente ou a chave seja inválida.
   - Para `base64`: decodifica automaticamente UTF-8 para exibição imediata e provê alternador bidirecional entre conteúdo decodificado e Base64 bruto preservando highlight de sintaxe.
3. Botão de cópia de código copia diretamente o conteúdo ativo exibido no elemento `<code>` (texto limpo decifrado ou versão alternada ativa).
4. Estilos do INK Design System v2 aplicados em `ink-editorial.css` e testes automatizados validados em `tests/test_web_ui.py`.
