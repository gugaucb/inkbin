# 06 - Atualização dos Readmes Multilíngues e Badges de Release

Status: resolved
Type: task
Blocked by: 01, 04, 05

## Question

Como atualizar a documentação multilíngue (`README.md`, `README.pt-BR.md`, `README.zh-CN.md`) incluindo os novos badges de Docker Hub e GitHub Release, atualizando as instruções de Quickstart para execução da imagem oficial `gugaucb/inkbin:latest`, atualizando as tabelas da galeria com os novos screenshots e adicionando o guia de publicação e releases?

## Scope

1. Adicionar badges estilizados oficiais no cabeçalho dos 3 READMEs:
   - Badge do Docker Hub apontando para `https://hub.docker.com/r/gugaucb/inkbin`
   - Badge da última Release no GitHub apontando para `https://github.com/gugaucb/inkbin/releases`
2. Atualizar a seção **Visual Gallery** com os screenshots novos capturados no ticket 05, garantindo legendas e referências precisas.
3. Atualizar a seção **Quickstart** para documentar:
   - Execução direta da imagem oficial via `docker pull gugaucb/inkbin:latest` e `docker run` / `docker compose up -d`.
   - Como utilizar o `docker-compose.yml` sem necessidade de clonar o código fonte ou compilar.
4. Adicionar seção de **Release & Versioning Guide** explicando como criar tags e disparar releases.
5. Garantir consistência terminológica e estilística em inglês (`README.md`), português (`README.pt-BR.md`) e chinês simplificado (`README.zh-CN.md`).
6. Atualizar o grafo de conhecimento com `graphify update .`.

## Answer

Atualização completa e multilíngue realizada nos três READMEs (`README.md`, `README.pt-BR.md` e `README.zh-CN.md`):
- Incluídos os novos badges estilizados de `Docker Hub` (`gugaucb/inkbin`) e `Release` (`v0.1.0`) seguindo a paleta monocromática do INK Design System v2.
- Atualizado o sumário (TOC) com âncora para o novo Guia de Releases.
- Seção **Visual Gallery** reformulada com 5 capturas de tela atualizadas (`editor-view.png` com barra de opções e marcadores ciano, `admin-delete-modal.png` com QR Code renderizado, `viewer-view.png`, `password-challenge.png` e `burn-after-read-interstitial.png`).
- Seção **Quickstart** expandida para destacar como Opção 1 a execução imediata da imagem oficial publicada via `docker run` ou `docker compose up -d` com download direto do `docker-compose.yml`, além de manter a compilação local (Opção 2) e o ambiente SQLite local (Opção 3).
- Adicionada seção dedicada **Release & Versioning Guide** explicando o padrão SemVer, automação multi-arquitetura e comandos `git tag` / `git push`.
- Grafo de conhecimento sincronizado com sucesso via `graphify update .`.
