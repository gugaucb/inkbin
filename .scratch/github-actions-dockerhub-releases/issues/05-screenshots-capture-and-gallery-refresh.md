# 05 - Captura de Screenshots e Atualização da Galeria Visual

Status: open
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
