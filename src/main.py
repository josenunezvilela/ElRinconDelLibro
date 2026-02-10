import os
import logging
import sys
from dotenv import load_dotenv
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,filters, MessageHandler,CallbackQueryHandler
from api import buscar_libros_lista, obtener_detalle_libro

# 1. Configuración de Logs (Para ver qué pasa en la consola si algo falla)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# 2. Cargar el Token desde el archivo .env
load_dotenv() # Esto carga las variables del archivo .env
TOKEN = os.getenv('TELEGRAM_TOKEN')


#FUNCIONES QUE RESPONDEN A COMANDOS
#=======COMANDO /start=======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 ¡Hola! Soy tu bibliotecario personal.\n\n🔎 Usa /buscar [nombre] para ver libros.\n⬇️ Usa /download [nombre_exacto] para bajar archivos de tu PC."
    )
    
#======COMANDO /buscar=========
async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Por favor, escribe el nombre del libro.\nEjemplo: /buscar El Principito"
        )
        return
    consulta = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    libros = buscar_libros_lista(consulta)
    
    if not libros:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ No encontré nada.")
        return

    teclado=[]
    for libro in libros:
        dato_oculto = f"info_{libro['id']}"
        boton = InlineKeyboardButton(text=f"{libro['titulo']} ({libro['autor']})", callback_data=dato_oculto)
        teclado.append([boton]) # Ponemos cada botón en una fila nueva
    
    reply_markup=InlineKeyboardMarkup(teclado)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📚 He encontrado {len(libros)} resultados para: *{consulta}*\nToca uno para ver la descripción:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    ) 

#=======MANEJADOR DE CLICS DE LOS BOTONES=====
async def botones_handler(update:Update, context: ContextTypes.DEFAULT_TYPE):
    # Esto se ejecuta cuando tocas un botón
    query = update.callback_query
    await query.answer() # Avisar a Telegram que recibimos el clic (para quitar el relojito)
    
    data = query.data # Aquí viene "info_ID12345"
    
    if data.startswith("info_"):
        libro_id = data.split("_")[1] # Sacamos el ID limpio
        detalle = obtener_detalle_libro(libro_id)
        
        # Editamos el mensaje original con la descripción
        await query.edit_message_text(text=detalle, parse_mode="Markdown")

#=======COMANDO /help=========
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra una lista de los comandos disponibles"""
    texto_ayuda = (
        "🤖 *Comandos Disponibles:*\n\n"
        "🟢 /start - Inicia el bot\n"
        "🔎 /buscar [nombre] - Busca un libro en Google Books\n"
        "❓ /help - Muestra este mensaje de ayuda"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=texto_ayuda,
        parse_mode="Markdown"
    )

#Bloque que arranca el bot y maneja los comandos 
if __name__ == '__main__':
    # Verificar que el token existe
    if not TOKEN:
        print("Error: No se encontró el TOKEN en el archivo .env")
        exit()

    # Construir la aplicación
    application = ApplicationBuilder().token(TOKEN).build()

    #Añadimos los handler 
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('buscar', buscar))
    application.add_handler(CommandHandler('help',help_command))
    
    print("El bot se está iniciando...")
    application.run_polling()

