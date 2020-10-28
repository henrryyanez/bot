import logging
import os
import telegram
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#Configurar Logging
logging.basicConfig(
    level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

#Solicitamos el TOKEN
#TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No especificó un MODO!")
    sys.exit(1)



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


def echo(update, context):
    user_id = update.effective_user['id']
    logger.info(f"El usuario {user_id}, ha enviado un mensaje de texto.")
    text = update.message.text
    context.bot.sendMessage(
        chat_id = user_id,
        parse_mode = "MarkdownV2",
        text = f"*Escribiste:*\n_{text}_"
    )
        


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
    dp.add_handler(MessageHandler(Filters.text, echo))

    run(updater)

    updater.start_polling()
    print("[*] BOT CARGADO")
    updater.idle() #Permite finalizar el bot con Ctrl + C