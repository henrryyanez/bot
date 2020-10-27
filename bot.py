import logging
import os
import telegram
import random
from telegram.ext import Updater, CommandHandler

#Configurar Logging
logging.basicConfig(
    level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

#Solicitamos el TOKEN
TOKEN = os.getenv("TOKEN")


def iniciar(update, context):
    """
    docstring
    """
    logging.info(f"El usuario {update.effective_user['username']}, ha iniciado una conversación")
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot.")



def random_number(update, context):
    user_id = update.effective_user['id']
    logger.info(f"El usuario {user_id}, ha solicitado un numero aleatorio")
    number = random.randint(1, 200)
    context.bot.sendMessage(chat_id= user_id, parse_mode="HTML", text= f"<b>Número</b> aleatorio:\n{number}")


if __name__ == "__main__":
    # Obtenemos información del bot
    my_bot = telegram.Bot(token = TOKEN)
    #print(my_bot.getMe())

# Enlazamos nuestro updater con nuestro bot
updater = Updater(my_bot.token, use_context=True)

# Creamos un despachador
dp = updater.dispatcher

# Creamos los manejadores
dp.add_handler(CommandHandler("iniciar", iniciar))

dp.add_handler(CommandHandler("random", random_number))


updater.start_polling()
print("[*] BOT CARGADO")
updater.idle() #Permite finalizar el bot con Ctrl + C