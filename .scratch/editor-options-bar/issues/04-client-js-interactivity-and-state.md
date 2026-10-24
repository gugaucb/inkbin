# Issue 04: Interatividade e Estado do Cliente em JS

Type: task
Status: resolved
Blocked by: 03

## Answer

Implementada lógica completa de cliente em `ink-editor.js`: alternância inteligente dos radios de formato com suporte a desmarcação (clique no radio ativo desmarca e retorna a texto puro), revelação dinâmica do campo de senha com foco e limpeza automática ao desmarcar, sincronização do input hidden `paste-content-format` e renderização em tempo real das explicações com marcadores de ponto ciano (`•`) com base nos atributos i18n do container. Submissão assíncrona compatível com AES-256-GCM, Base64 e senhas.

## Question

Como atualizar `ink-editor.js` para controlar o comportamento de alternância de formatos (radio buttons com deseleção), exibição condicional do campo de senha, renderização das explicações ativas com marcadores ciano e envio correto à API?

## Details

- Lógica de seleção de formato:
  - Radio buttons `paste-format-encrypt` e `paste-format-base64`.
  - Clicar no radio atualmente ativo desmarca-o, retornando o formato para `plaintext`.
  - Atualização do valor do formato enviado no payload (`content_format: "plaintext" | "aes-256-gcm" | "base64"`).
- Lógica de senha (`paste-password-toggle`):
  - Ao marcar, exibe o container do input `paste-password` e foca nele.
  - Ao desmarcar, oculta o container e limpa o valor da senha para não enviar acidentalmente.
- Atualização em tempo real das explicações:
  - Função `updateExplanations()` acionada em qualquer mudança nas opções.
  - Renderiza as linhas de explicação correspondentes às opções ativas com o ponto ciano `•`.
- Submissão assíncrona:
  - Manter cifragem cliente AES-256-GCM via Web Crypto API.
  - Manter codificação Base64.
  - Enviar payload correto para `/api/pastes`.
