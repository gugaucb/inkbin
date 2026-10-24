# 01 - Integração de Imagem e Build no Docker Compose

Status: open
Type: task
Blocked by: none

## Question

Como configurar o `docker-compose.yml` para consumir a imagem oficial `gugaucb/inkbin:${INKBIN_IMAGE_TAG:-latest}` do Docker Hub permitindo execução imediata via `docker compose up -d` sem compilação local, mantendo simultaneamente a diretiva `build: .` para desenvolvedores locais?

## Scope

1. Atualizar o serviço `app` em `docker-compose.yml` para adicionar a declaração `image: gugaucb/inkbin:${INKBIN_IMAGE_TAG:-latest}`.
2. Manter a diretiva `build: { context: ., dockerfile: Dockerfile }` intacta para que comandos com `--build` continuem funcionando perfeitamente em desenvolvimento.
3. Garantir que as variáveis de ambiente, volumes e dependências com `db` e `redis` permaneçam íntegras.
4. Validar o arquivo com `docker compose config` no terminal.
