# 02: Integração do Serviço Caddy com Docker Compose Profiles

**What to build:**
Adicionar o serviço `caddy` no arquivo `docker-compose.yml` utilizando a imagem leve `caddy:2-alpine`, montando os volumes persistentes de dados e configuração, expondo as portas 80 e 443 sob o perfil `profiles: ["production"]`. Garantir que o container da aplicação `app` permaneça acessível internamente pelo Caddy e que o comando padrão `docker compose up` continue funcionando normalmente para desenvolvimento sem subir o Caddy.

**Blocked by:** 01: Caddyfile com Configuração Dinâmica para Produção e Rede Local

**Status:** closed

- [x] Serviço `caddy` adicionado ao `docker-compose.yml` com `profiles: ["production"]`.
- [x] Mapeamento das portas `80:80` e `443:443`.
- [x] Volumes `caddy_data` e `caddy_config` declarados e montados para retenção dos certificados ACME.
- [x] Dependência do serviço `app` configurada para inicialização ordenada.
- [x] `docker compose config` valida sem erros sintáticos com e sem o profile `production`.
