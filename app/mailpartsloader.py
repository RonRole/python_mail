import sys
import enum
from .mailparts import MailParts, MailPartsList

class LoadType(enum.Enum):
    CSV = enum.auto()        

class MailPartsLoaderFactory:
    def create(loadtype, **settings):
        if loadtype == LoadType.CSV:
            return MailPartsCsvLoader(settings)

class MailPartsCsvLoader:
    def __init__(self, settings):
        self.mailfrom_idx = settings.get('mailfrom_idx', 0)
        self.mailto_idx = settings.get('mailto_idx', 1)
        self.subject_idx = settings.get('subject_idx', 2)
        self.contents_idx = settings.get('contents_idx', 3)
        self.encoding = settings.get('encoding', 'utf-8')

    def load(self, csv_file_name):
        with open(csv_file_name, encoding=self.encoding) as f:
            csv_lines = f.readlines()
            csv_items_list = list(map(lambda csv_line: csv_line.split(','), csv_lines))
            mailpartslist = list(
                map(
                    lambda items: MailParts(
                        mail_from = items[self.mailfrom_idx], 
                        mail_to   = items[self.mailto_idx],
                        subject   = items[self.subject_idx],
                        contents  = items[self.contents_idx]
                    ),
                    csv_items_list
                )
            )
            return MailPartsList(*mailpartslist)
