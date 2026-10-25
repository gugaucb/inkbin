# 01: Caddyfile com Configuração Dinâmica para Produção e Rede Local

**What to build:**
Criar o arquivo `Caddyfile` na raiz do projeto com template dinâmico que atenda tanto produção com domínio público (emissão automática de certificados Let's Encrypt / ZeroSSL) quanto rede local com CA interna (`tls internal`). Deve incluir cabeçalhos essenciais de segurança e proxy reverso para o container `app:8000`.

**Blocked by:** None (can start immediately).

**Status:** closed

- [x] Arquivo `Caddyfile` criado na raiz do repositório.
- [x] Configuração com suporte à interpolação de variáveis `{$DOMAIN:localhost}` e `{$ACME_EMAIL}`.
- [x] Suporte à variável `{$TLS_MODE:internal}` permitindo injetar `tls internal` para testes em IP/LAN local ou email para Let's Encrypt automático em domínio público.
- [x] Encaminhamento reverso transparente (`reverse_proxy app:8000`) com headers de `X-Forwarded-*`.
