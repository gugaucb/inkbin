# Spec: Barra de Opções e Segurança do Editor

## Visão Geral

Redesenhar os controles de expiração, formato, segurança e ciclo de vida do Inkbin, consolidando-os em uma barra de opções (`.editor-options-bar`) posicionada imediatamente abaixo do container de texto (`.editor-container`) e acima do botão de publicação, conforme especificação visual fornecida e alinhamento via `/wayfinder`.

## Objetivos e Mudanças Estruturais

1. **Reorganização do Topo (`.editor-header-fields`)**:
   - Manter no cabeçalho superior apenas os campos de metadados principais: **Título** (`paste-title`) e **Linguagem / Sintaxe** (`paste-language`).
   - Remover da barra superior o dropdown redundante `paste-content-format`, o checkbox antigo `paste-burn-after-read`, o campo estático de senha e o seletor antigo de expiração.

2. **Nova Barra de Opções (`.editor-options-bar`)**:
   - Posicionada diretamente abaixo de `.editor-container`.
   - **Seletor de Expiração Integrado** (`Expires in`): Caixa estilizada com label superior compacto e dropdown estilizado (`1 hour`, `1 day`, `1 week`, `1 month`, `never`).
   - **Controles de Segurança e Formato**:
     - `Password`: Checkbox que, ao ser marcado, revela dinamicamente o campo para digitação da senha de proteção com Argon2id.
     - `Encrypt in browser`: Radio button / seletor de formato AES-256-GCM client-side com chave no hash `#key`.
     - `Burn after read`: Checkbox de destruição pós-leitura com confirmação intermediária.
     - `Base64`: Radio button de codificação textual transparente.
   - **Comportamento de Seleção de Formato**:
     - `Encrypt in browser` e `Base64` são mutuamente exclusivos (radio button).
     - Clicar na opção ativa desmarca-a, retornando para texto puro (*plaintext*).
     - `Burn after read` e `Password` são independentes e combináveis com qualquer formato.

3. **Painel Dinâmico de Explicações e Dicas**:
   - Exibido logo abaixo da linha de opções.
   - Lista explicativa com marcadores de ponto ciano (`•`) detalhando o funcionamento das opções ativas:
     - **Encrypt in browser**: `Encrypt in browser: content is encrypted with AES-256-GCM before upload. The key is added to the share link after “#” and never sent to the server — lose the full link and the paste can't be decrypted.`
     - **Burn after read**: `Burn after read: the paste is deleted after the first confirmed view — readers are asked to confirm before it opens.`
     - **Base64**: `Base64: Base64 is encoding, not encryption — anyone with the link can decode it.`
     - **Password**: `Password: the paste requires a password to view, verified securely with Argon2id.`

4. **Estilo Editorial e Acessibilidade (INK Design System v2)**:
   - Cores e bordas monocromáticas com acento ciano/teal (`#14b8a6` / `#22d3ee`) nos indicadores ativos e marcadores.
   - Suporte completo a navegação por teclado e foco acessível.
   - Responsividade para telas menores que 900px e 640px.

5. **Internacionalização (i18n)**:
   - Paridade 100% entre `en.json`, `pt-br.json` e `cn.json` para todos os novos rótulos e textos explicativos.
