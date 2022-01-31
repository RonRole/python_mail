import sys
import json
import app.mailitems

settings_json = open('settings.json', 'r')
settings = json.load(settings_json)

SMTP_SERVER = settings['smtpserver']
SMTP_PORT = settings['smtpport']
MAIL_ACCOUNT = settings['mail_account']
MAIL_PASSWORD = settings['mail_password']

args = sys.argv
CSV_FILE_NAME = args[1]

mail_account_info = app.mailitems.MailAccountInfo(
    smtpserver = SMTP_SERVER, 
    smtpport   = SMTP_PORT, 
    account    = MAIL_ACCOUNT, 
    password   = MAIL_PASSWORD
)

mailserver = app.mailitems.MailServer(mail_account_info)

with open(CSV_FILE_NAME, encoding='utf-8') as f:
    csv_lines = f.readlines()
    mailpartslist = app.mailitems.MailParts.load_csv_lines(csv_lines)
    for mailparts in mailpartslist:
        mailserver.send(mailparts)

