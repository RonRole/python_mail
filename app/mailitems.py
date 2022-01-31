import smtplib
import email.mime.text
import functools 

class MailAccountInfo:
    def __init__(self, smtpserver, smtpport, account, password):
        self.smtpserver = smtpserver
        self.smtpport = smtpport
        self.account = account
        self.password = password

class MailParts:
    def __init__(self, mail_from, mail_to, subject='', contents=''):
        self.mail_from = mail_from
        self.mail_to   = mail_to
        self.subject   = subject
        self.contents  = contents

    def load_csv_lines(csv_lines):
        address_contents_dict = {}
        for csv_line in csv_lines:
            mail_from, mail_to, subject, contents = csv_line.split(',')
            address_keys = (mail_from, mail_to, subject)
            address_contents_dict[address_keys] = address_contents_dict.get(address_keys, '') + contents
        return list(map(lambda keys: MailParts(mail_from = keys[0], mail_to = keys[1], subject = keys[2], contents = address_contents_dict[keys]), address_contents_dict))

class MailServer:
    def __init__(self, mail_account_info):
        self.mail_account_info = mail_account_info

    def send(self, mailparts):
        msg = email.mime.text.MIMEText(mailparts.contents)
        msg['Subject'] = mailparts.subject
        msg['From'] = mailparts.mail_from
        msg['To'] = mailparts.mail_to
        smtpobj = smtplib.SMTP_SSL(self.mail_account_info.smtpserver, self.mail_account_info.smtpport)
        smtpobj.login(self.mail_account_info.account, self.mail_account_info.password)
        smtpobj.send_message(msg)
        smtpobj.quit()