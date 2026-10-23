# 06 - Documentação Multilíngue do Repositório (READMEs en, pt-BR e zh-CN)

Status: open
Type: task
Blocked by: 03, 04, 05

## Question

Como estruturar as versões em múltiplos idiomas da documentação oficial do Inkbin, tornando o `README.md` em inglês o padrão principal e provendo versões completas em português do Brasil e chinês simplificado com navegação rápida no topo?

## Scope

1. Atualizar e traduzir o arquivo principal `README.md` para o inglês (`en`), tornando-o canônico e alinhado aos padrões internacionais da comunidade open-source.
2. Criar `README.pt-BR.md` contendo a versão completa em português brasileiro, incorporando a nova variável `EXPIRATION_OPTIONS`, o seletor de idiomas e as funções de histórico local.
3. Criar `README.zh-CN.md` contendo a versão completa em chinês simplificado (简体中文).
4. Inserir no topo de cada um dos três arquivos de documentação uma barra de navegação de idiomas:
   ```markdown
   <div align="center">
     🌐 <b>Languages / Idiomas / 语言</b>:
     <a href="README.md">English</a> •
     <a href="README.pt-BR.md">Português (Brasil)</a> •
     <a href="README.zh-CN.md">简体中文</a>
   </div>
   ```
5. Atualizar tabelas de variáveis de ambiente e comandos de exemplo do Docker em todos os READMEs para refletir `EXPIRATION_OPTIONS`.
