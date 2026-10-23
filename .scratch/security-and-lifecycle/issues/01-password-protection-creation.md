# 01: Criação de Paste Protegido por Senha com Argon2id

**What to build:** O criador anônimo pode definir opcionalmente uma senha (de 4 a 50 caracteres) no formulário ou na chamada de API ao publicar um Paste. O sistema gera um hash criptográfico seguro com Argon2id (ou bcrypt cost 12), define o registro como protegido (`is_protected: true`) e assegura a imutabilidade do conteúdo. Ao acessar a URL pública ou `/raw/{slug}`, qualquer visitante não autenticado é interceptado por uma tela ou resposta de desafio de senha no estilo INK, sem que o conteúdo confidencial seja exposto.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Campo opcional de senha disponível na API (`POST /api/pastes`) e no formulário de criação com validação de 4 a 50 caracteres.
- [ ] Senha armazenada com hash seguro Argon2id em `password_hash`; a senha em texto plano jamais é salva ou exposta em logs e respostas.
- [ ] Resposta da API de criação retorna `is_protected: true` e omite o hash de senha.
- [ ] Acesso à URL pública (`GET /{slug}`) de um Paste protegido sem credenciais renderiza a tela editorial de desafio de senha do INK Design System.
- [ ] Acesso à rota bruta (`GET /raw/{slug}`) de um Paste protegido sem autenticação prévia retorna status HTTP 401/403.
- [ ] Tentativas de modificação pós-criação são categoricamente rejeitadas mantendo a imutabilidade estrita.
- [ ] Testes automatizados cobrem a criação com senha válida, validação de limites de caracteres e restrição de acesso público inicial.
