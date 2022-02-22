import smtplib
import email.mime.text

class MailAccountInfo:
    def __init__(self, smtpserver, smtpport, account, password):
        self.smtpserver = smtpserver
        self.smtpport = smtpport
        self.account = account
        self.password = password

class MailServer:
    def __init__(self, mail_account_info):
        self.__mail_account_info = mail_account_info
        self.__smtpobj = smtplib.SMTP_SSL(
            self.__mail_account_info.smtpserver, 
            self.__mail_account_info.smtpport
        )

    def __enter__(self):
        self.__smtpobj.login(
            self.__mail_account_info.account, 
            self.__mail_account_info.password
        )

    def __exit__(self, ex_type, ex_value, trace):
        self.__smtpobj.quit()

    def send(self, mailparts):
        msg = email.mime.text.MIMEText(mailparts.contents)
        msg['Subject'] = mailparts.subject
        msg['From'] = mailparts.mail_from
        msg['To'] = mailparts.mail_to
        self.__smtpobj.send_message(msg)