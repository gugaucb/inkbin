# 06: Diretrizes de Contribuição, Testes Automatizados e Licença

**What to build:** Inserir no README.md a seção de governança de comunidade open-source, estabelecendo o fluxo de trabalho para contribuidores, execução da suíte de testes com pytest, verificação de estilo de código com ruff, convenções de rastreamento de issues em `.scratch/` e detalhes da licença MIT.

**Blocked by:** 04: Guias de Execução Rápida, Docker e Configuração de Ambiente, 05: Guia de Uso via Terminal (cURL) e Referência da API REST

**Status:** resolved

- [x] Detalhar o fluxo de contribuição recomendado (criação de branch, boas práticas de commit, abertura de pull requests).
- [x] Documentar os comandos de execução de testes com `pytest` e cobertura de cenários.
- [x] Documentar a validação de linting e formatação de código com `ruff check .` e `ruff format --check .`.
- [x] Explicar a convenção de rastreamento local de especificações e tarefas em `.scratch/`.
- [x] Exibir a menção à Licença MIT com link para o arquivo `LICENSE` na raiz do repositório.

## Answer

Adicionadas ao `README.md`:
1. Seção "Desenvolvimento e Contribuição" com instruções passo a passo para clonagem, criação de branch de feature, instalação com `pip install -e ".[dev]"`.
2. Documentação da execução da suíte de 56 testes automatizados com `pytest`.
3. Instruções e comandos para checagem e formatação com `ruff check .` e `ruff format --check .`.
4. Explicação das convenções de governança do repositório com especificações e tarefas mantidas em arquivos Markdown locais sob `.scratch/`.
5. Seção de "Licença" com menção explícita à Licença MIT e link para o arquivo `LICENSE`.

