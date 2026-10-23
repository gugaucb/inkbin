# 02: Desbloqueio por Senha, Sessão por Cookie e Proteção contra Força Bruta

**What to build:** O leitor de um Paste protegido pode submeter a senha na tela de desafio ou via endpoint. A validação correta emite um cookie de sessão assinado (`inkbin_unlocked_{slug}`) válido por 24 horas, liberando o texto completo, syntax highlighting e rota `/raw/{slug}`. Tentativas incorretas decrementam as chances restantes; após 5 falhas consecutivas para o mesmo IP e slug, o sistema impõe bloqueio temporário de 15 minutos com HTTP 429.

**Blocked by:** 01: Criação de Paste Protegido por Senha com Argon2id

**Status:** ready-for-agent

- [ ] Endpoint `POST /api/pastes/{slug}/unlock` e formulário web para validação de senha.
- [ ] Comparação criptográfica segura de senha contra o hash Argon2id armazenado.
- [ ] Emissão de cookie seguro `inkbin_unlocked_{slug}` assinado com HMAC (atributos `HttpOnly`, `SameSite=Lax`, `Secure` em produção) com TTL de 24 horas.
- [ ] Presença do cookie válido libera automaticamente a visualização do paste na web e na rota `/raw/{slug}` sem repetição de senha.
- [ ] Contador atômico de tentativas de autenticação no Redis com chave por `{slug}:{client_ip}` e expiração móvel de 900s.
- [ ] Retorno de mensagem informativa com número de tentativas restantes em caso de senha incorreta.
- [ ] Aplicação de bloqueio por 15 minutos após 5 erros, retornando HTTP 429 com cabeçalho `Retry-After`.
- [ ] Testes automatizados cobrem desbloqueio correto, persistência da sessão por cookie, contagem de falhas e ativação do lockout por 15 minutos.
