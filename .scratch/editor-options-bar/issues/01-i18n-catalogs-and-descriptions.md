# Issue 01: Catálogos i18n e Textos Descritivos

Type: task
Status: resolved
Blocked by:

## Answer

Chaves de tradução adicionadas aos arquivos `en.json`, `pt-br.json` e `cn.json` com 100% de paridade, cobrindo os rótulos da barra de opções (`options_expires_in`, `option_password`, `option_encrypt`, `option_burn`, `option_base64`) e descrições explicativas detalhadas (`desc_encrypt`, `desc_burn`, `desc_base64`, `desc_password`). Testes de integridade e paridade `tests/test_i18n.py` aprovados (10/10).

## Question

Como atualizar os catálogos de tradução `en.json`, `pt-br.json` e `cn.json` para suportar os novos textos da barra de opções e das explicações dinâmicas com 100% de paridade?

## Details

- Cadastrar as chaves de labels e descrições detalhadas para as opções:
  - `editor.options_expires_in`: "Expires in" / "Expira em" / "过期时间"
  - `editor.option_password`: "Password" / "Senha" / "密码"
  - `editor.option_encrypt`: "Encrypt in browser" / "Criptografar no navegador" / "在浏览器中加密"
  - `editor.option_burn`: "Burn after read" / "Destruir após leitura" / "阅后即焚"
  - `editor.option_base64`: "Base64" / "Base64" / "Base64"
  - `editor.desc_encrypt`: "Encrypt in browser: content is encrypted with AES-256-GCM before upload. The key is added to the share link after “#” and never sent to the server — lose the full link and the paste can't be decrypted." / versão em pt-br e cn.
  - `editor.desc_burn`: "Burn after read: the paste is deleted after the first confirmed view — readers are asked to confirm before it opens." / versão em pt-br e cn.
  - `editor.desc_base64`: "Base64: Base64 is encoding, not encryption — anyone with the link can decode it." / versão em pt-br e cn.
  - `editor.desc_password`: "Password: the paste requires a password to view, verified securely with Argon2id." / versão em pt-br e cn.
