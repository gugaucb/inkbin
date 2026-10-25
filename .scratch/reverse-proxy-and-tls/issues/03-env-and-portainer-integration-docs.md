# 03: Variáveis de Ambiente e Documentação para Portainer e Produção

**What to build:**
Atualizar os arquivos `.env.example`, `.env` e a documentação do projeto (`README.md`, `README.pt-BR.md`) com as novas variáveis e instruções passo a passo para deploy em produção via linha de comando ou via Portainer Stacks utilizando `COMPOSE_PROFILES=production`.

**Blocked by:** 02: Integração do Serviço Caddy com Docker Compose Profiles

**Status:** closed

- [x] Variáveis `COMPOSE_PROFILES`, `DOMAIN`, `ACME_EMAIL` e `TLS_MODE` adicionadas ao `.env.example` com comentários explicativos.
- [x] Seção documentando o deploy em Produção com Let's Encrypt no `README.md` e `README.pt-BR.md`.
- [x] Guia específico de deploy no Portainer (explicando como configurar `COMPOSE_PROFILES=production` na interface web).
- [x] Instruções claras sobre como testar HTTPS na rede local usando `tls internal` ou a flag do navegador.
