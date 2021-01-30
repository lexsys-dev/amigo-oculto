import email.message
import mimetypes
import os.path
import smtplib

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
    gmail_user = 'vincenthimmel@gmail.com'
    gmail_pwd = ')a-*%)-5~Q63FS['
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail_server.login(gmail_user, gmail_pwd)
    mail_server.send_message(message)
    mail_server.quit()
