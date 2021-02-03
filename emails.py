import email.message
import mimetypes
import os.path
import smtplib
from configparser import ConfigParser

#Load configuration from config.ini

cfg = ConfigParser()
cfg.read("config.ini")
userinfo = cfg["USERINFO"]
serverinfo = cfg["SERVERCONFIG"]

def generate(sender, recipient, subject, body):
    """Creates an email with an attachement."""
    # Basic Email formatting
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["subject"] = subject
    message.set_content(body)

    return message

def send(message):
    """Sends the message to the confidured SMTP server."""
    mail_server = smtplib.SMTP_SSL(serverinfo["smtp_server"], serverinfo["port"])
    mail_server.login(userinfo["loginid"], userinfo["password"])
    mail_server.send_message(message)
    mail_server.quit()
