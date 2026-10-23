<div align="center">

# `>_` INKBIN
### Editorial Pastebin & Anonymous Ephemeral Text Sharing

Plataforma open-source de alto desempenho e segura para publicação e compartilhamento anônimo de textos e trechos de código com URLs curtas e ofuscadas, seguindo o design system editorial INK.

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-000000?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-000000?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Database](https://img.shields.io/badge/Database-PostgreSQL_16_%7C_SQLite-000000?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Cache](https://img.shields.io/badge/Cache-Redis_7_%7C_In--Memory-000000?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Linter](https://img.shields.io/badge/Code_Style-Ruff-000000?style=for-the-badge&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/badge/Docker-Compose_Ready-000000?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-56_Passed-000000?style=for-the-badge&logo=pytest&logoColor=white)](tests)
[![License](https://img.shields.io/badge/License-MIT-000000?style=for-the-badge)](LICENSE)

<br>

[Galeria Visual](#-galeria-visual-e-demonstração) •
[Recursos](#-recursos-principais) •
[Início Rápido](#-início-rápido) •
[Variáveis de Ambiente](#-variáveis-de-ambiente) •
[Uso via Terminal (cURL)](#-guia-de-uso-via-terminal-curl) •
[API REST](#-referência-da-api-rest) •
[Arquitetura](#-arquitetura-e-estrutura) •
[Contribuição](#-desenvolvimento-e-contribuição)

</div>

---

## 📸 Galeria Visual e Demonstração

Interface gráfica construída sob as diretrizes do **INK Design System v2**, unindo tipografia editorial monocromática de alto contraste, alvos táteis confortáveis e ícones vetoriais Tabler Icons.

| Editor View | Viewer View |
| :---: | :---: |
| <img src="docs/assets/screenshots/editor-view.png" alt="Editor View" width="550"> | <img src="docs/assets/screenshots/viewer-view.png" alt="Viewer View" width="550"> |
| *Formulário de criação com seleção de linguagem, política de expiração, senha e contadores em tempo real.* | *Visualizador de código com cabeçalho de metadados, contagem de visualizações, ações rápidas e destaque de sintaxe.* |

| Modal de Confirmação & Admin Delete Token | Desafio de Senha (Security Gate) |
| :---: | :---: |
| <img src="docs/assets/screenshots/admin-delete-modal.png" alt="Admin Delete Modal" width="550"> | <img src="docs/assets/screenshots/password-challenge.png" alt="Password Challenge" width="550"> |
| *Modal pós-criação apresentando a URL pública e a chave secreta irrecuperável de exclusão permanente.* | *Tela de desafio para Protected Pastes, requerendo a credencial criptografada antes de descriptografar e exibir o conteúdo.* |

---
