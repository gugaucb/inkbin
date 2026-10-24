# 05 - Captura de Screenshots e Atualização da Galeria Visual

Status: resolved
Type: task
Blocked by: none

## Question

Como capturar screenshots atualizados de alta resolução cobrindo o Editor com as novas opções (criptografia cliente, barra de expiração, formato, burn-after-read), o Visualizador, o Modal de confirmação com QR Code e a tela de confirmação de exclusão permanente, salvando os novos assets em `docs/assets/screenshots/`?

## Scope

1. Iniciar a aplicação Inkbin localmente com ambiente limpo.
2. Utilizar ferramentas de browser/automação para capturar imagens nítidas (proporção e contraste refinados sob o INK Design System v2):
   - `editor-view.png`: Formulário principal exibindo a barra de opções, marcadores ciano, opções de expiração e formato.
   - `viewer-view.png`: Visualizador de código com cabeçalho de metadados, botões com Tabler Icons e realce de sintaxe.
   - `admin-delete-modal.png`: Modal pós-criação com link curto, token de exclusão de administrador e componente de QR Code renderizado.
   - `password-challenge.png` ou `burn-after-read-interstitial.png`: Telas de proteção de acesso e confirmação de visualização única.
3. Otimizar e salvar as imagens em `docs/assets/screenshots/`.

## Answer

Capturados e validados 5 screenshots de alta fidelidade e resolução (device scale 1.5) sob o INK Design System v2 salvos em `docs/assets/screenshots/`:
1. `editor-view.png`: Formulário principal com código Python, opções dinâmicas ativas (AES-256-GCM, Burn after read), marcadores pontilhados ciano `#00d4b8` e contadores de caracteres/bytes em tempo real.
2. `admin-delete-modal.png`: Modal de sucesso pós-criação com banner de criptografia de cliente, short URL, token secreto de administração e componente de QR Code renderizado para escaneamento móvel.
3. `viewer-view.png`: Leitor de código com sintaxe Bash destacada, cabeçalho de metadados e botões de ação enriquecidos com Tabler Icons.
4. `password-challenge.png`: Tela de segurança com badge `PASSWORD PROTECTED` e formulário de desafio de credenciais.
5. `burn-after-read-interstitial.png`: Tela de confirmação e aviso de ação irreversível para destruição imediata após leitura.
O script reutilizável de captura foi versionado em `scripts/capture_screenshots.py`.
