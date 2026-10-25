# Especificação Técnica: Camada de Proxy Reverso, TLS e Let's Encrypt para Produção e Rede Local

**Status**: Aprovado  
**Data**: 2026-10-24  
**Local**: `.scratch/reverse-proxy-and-tls/spec.md`  

---

## Problem Statement

Atualmente, o Inkbin expõe a aplicação diretamente via HTTP na porta `8000:8000`. Recursos criptográficos fundamentais (cifragem simétrica com AES-256-GCM no cliente via Web Crypto API) dependem de um *Secure Context* (`window.isSecureContext === true`). Ao acessar a aplicação em rede local (ex: via IP `192.168.x.x` em smartphones ou outros computadores da LAN) ou ao implantar em servidores de produção acessíveis pela internet, a ausência de terminação HTTPS nativa impede a utilização de recursos criptográficos de segurança e exige configurações manuais complexas de certificados.

Além disso, desenvolvedores e administradores que utilizam orquestradores de containers (como Portainer, Docker Compose ou Docker Swarm) necessitam de uma forma padronizada e automatizada de ativar HTTPS público via Let's Encrypt em produção sem quebrar ou engessar o ambiente de desenvolvimento local.

## Solution

Adotar o **Caddy** (`caddy:2-alpine`) como o proxy reverso oficial e desacoplado do Inkbin, integrado ao `docker-compose.yml` através de perfis do Docker (`profiles: ["production"]` ou variável `COMPOSE_PROFILES=production`):

1. **Produção**: O Caddy escuta nas portas públicas `80` e `443`, obtém e renova certificados SSL/TLS automaticamente via Let's Encrypt / ZeroSSL (ACME) para o domínio informado em `DOMAIN`, e repassa as requisições internamente para o serviço `app:8000` via rede Docker privada.
2. **Rede Local (LAN) e Homologação**: O `Caddyfile` dinâmico suporta a diretiva `tls internal`, gerando certificados com autoridade certificadora própria do Caddy para permitir testes com HTTPS em IPs locais (ex: `192.168.15.8`), destravando o *Secure Context* e a Web Crypto API em dispositivos móveis e máquinas da rede.
3. **Desenvolvimento Padrão**: O comando usual `docker compose up` sem o profile de produção continua subindo a aplicação de forma leve e direta na porta `8000`, sem ocupar as portas 80/443 do host.
4. **Compatibilidade com Portainer**: Usuários do Portainer podem ativar a terminação TLS completa apenas declarando `COMPOSE_PROFILES=production` na tela de variáveis de ambiente da Stack.

---

## User Stories

1. Como administrador de sistema, quero implantar o Inkbin em um servidor de produção com suporte automático a Let's Encrypt, para que todas as comunicações sejam cifradas com HTTPS sem necessidade de configurar cron jobs ou certbot manualmente.
2. Como usuário acessando o Inkbin por um smartphone na rede Wi-Fi local, quero que a aplicação possa operar sobre HTTPS, para que o navegador reconheça o contexto como seguro e libere a cifragem no navegador (AES-256-GCM).
3. Como desenvolvedor rodando o Inkbin localmente, quero iniciar os serviços essenciais via `docker compose up` sem que portas privilegiadas (80 e 443) sejam ocupadas no meu computador.
4. Como operador que gerencia stacks no Portainer, quero poder ativar o proxy reverso com Let's Encrypt apenas definindo a variável `COMPOSE_PROFILES=production`, para que o deploy em ambientes gerenciados seja declarativo e direto.
5. Como administrador, quero que o Caddy redirecione automaticamente todo o tráfego HTTP da porta 80 para HTTPS na porta 443, para garantir que nenhum dado trafegue em texto puro.
6. Como criador de paste, quero que as URLs públicas geradas pelo Inkbin contenham o esquema `https://` e o domínio público correto, para que links compartilhados abram diretamente com segurança.

---

## Implementation Decisions

1. **Proxy Reverso com Caddy**:
   - Imagem: `caddy:2-alpine`.
   - Volumes persistentes: `caddy_data` (armazena certificados emitidos e chaves privadas) e `caddy_config` (armazena metadados de configuração).
   - Mapeamento de portas: `80:80` e `443:443`.
2. **Caddyfile Dinâmico**:
   - Arquivo `Caddyfile` na raiz do projeto com interpolação de variáveis de ambiente:
     - `{$DOMAIN:localhost}`
     - `{$TLS_CONFIG:}`
     - `reverse_proxy app:8000`
   - Inclusão de cabeçalhos de segurança (Strict-Transport-Security, X-XSS-Protection, X-Frame-Options) e repasse transparente de headers (`X-Forwarded-For`, `X-Forwarded-Proto`, `Host`).
3. **Docker Compose Profiles**:
   - O serviço `caddy` pertence a `profiles: ["production"]`.
   - Em produção, a porta pública do `app` é restrita a `127.0.0.1:8000` ou interna, forçando todo o tráfego a passar pelo Caddy.
4. **Variáveis de Ambiente**:
   - Adição ao `.env.example`:
     - `COMPOSE_PROFILES=production` (opcional, ativa Caddy)
     - `DOMAIN=paste.example.com`
     - `ACME_EMAIL=admin@example.com`
     - `TLS_CONFIG=` (vazio para Let's Encrypt público, ou `tls internal` para rede local)
5. **Documentação e Guias**:
   - Atualização do `README.md` (e versões pt-BR / zh-CN) com seção clara sobre "Produção e HTTPS com Caddy / Portainer".

---

## Testing Decisions

- Testar sintaxe e validação do `Caddyfile` via `caddy validate --config Caddyfile` (ou execução em container).
- Testar a subida de containers via `docker compose --profile production config` para validar a sintaxe e a interpolação das variáveis.
- Testar o comportamento do backend (`routes/api.py`) garantindo que headers de proxy reverso (`X-Forwarded-Proto: https` e `Host`) sejam respeitados na geração de URLs.
- Garantir que a suíte completa de testes (`pytest`) permaneça 100% verde.

---

## Out of Scope

- Gerenciamento de registros DNS externos ou zonas de DNS dinâmico (Route53, Cloudflare API tokens, etc.).
- Modificação do código core de negócios do Inkbin para lidar com criptografia de transporte (mantendo a separação estrita de camadas).
