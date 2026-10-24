# 04 - Automação de Versionamento e GitHub Releases

Status: resolved
Type: task
Blocked by: 03

## Question

Como estruturar o controle de versões, automação de GitHub Releases e sincronização com tags `vX.Y.Z` (`.github/workflows/release.yml`), gerando changelog automático a partir de commits e permitindo disparo via tag push (`git push origin vX.Y.Z`) ou acionamento manual (`workflow_dispatch`)?

## Scope

1. Criar `.github/workflows/release.yml` acionado quando uma tag `v*.*.*` é enviada ou via `workflow_dispatch` com input da versão.
2. Utilizar `softprops/action-gh-release@v2` para criar a release oficial no GitHub associada à tag correspondente.
3. Habilitar geração automática de changelog / release notes (`generate_release_notes: true`).
4. Definir documentação/instruções claras no repositório sobre como criar e enviar tags Git locais para gerar novas versões (ex: `git tag v0.1.0 && git push origin v0.1.0`).

## Answer

Implementada a automação completa de versionamento e GitHub Releases:
- Criado `.github/workflows/release.yml` acionado automaticamente no push de tags `v*.*.*` e manualmente via `workflow_dispatch` com permissão `contents: write`.
- Integração da action oficial `softprops/action-gh-release@v2` com `generate_release_notes: true` para geração automatizada do changelog a partir dos commits.
- Criada documentação técnica em `docs/release-guide.md` detalhando as convenções SemVer, o ciclo de disparo sincronizado com o workflow do Docker Hub e o passo a passo para criação e publicação de tags Git pelo terminal ou interface web.
