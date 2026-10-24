# 01 - Integração de Imagem e Build no Docker Compose

Status: resolved
Type: task
Blocked by: none

## Question

Como configurar o `docker-compose.yml` para consumir a imagem oficial `gugaucb/inkbin:${INKBIN_IMAGE_TAG:-latest}` do Docker Hub permitindo execução imediata via `docker compose up -d` sem compilação local, mantendo simultaneamente a diretiva `build: .` para desenvolvedores locais?

## Scope

1. Atualizar o serviço `app` em `docker-compose.yml` para adicionar a declaração `image: gugaucb/inkbin:${INKBIN_IMAGE_TAG:-latest}`.
2. Manter a diretiva `build: { context: ., dockerfile: Dockerfile }` intacta para que comandos com `--build` continuem funcionando perfeitamente em desenvolvimento.
3. Garantir que as variáveis de ambiente, volumes e dependências com `db` e `redis` permaneçam íntegras.
4. Validar o arquivo com `docker compose config` no terminal.

## Answer

Configuração concluída com sucesso no `docker-compose.yml`. O serviço `app` agora declara `image: gugaucb/inkbin:${INKBIN_IMAGE_TAG:-latest}` em conjunto com o bloco `build: { context: ., dockerfile: Dockerfile }`. Dessa forma, o comando `docker compose up -d` pode baixar e executar diretamente a imagem oficial publicada no Docker Hub, enquanto desenvolvedores locais podem continuar construindo a imagem local via `docker compose up --build`. A integridade sintática e funcional foi verificada via `docker compose config`.
