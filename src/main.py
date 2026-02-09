import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# 1. Configuración de Logs (Para ver qué pasa en la consola si algo falla)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. Cargar el Token desde el archivo .env
load_dotenv() # Esto carga las variables del archivo .env
TOKEN = os.getenv('TELEGRAM_TOKEN')

# 3. Definir la función que responde al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Esta función se ejecuta cuando alguien escribe /start
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="¡Hola! Soy El Rincón del Libro 📚. Estoy listo para ayudarte a encontrar tu próxima lectura."
    )

# 4. El bloque principal que arranca el bot
if __name__ == '__main__':
    # Verificar que el token existe
    if not TOKEN:
        print("Error: No se encontró el TOKEN en el archivo .env")
        exit()

    # Construir la aplicación
    application = ApplicationBuilder().token(TOKEN).build()

    # Añadir el "manejador" del comando start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Encender el bot
    print("El bot se está iniciando...")
    application.run_polling()
    