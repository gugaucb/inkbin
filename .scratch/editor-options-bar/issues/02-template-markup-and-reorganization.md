# Issue 02: Estrutura do Template HTML do Editor

Type: task
Status: resolved
Blocked by: 01

## Answer

Estrutura HTML de `editor.html` reorganizada com sucesso: o cabeçalho superior (`.editor-header-fields`) foi limpo para conter apenas Título e Linguagem/Sintaxe; a barra de opções (`.editor-options-bar`) foi inserida diretamente abaixo do container de texto (`.editor-container`), composta pela caixa de controle de expiração estilizada (`Expires in`), grupo de toggles/radios de segurança (`Password`, `Encrypt in browser`, `Burn after read`, `Base64`), campo retrátil de senha e o painel de explicações dinâmicas com atributos de tradução. 17 testes de UI aprovados (100%).

## Question

Como reestruturar `editor.html` para posicionar a barra de opções (`.editor-options-bar`) diretamente abaixo de `.editor-container`, limpando o cabeçalho superior e adicionando o container de explicações dinâmicas e o campo retrátil de senha?

## Details

- Manter em `.editor-header-fields` apenas `paste-title` e `paste-language`.
- Inserir `.editor-options-bar` imediatamente após `.editor-container`:
  - Seletor estilizado de expiração (`paste-expiration`) com label superior compacto.
  - Grupo de opções com checkboxes e radiobuttons:
    - Checkbox `paste-password-toggle` com input de senha retrátil associado (`paste-password`).
    - Radio button `paste-format-encrypt` com `value="aes-256-gcm"`.
    - Checkbox `paste-burn-after-read`.
    - Radio button `paste-format-base64` com `value="base64"`.
- Container dinâmico `.editor-options-explanations` para os marcadores de ponto ciano com as explicações das opções ativas.
- Preservar acessibilidade (atributos `aria-`, `role="note"` e labels semânticos).
