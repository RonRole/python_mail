import json
import sys
sys.path.append('../')
import app

#設定ファイルからapp内クラスのインスタンスを生成するfactory的な箇所
class SettingsToMailServer(object):
    #required full path of "settings.json"
    def load(fullpath_settings_json):
        settings_json = open(fullpath_settings_json, 'r')
        settings = json.load(settings_json)
        mail_account_settings = settings['mail']
        SMTP_SERVER   = mail_account_settings['smtpserver']
        SMTP_PORT     = mail_account_settings['smtpport']
        MAIL_ACCOUNT  = mail_account_settings['mail_account']
        MAIL_PASSWORD = mail_account_settings['mail_password']
        mail_account_info = app.MailAccountInfo(
            smtpserver = SMTP_SERVER, 
            smtpport   = SMTP_PORT, 
            account    = MAIL_ACCOUNT, 
            password   = MAIL_PASSWORD
        )
        return app.MailServer(mail_account_info)