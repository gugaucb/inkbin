# 03 - Workflow de Publicação Multi-Arquitetura no Docker Hub

Status: resolved
Type: task
Blocked by: 02

## Question

Como implementar o workflow `.github/workflows/docker-publish.yml` no GitHub Actions para autenticar no Docker Hub via `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`, compilar imagens multi-arquitetura (`linux/amd64`, `linux/arm64`) via QEMU e Buildx com cache GHA, e publicar tags `latest`, `vX.Y.Z` e `X.Y.Z` em releases, e `edge` em pushes na `main`?

## Scope

1. Criar `.github/workflows/docker-publish.yml` com gatilhos para:
   - Tags no padrão `v*.*.*`
   - Pushes na branch `main`
   - Disparo manual via `workflow_dispatch`
2. Configurar `docker/setup-qemu-action@v3` e `docker/setup-buildx-action@v3`.
3. Autenticar no Docker Hub usando `docker/login-action@v3` com as secrets `secrets.DOCKERHUB_USERNAME` e `secrets.DOCKERHUB_TOKEN`.
4. Utilizar `docker/metadata-action@v5` para extrair e gerar tags semânticas canônicas:
   - Em tag `v1.2.3`: gera `latest`, `1.2.3` e `v1.2.3`.
   - Em push na `main`: gera `edge`.
5. Compilar e publicar com `docker/build-push-action@v6` suportando as plataformas `linux/amd64,linux/arm64` com cache GitHub Actions (`cache-from: type=gha`, `cache-to: type=gha,mode=max`).

## Answer

Implementado o workflow `.github/workflows/docker-publish.yml` atendendo a todos os requisitos:
- Gatilhos configurados para pushes na `main`, envio de tags semânticas `v*.*.*` e acionamento manual `workflow_dispatch`.
- Setup de emulação multi-arquitetura via `docker/setup-qemu-action@v3` e `docker/setup-buildx-action@v3`.
- Autenticação segura contra o Docker Hub com `secrets.DOCKERHUB_USERNAME` e `secrets.DOCKERHUB_TOKEN`.
- Extração de tags canônicas via `docker/metadata-action@v5` (`edge` para pushes na `main`, `latest`, `{{version}}`, `v{{version}}` para tags SemVer).
- Compilação e publicação multi-arch para as plataformas `linux/amd64` e `linux/arm64` com cache acelerado GitHub Actions (`type=gha`, `mode=max`).
