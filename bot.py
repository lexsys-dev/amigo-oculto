#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program dedicated to the public domain under the CC0 license.

"""Bot para sortear amigos e ajudar na troca de presentes entre si.
Utiliza emails para informar os resultados.
"""

import os
import logging
import re
import random
import sys
import emails

from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from bs4 import BeautifulSoup
from configparser import ConfigParser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
START_TEXT = """Para comecar você pode adicionar um amigo a sua lista de sorteio 
eviando-me o comando /add amigo amigo@email.com ou se precisar de ajuda envie /ajuda""" 
HELP_TEXT = """
Olá! Sou um bot criado para ajudá-lo a sortear um Amigo Oculto.
Fui criado para incluir os amigos que ainda não tem uma conta no Telegram,
por isso vou precisar que me diga qual email seu amigo(a) utiliza,
dessa forma vou poder lhes enviar o resultado.

Aqui estão todos os comandos que posso executar:
/ajuda - Apresenta esta lista
/add - Adiciona amigos ao sorteio. Ex.: /add amigo amigo@example.com
/apagar - Remove um amigo da lista. Ex.: /apagar amigo
/sorteio - Realiza o sorteio e informa os participantes
/lista - Apresenta todos os amigos ja colocados na lista de sorteio
"""
def start(update, context):
  """Send a message when the command /start is issued."""
  update.message.reply_text(text = START_TEXT)
def help(update, context):
  """Send a message when the command /help is issued."""
  update.message.reply_text(HELP_TEXT)
def add(update, context):
    """Usage: /add friend friend@example.com"""
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]
    lst = list(value.split(" "))
    key = lst[0]
    emailF = lst[1]
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,emailF)):
        # Store value in dict user_data
        context.user_data[key] = emailF
        # Send the key to the user
        update.message.reply_text(key + " agora está na lista de amigos para o sorteio.")
    else:
        update.message.reply_text(emailF + " Este email parece-me incorreto, tente novamente.")

def lista(update, context):
    """Usage: /lista uuid"""
    if bool(context.user_data) is False:
        update.message.reply_text("Ainda não há ninguém em sua lista, você pode adicionar alguém enviando-me o comando /add amigo amigo@example.com")
    else:
        lista = 'Aqui estão todos os amigos que participam do sorteio:\n'
        for i in context.user_data.items():
            lista += f'{i}\n'
        update.message.reply_text(lista)
def rand_friends(update,context):
    lst = []
    gift_dict = {}
    try:
        for k,v in context.user_data.items():
            lst.append(k)
        random.shuffle(lst)
        lst.append(lst[0])
        for i in range(len(context.user_data)):
            gift_dict[lst[i]] = lst[i+1]
        return gift_dict
    except:
        return gift_dict 
def sorteio(update, context):
    """Usage: /sorteio uuid"""
    sorteados = rand_friends(update, context)
    if bool(sorteados) is False:
        update.message.reply_text('Você não adicionou nenhum amigo a sua lista. :(')
    else:
        update.message.reply_text(f'Ok! Estes são os particpantes do amigo oculto: ')
        for k in sorteados:
            update.message.reply_text(f'{sorteados[k]}\n')
        update.message.reply_text('Para enviar um email a todos os amigos basta me dar o seguinte comando: /enviar')
def send_email(update, context):
    """Send an email for each friend with results and erase friends list"""
    dictF = rand_friends(update, context)
    chat_user_client = update.message.from_user.username
    try:
        for k in dictF:
            if k in context.user_data:
                sender = 'AmigoBot'
                recipient = context.user_data[k]
                subject = "Seu amigo oculto foi escolhido."
                body = f"""Olá {k},\n
                {chat_user_client} adicionou seu email ao grupo para participar do Amigo Oculto!\n
            
                E o seu amigo secreto é: {dictF[k]}\n
            
                Por favor, não responda a este email. Sou apenas um bot e não sei dar maiores informações.
                Você também pode criar o próprio sorteio, basta falar comigo aqui: https://telegram.me/migocultobot
                Se quiser falar mais sobre este sorteio pode enviar uma mensagem para https://telegram.me/{chat_user_client}"""
                update.message.reply_text(f'E-mail enviado à {k}')
                message = emails.generate(sender, recipient, subject, body)
                emails.send(message)
                del context.user_data[k]
        if bool(recipient) is True:
            update.message.reply_text("""Ok! Enviei um e-mail a todos, descubra quem irá presentear em sua caixa de emails.
Uma vez que o sorteio já foi realizado, agora vou limpar a sua /lista
Se precisar fazer um novo sorteio conte comigo.
Ah! Antes que me esqueça o meu e-mail é migsoculto@gmail.com""")
    except:
        update.message.reply_text("Não há e-mails à enviar, para adicionar participantes ao sorteio use o comando /add") 
def apagar(update, context):
    rem_friend = context.args[0]
    if rem_friend is None:
        update.message.reply_text("Diga-me qual amigo deseja remover da lista de sorteio: /apagar amigo")
    else:
        if rem_friend in context.user_data:
            del context.user_data[rem_friend]
            update.message.reply_text(rem_friend + " foi removido da lista de sorteio.")
        else:
            update.message.reply_text(rem_friend + " não está na lista de amigos. É mesmo este nome?")

# Load configuration from config.ini

cfg = ConfigParser()
cfg.read("config_mig.ini")
token = cfg["BOT ACCESS"]["token"]

# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(token)

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
  dp.add_handler(CommandHandler("ajuda", help))
  dp.add_handler(CommandHandler("add", add))
  dp.add_handler(CommandHandler("lista", lista))
  dp.add_handler(CommandHandler("sorteio", sorteio))
  dp.add_handler(CommandHandler("apagar", apagar))
  dp.add_handler(CommandHandler("enviar", send_email))
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

