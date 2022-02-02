import sys
sys.path.append('../')
sys.path.append('../app')
from app.mailpartsloader import LoadType, MailPartsLoaderFactory

csv_loader = MailPartsLoaderFactory.create(LoadType.CSV, **dict(
    mailfrom_idx = 0,
    mailto_idx = 1,
    subject_idx = 2,
    encoding = 'utf-8'
))

mailpartslist = csv_loader.load('/Users/givemewater/Repositories/python_mail/csvs/test.csv')

for mailparts in mailpartslist:
    print(mailparts.mail_from)
    print(mailparts.mail_to)
    print(mailparts.subject)
    print(mailparts.contents)