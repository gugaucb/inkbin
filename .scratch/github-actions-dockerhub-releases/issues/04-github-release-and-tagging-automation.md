# 04 - Automação de Versionamento e GitHub Releases

Status: open
Type: task
Blocked by: 03

## Question

Como estruturar o controle de versões, automação de GitHub Releases e sincronização com tags `vX.Y.Z` (`.github/workflows/release.yml`), gerando changelog automático a partir de commits e permitindo disparo via tag push (`git push origin vX.Y.Z`) ou acionamento manual (`workflow_dispatch`)?

## Scope

1. Criar `.github/workflows/release.yml` acionado quando uma tag `v*.*.*` é enviada ou via `workflow_dispatch` com input da versão.
2. Utilizar `softprops/action-gh-release@v2` para criar a release oficial no GitHub associada à tag correspondente.
3. Habilitar geração automática de changelog / release notes (`generate_release_notes: true`).
4. Definir documentação/instruções claras no repositório sobre como criar e enviar tags Git locais para gerar novas versões (ex: `git tag v0.1.0 && git push origin v0.1.0`).
