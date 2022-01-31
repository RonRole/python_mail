import smtplib
import email

class MailAccountInfo:
    def __init__(smtpserver, smtpport, account, password):
        self.smtpserver = smtpserver
        self.smtpport = smtpport
        self.account = account
        self.password = password

class MailParts:
    def __init__(self, mail_from, mail_to, contents):
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.contents = contents

    def load_csv_lines(csv_lines):
        address_contents_dict = {}
        for csv_line in csv_lines:
            mail_from, mail_to, contents = csv_line.split(',')
            if (mail_from, mail_to) in address_contents_dict:
                address_contents_dict[(mail_from, mail_to)] += contents
            else:
                address_contents_dict[(mail_from,mail_to)] = contents
        return list(map(lambda key: MailParts(key[0], key[1], address_contents_dict[key]), address_contents_dict))

class MailServer:
    def __init__(self, mail_account_info):
        self.smtpobj = smtplib.SMTP_SSL(mail_account_info.smtpserver, mail_account_info.smtpport)
        self.account = mail_account.info.account
        self.password = mail_account.info.password


    def send(mailparts):
        msg = email.mime.text.MIMEText(mailparts.contents)
        msg['From'] = mailparts.mail_from
        msg['To'] = mailparts.mail_to
        smtpobj.send_message()













    











