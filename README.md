# Bot AI Telegram

Um bot de Telegram que processa mensagens e imagens entre canais e grupos usando o modelo Ollama para geração de texto e descrição de imagens.

## Funcionalidades

- **Processamento de Texto**: Encaminha mensagens de texto de um canal/grupo para outro, processando-as através do modelo Ollama.
- **Processamento de Imagens**: Analisa imagens enviadas em um canal e gera descrições detalhadas usando o modelo Ollama, encaminhando essas descrições para outro canal.
- **Identificação de Chats**: Funções para identificar IDs de chats, grupos e canais do Telegram.

## Requisitos

- Python 3.7+
- Biblioteca python-telegram-bot
- Pillow (PIL)
- Requests
- Ollama rodando localmente

## Instalação

1. Clone o repositório:
   ```
   git clone [URL_DO_REPOSITÓRIO]
   cd botaitelegram
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` com seu token do Telegram:
   ```
   TELEGRAM_TOKEN1=seu_token_aqui
   ```

## Configuração

1. **Token do Telegram**: Obtenha um token do BotFather no Telegram e adicione-o ao arquivo `.env`.

2. **IDs de Canais e Grupos**: Substitua os IDs de exemplo no código pelos IDs reais dos seus canais e grupos:
   ```python
   GROUP_A_ID = -4744392705  # substitua pelo ID real do Grupo A
   GROUP_B_ID = -4632787658  # substitua pelo ID real do Grupo B
   CANAL_A_ID = -1002340793709
   CANAL_B_ID = -1002509946887
   ```

3. **Ollama**: Certifique-se de que o Ollama está rodando localmente na URL padrão:
   ```
   http://localhost:11434/api/generate
   ```

4. **Modelo**: O bot está configurado para usar o modelo `gemma3:latest`. Você pode alterar para outro modelo disponível no Ollama modificando a variável `MODEL_NAME`.

## Uso

1. Inicie o bot:
   ```
   python teste.py
   ```

2. O bot começará a monitorar as mensagens e imagens no Canal A e encaminhará as respostas processadas para o Canal B.

### Comandos Disponíveis

O código inclui funções para obter IDs de chats e canais, que podem ser ativadas descomentando as linhas apropriadas no método `main()`:

- Para obter o ID de qualquer chat: Descomente a linha com `application.add_handler(MessageHandler(filters.ALL, get_chat_id))`
- Para obter o ID de canais: Descomente a linha com `application.add_handler(MessageHandler(filters.ALL, get_channel_id))`

## Funcionalidades Detalhadas

### Processamento de Texto

O bot captura mensagens de texto do Grupo A ou Canal A, envia o texto para o modelo Ollama para processamento, e então encaminha a resposta gerada para o Grupo B ou Canal B, respectivamente.

### Processamento de Imagens

Quando uma imagem é enviada no Canal A, o bot:
1. Baixa a imagem
2. Converte para base64
3. Envia para o Ollama com um prompt solicitando uma descrição detalhada
4. Encaminha a descrição gerada para o Canal B

## Arquitetura

O bot utiliza a biblioteca `python-telegram-bot` para interagir com a API do Telegram e a biblioteca `requests` para se comunicar com a API do Ollama. A estrutura principal inclui:

- Handlers para diferentes tipos de mensagens (texto e imagens)
- Funções para processar e encaminhar conteúdo entre canais/grupos
- Integração com o modelo Ollama para geração de texto e análise de imagens

## Solução de Problemas

- **Erro de Token**: Verifique se o arquivo `.env` está configurado corretamente e se o token é válido.
- **Erro de Conexão com Ollama**: Certifique-se de que o Ollama está rodando localmente na porta padrão.
- **Permissões de Bot**: Verifique se o bot tem permissões adequadas nos canais e grupos configurados.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.