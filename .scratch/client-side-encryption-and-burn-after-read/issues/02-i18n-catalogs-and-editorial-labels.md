# 02 - Catálogos i18n para Formatos de Cifragem, Burn After Read e Avisos Editoriais

Status: open
Type: task
Blocked by: none

## Question

Como estruturar as chaves e textos nos catálogos de internacionalização (`src/inkbin/locales/en.json`, `pt-br.json`, `cn.json`) com 100% de paridade para cobrir a seleção de formato no editor, a opção e tela intermediária de Burn after read, e os avisos de segurança/transparência de criptografia no cliente e Base64?

## Scope

1. Adicionar seções e chaves nos catálogos `en.json`, `pt-br.json` e `cn.json`:
   - Seletor de Formato no Editor:
     - `editor.format_label`: Rótulo do campo (ex: "Modo de Conteúdo / Segurança").
     - `editor.format_plaintext`: "Texto puro (Padrão)".
     - `editor.format_aes_gcm`: "Criptografar no navegador (AES-256-GCM)".
     - `editor.format_base64`: "Codificação Base64".
     - `editor.format_base64_hint`: "Base64 é uma codificação e não criptografia — qualquer pessoa com o link pode lê-lo."
   - Modificador Burn After Read:
     - `editor.burn_label`: "Destruir após leitura (Burn after read)".
     - `editor.burn_hint`: "O paste será excluído permanentemente após a primeira visualização confirmada."
   - Modal de Sucesso com Link Cifrado:
     - `modal.encrypted_notice`: "Criptografado com AES-256-GCM. A chave de decifração reside unicamente após o '#' da URL e jamais foi enviada ao servidor. Se o link for perdido, o conteúdo não poderá ser recuperado."
   - Tela Intermediária de Burn After Read:
     - `burn.page_title`: "Destruição Após Leitura — Inkbin".
     - `burn.badge`: "Ação Irreversível".
     - `burn.title`: "Este paste será destruído após a leitura".
     - `burn.description`: "O autor configurou este documento para ser excluído permanentemente do servidor assim que for aberto. Deseja revelar o conteúdo agora?".
     - `burn.confirm_btn`: "Revelar e Destruir Paste".
     - `burn.burned_banner`: "Este documento foi destruído permanentemente do banco de dados na visualização atual.".
   - Avisos no Visualizador:
     - `viewer.base64_badge`: "Base64 Codificado".
     - `viewer.base64_notice`: "Aviso: Este conteúdo está codificado em Base64. Base64 é uma codificação, não criptografia — qualquer pessoa com o link pode lê-lo.".
     - `viewer.base64_toggle_decoded`: "Visualizar Decodificado".
     - `viewer.base64_toggle_raw`: "Visualizar Base64 Bruto".
     - `viewer.encrypted_badge`: "AES-256-GCM Cifrado no Cliente".
     - `viewer.encrypted_missing_key`: "Chave de decifração ausente no link (#chave). Sem a chave original, este documento não pode ser decifrado.".
2. Garantir ausência de chaves órfãs e paridade total entre os três idiomas.
3. Adicionar testes unitários em `tests/test_i18n.py`.
