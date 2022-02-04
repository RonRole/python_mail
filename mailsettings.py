import app
import json

settings_json = open('settings.json', 'r')
settings = json.load(settings_json)

SMTP_SERVER = settings['smtpserver']
SMTP_PORT = settings['smtpport']
MAIL_ACCOUNT = settings['mail_account']
MAIL_PASSWORD = settings['mail_password']

mail_account_info = app.MailAccountInfo(
    smtpserver = SMTP_SERVER, 
    smtpport   = SMTP_PORT, 
    account    = MAIL_ACCOUNT, 
    password   = MAIL_PASSWORD
)

def get_mailserver():
    mailserver = app.MailServer(mail_account_info)
    return mailserver


