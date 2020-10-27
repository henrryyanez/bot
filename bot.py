import logging
import os
from telegram.ext import Updater

#Configurar Logging
logging.basicConfig(
    level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

#Solicitamos el TOKEN
TOKEN = os.getenv("TOKEN")
print(TOKEN)