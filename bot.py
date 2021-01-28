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
/amigos - adiciona amigos ao sorteio
/apagar - apaga toda a lista de amigos
/sorteio - recebe nomes e entrega o resultado do sorteio
"""

amigos = []

def start(update, context):
  """Send a message when the command /start is issued."""
  update.message.reply_text(text = START_TEXT)
def help(update, context):
  """Send a message when the command /help is issued."""
  update.message.reply_text(HELP_TEXT)
def echo(update, context):
  """Echo the user message."""
  update.message.reply_text(update.message.text)
def amigos(update, context):
    update.message.reply_text("Envie o nome de cada amigo ou digite 'parar' para encerrar o programa :")
    get_name = []
    get_name.append(update.message.text)
    if "parar" not in get_name:
        for i in get_name:
            friends.append(i)
def secret_santa(update, context):
    update.message.reply_text("O resultado do sorteio é: ")
    rand_friends = random.shuffle(amigos)
    rand_friends.append(rand_friends[0])
    gift_dict = {}
    for i in range(len(rand_friends) - 1):
        gift_dict[rand_friends[i]] = rand_friends[i+1]
    for k in gift_dict:
        update.message.reply_text(f'{k} presentei-a {gift_dict[k]}')
def put(update, context):
    """Usage: /put value"""
    # Generate ID and seperate value from command
    #key = str(uuid4())
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]
    lst = list(value.split(" "))
    key = lst[0]
    emailF = lst[1]
    # Store value
    context.user_data[key] = emailF
    # Send the key to the user
    update.message.reply_text(key + " foi adicionado a lista de amigos.")

def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = context.args[0]

    # Load value and send it to the user
    value = context.user_data.get(key, 'Not found')
    update.message.reply_text(context.user_data)
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
  dp.add_handler(CommandHandler("sorteio", secret_santa))
  dp.add_handler(CommandHandler("put", put))
  dp.add_handler(CommandHandler("get", get))
  dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@lexsys')))
  # In noncommand i.e message - echo the message on Telegram
  dp.add_handler(MessageHandler(Filters.text, echo))
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
