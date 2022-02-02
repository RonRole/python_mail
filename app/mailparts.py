class MailParts:
    def __init__(self, mail_from, mail_to, subject='', contents=''):
        self.mail_from = mail_from
        self.mail_to   = mail_to
        self.subject   = subject
        self.contents  = contents
