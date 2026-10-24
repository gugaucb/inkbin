# 06 - Atualização dos Readmes Multilíngues e Badges de Release

Status: open
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
