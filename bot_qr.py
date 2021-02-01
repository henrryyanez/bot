import os
import qrcode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction


INPUT_TEXT = 0 #modo de conversación Estado 0, está esperando que envíen el text
TOKEN=''

def start(update, context):

    update.message.reply_text(
        update.message.reply_text('Hola, bienvenido, que deseas hacer?\n\n Usa /qr para generar un código qr.')
    )


def qr_command_handler(update, context):

    update.message.reply_text('Envíame el texto para generarte un código QR.')

    return INPUT_TEXT


def generate_qr(text):

    filename = text + '.jpg'
    #hola.jpg

    img = qrcode.make(text)
    img.save(filename)

    return filename


def send_qr(filename, chat):

    #Hago que aparezca un status de Sending a Photo en el chat:
    chat.send_action(
        action = ChatAction.UPLOAD_PHOTO,
        timeout = None
    )

    chat.send_photo(
        photo = open(filename, 'rb')
    )

    os.unlink(filename) # Aqui borro el archivo generado despues de enviarlo al usuario


def input_text(update, context):

    text = update.message.text

    filename = generate_qr(text)

    chat = update.message.chat #veo el chat de esta conversación =  {'id': , 'type': '', 'username': '', 'first_name': '', 'last_name': ''}

    print(chat)

    send_qr(filename, chat)

    return ConversationHandler.END

if __name__ == '__main__':

    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },

        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()