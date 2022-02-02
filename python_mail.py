import sys
import json
import app

settings_json = open('settings.json', 'r')
settings = json.load(settings_json)

SMTP_SERVER = settings['smtpserver']
SMTP_PORT = settings['smtpport']
MAIL_ACCOUNT = settings['mail_account']
MAIL_PASSWORD = settings['mail_password']

mail_account_info = app.mailserver.MailAccountInfo(
    smtpserver = SMTP_SERVER, 
    smtpport   = SMTP_PORT, 
    account    = MAIL_ACCOUNT, 
    password   = MAIL_PASSWORD
)

mailserver = app.mailserver.MailServer(mail_account_info)
mailpartsloader = app.mailpartsloader.MailPartsLoaderFactory.create(app.mailpartsloader.LoadType.CSV, **dict(
    mailfrom_idx = 0,
    mailto_idx = 1,
    subject_idx = 2,
    encoding = 'utf-8'
))

args = sys.argv
CSV_FILE_NAME = args[1]

mailpartslist = mailpartsloader.load(CSV_FILE_NAME).group_by_address_and_subject()
for mailparts in mailpartslist:
    mailserver.send(mailparts)

