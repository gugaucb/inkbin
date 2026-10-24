# Map: GitHub Actions, Docker Hub & Release Management

## Destination

Pipeline de CI/CD automatizado via GitHub Actions para build e publicação multi-arquitetura (`linux/amd64`, `linux/arm64`) no Docker Hub (`gugaucb/inkbin`), automação de versionamento semântico gerando tags e GitHub Releases correspondentes, atualização de `docker-compose.yml` para consumo da imagem oficial, captura de screenshots atualizados da UI com as novas features e atualização completa dos três READMEs (`README.md`, `README.pt-BR.md`, `README.zh-CN.md`).

## Notes

- **Domínio**: DevOps, CI/CD, GitHub Actions, Docker Hub, SemVer e Documentação Técnica.
- **Repositório GitHub**: `gugaucb/inkbin` (branch principal: `main`).
- **Repositório Docker Hub**: `gugaucb/inkbin` (secrets configuradas no GitHub: `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`).
- **Modo de execução**: *Execution carried into the map* — este esforço governa as decisões e a implementação direta dos workflows de actions, arquivos de configuração, screenshots e documentação.
- **Skills relevantes**: `architecture-patterns`, `codebase-design`, `writing-for-agents`.

## Decisions so far

- 01: [01-docker-compose-image-and-build-integration.md](issues/01-docker-compose-image-and-build-integration.md) — Configurado `docker-compose.yml` com `image: gugaucb/inkbin:${INKBIN_IMAGE_TAG:-latest}` e preservado bloco `build: .` para desenvolvimento local.
- 02: [02-ci-testing-and-linting-workflow.md](issues/02-ci-testing-and-linting-workflow.md) — Configurado `.github/workflows/ci.yml` com Python 3.11, cache pip, validação com Ruff e Pytest em pushes e PRs para a `main`.
- 03: [03-dockerhub-multiarch-publish-workflow.md](issues/03-dockerhub-multiarch-publish-workflow.md) — Configurado `.github/workflows/docker-publish.yml` para publicação multi-arch (`linux/amd64`, `linux/arm64`) no Docker Hub com tags semânticas e cache GHA.
- 04: [04-github-release-and-tagging-automation.md](issues/04-github-release-and-tagging-automation.md) — Implementado workflow `.github/workflows/release.yml` com release notes automáticos e criado guia em `docs/release-guide.md`.
- 05: [05-screenshots-capture-and-gallery-refresh.md](issues/05-screenshots-capture-and-gallery-refresh.md) — Capturados 5 screenshots em alta fidelidade demonstrando a nova barra de opções, criptografia no navegador, QR code e telas de confirmação.

## Not yet specified

- **Notificação e Deploy Contínuo Automatizado**: Caso desejado no futuro, configurar webhook ou runner SSH para auto-deploy em servidor de produção quando uma nova release for publicada no Docker Hub.
- **Assinatura Criptográfica de Imagens (Cosign/Sigstore)**: Assinatura das imagens publicadas no Docker Hub e emissão de atestado de proveniência / SBOM para segurança da cadeia de suprimentos.
- **Categorização Automática de Changelog via Release Drafter**: Agrupamento visual refinado de notas de lançamento por labels (`feature`, `bugfix`, `security`).

## Out of scope

- Publicação de pacote Python no PyPI (o Inkbin é uma aplicação/serviço autocontido para self-hosting em Docker, não uma biblioteca).
- Configuração de charts de Kubernetes / Helm (o escopo de orquestração oficial é focado em Docker Compose).
- Alterações em regras de negócio ou refatoração de endpoints da API (o escopo é estritamente infraestrutura, automação de release e documentação).
