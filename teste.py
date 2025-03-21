import requests
import base64
import io
from PIL import Image
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import os

# Read token directly from .env file
def read_env_file():
    with open('.env', 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if key.strip() == 'TELEGRAM_TOKEN1':
                    return value.strip().strip('"').strip("'")
    return None

TELEGRAM_TOKEN = read_env_file()
GROUP_A_ID = -4744392705  # substitua pelo ID real do Grupo A
GROUP_B_ID = -4632787658  # substitua pelo ID real do Grupo B
CANAL_A_ID = -1002340793709
CANAL_B_ID = -1002509946887
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_NAME = 'gemma3:latest'  # Fixed typo

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the chat ID when receiving any message."""
    chat_id = update.effective_chat.id
    chat_title = update.effective_chat.title if update.effective_chat.title else "Private Chat"
    await update.message.reply_text(f"Chat ID: {chat_id}\nChat Title: {chat_title}")
    print(f"Message received from {chat_title} (ID: {chat_id})")

async def get_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Captura e exibe o ID do canal quando qualquer mensagem é recebida."""
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title if update.effective_chat.title else "Chat Privado"
    
    if chat_type == "channel":
        # Apenas imprime no console, sem responder no canal para não poluir
        print(f"Mensagem recebida no canal {chat_title} (ID: {chat_id})")
        # Opcionalmente, você pode descomentar a linha abaixo se quiser que o bot responda no canal
        # await update.message.reply_text(f"ID do Canal: {chat_id}\nNome do Canal: {chat_title}")
    else:
        # Para outros tipos de chat, apenas registra no console
        print(f"Mensagem recebida em um {chat_type} (ID: {chat_id}, Nome: {chat_title})")
        # Opcionalmente, você pode descomentar a linha abaixo se quiser que o bot responda
        # await update.message.reply_text(f"ID: {chat_id}\nTipo: {chat_type}\nNome: {chat_title}")

async def handle_message(update: Update, context):
    print(f"Received message from chat ID: {update.message.chat_id}")
    if update.message.chat_id == GROUP_A_ID:
        message_text = update.message.text
        payload = {
            'model': MODEL_NAME,
            'prompt': message_text,
            'stream': False
        }
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            generated_text = result['response']
            await context.bot.send_message(chat_id=GROUP_B_ID, text=generated_text)
        else:
            print(f"Error from Ollama: {response.status_code}")

async def handle_channel_message(update: Update, context):
    print(f"Received message from channel ID: {update.effective_chat.id}")
    if update.effective_chat.id == CANAL_A_ID:
        message_text = update.effective_message.text
        payload = {
            'model': MODEL_NAME,
            'prompt': message_text,
            'stream': False
        }
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            generated_text = result['response']
            await context.bot.send_message(chat_id=CANAL_B_ID, text=generated_text)
        else:
            print(f"Error from Ollama: {response.status_code}")

async def handle_channel_photo(update: Update, context):
    print(f"Received photo from channel ID: {update.effective_chat.id}")
    if update.effective_chat.id == CANAL_A_ID:
        # Determine if the photo is in message or channel_post
        if update.channel_post and update.channel_post.photo:
            photo_container = update.channel_post
        elif update.message and update.message.photo:
            photo_container = update.message
        else:
            print("No photo found in update")
            return
        
        # Get the photo with the highest resolution
        photo = photo_container.photo[-1]
        
        # Download the photo
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        # Convert the photo to base64
        base64_image = base64.b64encode(photo_bytes).decode('utf-8')
        
        # Create a prompt asking for a description of the image
        prompt = "Please describe this image in detail."
        
        # Prepare payload for Ollama API with the image
        payload = {
            'model': MODEL_NAME,
            'prompt': prompt,
            'stream': False,
            'images': [base64_image]
        }
        
        try:
            # Send the request to Ollama API
            response = requests.post(OLLAMA_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result['response']
                
                # Forward the generated description to Canal B
                await context.bot.send_message(chat_id=CANAL_B_ID, text=generated_text)
            else:
                error_message = f"Error from Ollama API: {response.status_code}"
                print(error_message)
                # Optionally, you can send an error notification to Canal B
                await context.bot.send_message(chat_id=CANAL_B_ID, text="Failed to process the image.")
        
        except Exception as e:
            error_message = f"Exception while processing photo: {str(e)}"
            print(error_message)
            # Optionally, you can send an error notification to Canal B
            await context.bot.send_message(chat_id=CANAL_B_ID, text="An error occurred while processing the image.")

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable not set")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handler to respond with chat ID for any message
    # application.add_handler(MessageHandler(filters.ALL, get_chat_id))
    
    # Adiciona handler para capturar IDs de canais em qualquer mensagem
    # application.add_handler(MessageHandler(filters.ALL, get_channel_id))
    
    # Mantém o handler para o comando /channel_id para compatibilidade
    # application.add_handler(CommandHandler("channel_id", get_channel_id))
    
    print("Bot iniciado! Processando mensagens entre grupos e canais.")
    # Ativa o handler para processar mensagens do Grupo A para o Grupo B
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=GROUP_A_ID), handle_message))
    
    # Ativa o handler para processar mensagens do Canal A para o Canal B
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=CANAL_A_ID), handle_channel_message))
    
    # Ativa o handler para processar fotos do Canal A para o Canal B
    application.add_handler(MessageHandler(filters.PHOTO & filters.Chat(chat_id=CANAL_A_ID), handle_channel_photo))
    
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("Bot stopped by user")

if __name__ == '__main__':
    main()