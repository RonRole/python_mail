import sys
import json
import mailsettings

mailserver = mailsettings.get_mailserver()
mailpartsloader = app.mailpartsloader.MailPartsLoaderFactory.create(app.mailpartsloader.LoadType.CSV_FILE, **dict(
    mailfrom_idx = 0,
    mailto_idx = 1,
    subject_idx = 2,
    contents_idx = 3,
    encoding = 'utf-8'
))

args = sys.argv
CSV_FILE_NAME = args[1]

mailpartslist = mailpartsloader.load(CSV_FILE_NAME).group_by_address_and_subject()
for mailparts in mailpartslist:
    mailserver.send(mailparts)

