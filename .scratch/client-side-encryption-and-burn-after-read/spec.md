# Especificação Técnica: Criptografia Client-side, Burn After Read e Codificação Base64

**Status**: Aprovado  
**Data**: 2026-10-24  
**Local**: `.scratch/client-side-encryption-and-burn-after-read/spec.md`  
**Escopo**: Adição das opções de segurança avançada e formatos de privacidade no Inkbin:
1. **Encrypt in browser**: Cifragem ponta-a-ponta no cliente com AES-256-GCM antes do upload, com a chave simétrica adicionada exclusivamente ao fragmento `#key` na URL e nunca enviada ao servidor (*Zero-Knowledge*).
2. **Burn after read**: Destruição física definitiva do paste após a primeira visualização confirmada pelo leitor, com tela intermediária (*interstitial confirmation screen*) para prevenção de disparo involuntário por crawlers e pré-visualizadores de links (WhatsApp, Slack, Discord, Telegram).
3. **Base64**: Codificação de texto em Base64 com aviso editorial explícito de transparência ("Base64 é uma codificação e não criptografia — qualquer pessoa com o link pode decodificá-lo") e alternância no visualizador entre texto decodificado e Base64 bruto.

---

## 1. Arquitetura e Modelo de Domínio

### 1.1 Atualizações no Modelo de Domínio (`GLOSSARY.md`)
- **Client-Side Encryption**: Processo de cifragem simétrica com AES-256-GCM executado integralmente no navegador do autor via Web Crypto API antes do envio, onde a chave secreta reside exclusivamente no fragmento da URL (`#key`) e nunca é transmitida ou armazenada no servidor.
- **Burn After Read**: Política de retenção e descarte permanente em que o paste é fisicamente expurgado após a primeira visualização confirmada pelo leitor, resguardada por uma tela intermediária de confirmação para impedir consumo involuntário por rastreadores e pré-visualizadores de links.
- **Base64 Encoding**: Formato de transformação e representação textual que não provê segurança criptográfica, acompanhado de aviso editorial transparente e alternância entre conteúdo decodificado e bruto.

### 1.2 Atualização no Banco de Dados (`Paste` Model)
Dois novos campos no modelo relacional `Paste` (`src/inkbin/models.py`):
- `content_format`: `Mapped[str] = mapped_column(String(20), default="plaintext", nullable=False)`
  - Valores válidos: `"plaintext"`, `"aes-256-gcm"`, `"base64"`.
- `burn_after_read`: `Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)`

Migração incremental automática em `_sync_migrate_schema` (`src/inkbin/db.py`) com compatibilidade para SQLite e PostgreSQL:
```python
if "content_format" not in existing_cols:
    connection.execute(text("ALTER TABLE pastes ADD COLUMN content_format VARCHAR(20) DEFAULT 'plaintext' NOT NULL"))
if "burn_after_read" not in existing_cols:
    connection.execute(text(f"ALTER TABLE pastes ADD COLUMN burn_after_read BOOLEAN DEFAULT {bool_false} NOT NULL"))
```

---

## 2. Especificação Criptográfica Client-Side (AES-256-GCM)

### 2.1 Geração de Chave e Cifragem no Cliente (`main.js`)
Quando `content_format == "aes-256-gcm"`:
1. O autor preenche o conteúdo no editor.
2. Ao submeter o formulário:
   - Gera chave simétrica aleatória de 256 bits via `crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, true, ["encrypt", "decrypt"])`.
   - Gera vetor de inicialização (IV) de 12 bytes aleatórios via `crypto.getRandomValues(new Uint8Array(12))`.
   - Codifica o texto em UTF-8 (`TextEncoder`).
   - Cifra com `crypto.subtle.encrypt({ name: "AES-GCM", iv: iv }, key, encodedText)`.
   - Concatena o IV de 12 bytes com o ciphertext gerado (que inclui a tag de autenticação GCM de 16 bytes).
   - Codifica o pacote binário resultante em Base64 padrão para transmissão no campo `content`.
   - Exporta a chave bruta (`raw`) via `crypto.subtle.exportKey("raw", key)` e codifica em Base64URL seguro para URLs.
3. Envia o payload via `POST /api/pastes`:
   ```json
   {
     "title": "Documento Seguro",
     "content": "<base64_iv_plus_ciphertext>",
     "language": "python",
     "content_format": "aes-256-gcm",
     "burn_after_read": false,
     "expiration": "1d",
     "password": null
   }
   ```
4. Ao receber a resposta com `url: "http://.../p/<slug>"`, o cliente concatena a chave ao fragmento de hash:
   `share_url = data.url + "#" + exportedKeyBase64Url`.
5. O modal de sucesso exibe o link com `#key` e o aviso:
   *"Criptografado no navegador com AES-256-GCM. A chave de decifração reside unicamente após o '#' deste link e jamais foi enviada ao servidor. Se você perder este link completo, o paste não poderá ser recuperado."*

### 2.2 Decifração no Visualizador (`viewer.html` / `main.js`)
1. O leitor acessa `https://inkbin.com/p/<slug>#<key>`.
2. O servidor envia o HTML com o `content` cifrado. O servidor **não tem conhecimento da chave** pois o fragmento `#` não é transmitido via HTTP.
3. O script da página verifica `window.location.hash`:
   - Se presente: extrai a chave Base64URL, decodifica para buffer binário, importa via `crypto.subtle.importKey("raw", keyBytes, { name: "AES-GCM" }, false, ["decrypt"])`.
   - Decodifica o `content` Base64 recebido do servidor, separa os primeiros 12 bytes (IV) do restante (ciphertext + tag).
   - Decifra via `crypto.subtle.decrypt({ name: "AES-GCM", iv: iv }, key, ciphertext)`.
   - Decodifica para texto UTF-8 (`TextDecoder`).
   - Insere o texto limpo no elemento `<pre><code>` e aplica `hljs.highlightElement()`.
4. Se o fragmento `#key` estiver ausente ou a decifração falhar:
   - Exibe banner editorial de erro: *"Este paste foi criptografado no navegador pelo autor e requer a chave de decifração contida no link original completo (#chave). Sem a chave, o conteúdo não pode ser lido."*

---

## 3. Especificação do "Burn After Read"

### 3.1 Criação
- No formulário de criação, o usuário pode marcar a opção `[x] Destruir após leitura (Burn after read)`.
- Enviado como `burn_after_read: true` para a API.
- Pode ser combinado com qualquer política de expiração (ex: expira em 1 hora se nunca for lido, mas se for lido aos 10 minutos, é destruído imediatamente).

### 3.2 Interceptação e Tela Intermediária (*Interstitial Confirmation*)
Para evitar destruição involuntária por robôs (crawlers do Google, prévias do WhatsApp/Telegram/Slack):
1. **Requisição Web (`GET /p/<slug>`)**:
   - Se `paste.burn_after_read == True`:
     - O servidor **não entrega o conteúdo do paste nem o destrói**.
     - Renderiza a página `burn_confirmation.html` com aviso editorial:
       - Badge: `Destruição Após Leitura`
       - Título: `Este paste será destruído após a leitura`
       - Descrição: `O autor configurou este documento para ser expurgado permanentemente do servidor na primeira visualização confirmada. Deseja revelá-lo agora?`
       - Botão de ação: `[ Revelar e Destruir Paste ]`
2. **Confirmação e Expurgamento (`POST /p/<slug>/reveal` ou `GET /p/<slug>?confirm=1`)**:
   - O servidor verifica a existência e validade do paste.
   - Incrementa a contagem de visualizações.
   - Deleta fisicamente o registro da tabela `pastes` e remove chaves do Redis/Cache.
   - Retorna a página `viewer.html` renderizada com o conteúdo e uma mensagem de topo:
     *"Este documento foi expurgado permanentemente da base de dados. Qualquer tentativa futura de acesso retornará 404."*
3. **Acesso Posterior**:
   - Qualquer tentativa subsequente de acessar `/p/<slug>` retorna `404 Not Found`.

---

## 4. Especificação da Opção "Base64"

### 4.1 Criação
- Seletor de Modo de Formato: `Codificação Base64`.
- Texto codificado em Base64 padrão UTF-8 antes do upload, ou salvo com `content_format="base64"`.
- O formulário exibe aviso sutil: *"Base64 é uma codificação e não criptografia — qualquer pessoa com o link pode lê-lo."*

### 4.2 Visualização
- O visualizador renderiza o texto decodificado por padrão, com destaque de sintaxe da linguagem selecionada.
- No cabeçalho do código, exibe badge editorial: `[ Base64 Encoded ]`.
- Alerta informativo: *"Aviso: Este paste foi codificado em Base64. Lembre-se que Base64 é apenas codificação para transporte e não provê segurança criptográfica."*
- Botão de alternância: `[ Visualizar Decodificado ]` vs `[ Visualizar Base64 Bruto ]`.

---

## 5. Paridade e Internacionalização (i18n)

Todas as novas strings serão adicionadas com 100% de paridade em:
- `src/inkbin/locales/en.json`
- `src/inkbin/locales/pt-br.json`
- `src/inkbin/locales/cn.json`

Seções cobertas:
- Seletor de formato no editor (`format_mode`, `format_plaintext`, `format_aes_gcm`, `format_base64`).
- Checkbox e dica de Burn after read (`burn_after_read_label`, `burn_after_read_hint`).
- Tela intermediária de Burn after read (`burn.badge`, `burn.title`, `burn.description`, `burn.confirm_btn`, `burn.burned_notice`).
- Mensagens do cliente para AES-256-GCM (`crypto.missing_key`, `crypto.decryption_error`, `crypto.modal_notice`).
- Avisos e alternador do Base64 (`base64.badge`, `base64.notice`, `base64.view_decoded`, `base64.view_raw`).

---

## 6. Estratégia de Testes Automatizados

1. **Testes de Modelo e Migração (`test_models.py`, `test_migration.py`)**:
   - Criação de paste com `content_format` e `burn_after_read`.
   - Validação da migração de esquema sem perda de dados existentes.
2. **Testes de API e Validação Pydantic (`test_schemas.py`, `test_api.py`)**:
   - Validação de rejeição para valores inválidos de `content_format`.
   - Verificação dos campos retornados em `PasteCreateResponse` e `PasteDetailResponse`.
3. **Testes do Ciclo de Vida do Burn After Read (`test_burn_after_read.py`)**:
   - `GET /p/<slug>` retorna a tela intermediária de confirmação sem deletar o paste.
   - `POST /p/<slug>/reveal` retorna o conteúdo e expurga o paste do banco.
   - Segunda requisição retorna estritamente `404 Not Found`.
4. **Testes de Internacionalização (`test_i18n.py`)**:
   - Verificação de ausência de chaves faltantes entre `en.json`, `pt-br.json` e `cn.json`.
