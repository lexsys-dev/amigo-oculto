#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program dedicated to the public domain under the CC0 license.

"""Bot para sortear amigos e ajudar na troca de presentes entre si
"""

import os
import logging
import re
import random
import sys
import string
import requests

from uuid import uuid4
from threading import Thread
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from bs4 import BeautifulSoup
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
START_TEXT = 'Bot para ajudar a sortear uma lista de amigos ocultos'
HELP_TEXT = """
Lista de comandos:
/help - Apresenta esta lista
/add - adiciona amigos ao sorteio
/apagar - apaga toda a lista de amigos
/sorteio - recebe nomes e entrega o resultado do sorteio
/lista - apsenta todos os amigos ja colocados na lista
"""

amigos = []

def start(update, context):
  """Send a message when the command /start is issued."""
  update.message.reply_text(text = START_TEXT)
def help(update, context):
  """Send a message when the command /help is issued."""
  update.message.reply_text(HELP_TEXT)
def add(update, context):
    """Usage: /add friends name"""
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]
    lst = (value.split(" "))
    key = lst[0]
    emailF = lst[1]
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,emailF)):
        # Store value in dict user_data
        context.user_data[key] = emailF
        # Send the key to the user
        update.message.reply_text(key + " agora esta na lista de amigos para o sorteio.")
    else:
        update.message.reply_text(emailF + " bota um email certo ai")

def lista(update, context):
    """Usage: /lista uuid"""
    # Seperate ID from command
    #key = context.args[0]
    # Load value and send it to the user
    #value = context.user_data.get(key, 'Not found')
    lista = 'Aqui estao todos os amigos que participam do sorteio: '
    for i in context.user_data.items():
        lista += f'{i}\n'
    update.message.reply_text(lista)
def sorteio(update, context):
    """Usage: /sorteio uuid"""
    lst = []
    for k,v in context.user_data.items():
        lst.append(k)
    random.shuffle(lst)
    lst.append(lst[0])
    gift_dict = {}
    for i in range(len(context.user_data)):
            gift_dict[lst[i]] = lst[i+1]
    for k in gift_dict:
        update.message.reply_text(f'{k} presenteia {gift_dict[k]}')    
# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater("1679932632:AAH01E9PBfHBKHYkkm2sLnr4gyYd23ET5Uo")

def stop_and_restart():
  """Gracefully stop the Updater and replace the current process with a new one"""
  updater.stop()
  os.execl(sys.executable, sys.executable, *sys.argv)

def restart(update, context):
  update.message.reply_text('Bot is restarting...')
  Thread(target=stop_and_restart).start()

def error(update, context):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
  """Start the bot."""
  # Create the Updater and pass it your bot's token.
  # Make sure to set use_context=True to use the new context based callbacks
  # Post version 12 this will no longer be necessary

  # Get the dispatcher to register handlers
  dp = updater.dispatcher

  # On different commands - answer in Telegram
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("help", help))
  dp.add_handler(CommandHandler("add", add))
  dp.add_handler(CommandHandler("lista", lista))
  dp.add_handler(CommandHandler("sorteio", sorteio))
  dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@lexsys')))
  # log all errors
  dp.add_error_handler(error)

  # Start the Bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()


if __name__ == '__main__':
  main()
