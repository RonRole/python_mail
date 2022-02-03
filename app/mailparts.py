class MailParts:
    def __init__(self, mail_from, mail_to, subject='', contents=''):
        self.mail_from = mail_from
        self.mail_to   = mail_to
        self.subject   = subject
        self.contents  = contents

class MailPartsList:
    def __init__(self, *mailparts):
        self.__mailpartslist = list(mailparts)

    def all(self):
        return self.__mailpartslist

    def group_by_address_and_subject(self):
        address_contents_dict = {}
        for mailparts in self.__mailpartslist:
            unique_keys = (
                mailparts.mail_from,
                mailparts.mail_to,
                mailparts.subject
            )
            contents = mailparts.contents
            address_contents_dict[unique_keys] = address_contents_dict.get(unique_keys, '') + contents
        return list(
            map(
                lambda keys: MailParts(
                    mail_from = keys[0], 
                    mail_to = keys[1], 
                    subject = keys[2], 
                    contents = address_contents_dict[keys]
                ), address_contents_dict)
            )

