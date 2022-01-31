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


#user
python_mail = PythonMail(some_settings)
python_mail.load_csv(csv_file_name, mailfrom_idx = 0, mailto_idx = 1, contents_idx = 2)
python_mail.send()











