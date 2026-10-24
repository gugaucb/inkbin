# Inkbin

Plataforma open-source de alto desempenho e segura para publicação e compartilhamento anônimo de textos e trechos de código com URLs curtas e ofuscadas, seguindo o design system editorial INK.

## Language

**Inkbin**:
Nome canônico da plataforma open-source de compartilhamento de texto e código.
_Avoid_: TextEditor, PastebinApp, PasteService

**Anonymous Creation**:
Processo de publicação de paste sem exigência de conta ou autenticação prévia de usuário.
_Avoid_: Guest post, criação pública não logada

**Paste**:
Registro compartilhado contendo texto ou código-fonte publicado, com título opcional, linguagem de programação e política de expiração.
_Avoid_: Snippet, post, documento, texto

**Slug**:
Identificador alfanumérico curto (6 a 8 caracteres em Base62) e não sequencial que compõe a URL pública única de acesso ao paste.
_Avoid_: ID sequencial, hashid, código de acesso, alias

**Admin Delete Token**:
Chave de segurança única gerada no ato da criação anônima que confere ao criador anônimo a permissão irrevogável de excluir seu paste permanentemente.
_Avoid_: Senha de admin, delete key, link secreto

**Protected Paste**:
Paste cuja visualização requer validação de senha (armazenada com hash Argon2/bcrypt), sujeito a bloqueio temporário após 5 tentativas incorretas.
_Avoid_: Paste privado, paste trancado

**Expiration Policy**:
Regra parametrizável (via configuração de ambiente `EXPIRATION_OPTIONS`) que determina os períodos de retenção permitidos para um paste (ex: 1 hora, 1 dia, 1 semana, 1 mês ou nunca), disparando sua remoção física ao expirar.
_Avoid_: TTL, tempo de vida, prazo

**Locale**:
Identificador canônico do idioma e convenções regionais ativas na interface (`en`, `pt-br`, `cn`), com fallback padrão para inglês (`en`) e persistido via cookie `inkbin_locale`.
_Avoid_: Language code, dialect, idioma local

**Client-Side Encryption**:
Processo de cifragem simétrica com AES-256-GCM executado integralmente no navegador do autor via Web Crypto API antes do envio, onde a chave secreta reside exclusivamente no fragmento da URL (`#key`) e nunca é transmitida ou armazenada no servidor.
_Avoid_: Server-side encryption, criptografia em repouso, chave de servidor

**Burn After Read**:
Política de retenção e descarte permanente em que o paste é fisicamente expurgado após a primeira visualização confirmada pelo leitor, resguardada por uma tela intermediária de confirmação para impedir consumo involuntário por rastreadores e pré-visualizadores de links.
_Avoid_: Auto-delete, leitura efêmera desprotegida, one-time link sem confirmação

**Base64 Encoding**:
Formato de transformação e representação textual que não provê segurança criptográfica, acompanhado de aviso editorial transparente e alternância entre conteúdo decodificado e bruto.
_Avoid_: Criptografia Base64, encriptação leve, cifra Base64


