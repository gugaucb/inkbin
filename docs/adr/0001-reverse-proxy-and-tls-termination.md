# Terminação TLS com Caddy e Let's Encrypt via Docker Profiles

Contexto: A plataforma Inkbin requer comunicação segura (HTTPS) para habilitar recursos essenciais no navegador via Web Crypto API (cifragem no cliente com AES-256-GCM) em acessos externos ou de rede local. Decidimos adotar o **Caddy** como o proxy reverso oficial em container isolado, acionado via Docker Profiles (`COMPOSE_PROFILES=production`), em vez de acoplar certificados ou ACME diretamente na aplicação FastAPI/Uvicorn ou usar Nginx com containers auxiliares de Certbot.

## Considerações e Alternativas
- **Uvicorn com SSL direto**: Rejeitado pois acopla a aplicação a privilégios de rede (portas 80/443) e exige gerenciamento de ciclo de vida de certificados no código da aplicação, violando o princípio de responsabilidade única.
- **Nginx + Certbot**: Rejeitado pela complexidade operacional de manter dois containers adicionais, volumes compartilhados para desafios `.well-known/acme-challenge` e scripts de cron para renovação periódica.
- **Caddy (`caddy:2-alpine`)**: Selecionado por conter suporte nativo a Let's Encrypt / ZeroSSL com renovação automática sem cron, configuração concisa via `Caddyfile` dinâmico e Autoridade Certificadora embutida (`tls internal`) para desenvolvimento HTTPS em rede local (LAN).

## Consequências
- A aplicação Python/FastAPI permanece estritamente como servidor HTTP interno na porta 8000.
- Em desenvolvimento simples, `docker compose up` expõe a porta 8000 diretamente sem Caddy.
- Para deploys atrás de proxies reversos externos (Traefik, Nginx, Cloudflare Tunnel, AWS ALB) ou ambientes autônomos sem Caddy, utiliza-se `docker-compose.standalone.yml` (`docker compose -f docker-compose.standalone.yml up -d`), garantindo ausência total de volumes e portas do Caddy.
- Quando o Caddy integrado for desejado, ele é ativado via perfis Docker dedicados (`COMPOSE_PROFILES=caddy`, `proxy` ou `production`) no `.env` ou via CLI (`docker compose --profile caddy up -d`).
