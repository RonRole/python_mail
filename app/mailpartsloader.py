import sys
import enum
from .mailparts import MailParts

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
        self.contents_idx = settings.get('contents', 3)
        self.encoding = settings.get('encoding', 'utf-8')

    def load(self, csv_file_name):
        with open(csv_file_name, encoding=self.encoding) as f:
            csv_lines = f.readlines()

            address_contents_dict = {}
            for csv_line in csv_lines:
                csv_items = csv_line.split(',')
                address_keys = (
                    csv_items[self.mailfrom_idx], 
                    csv_items[self.mailto_idx], 
                    csv_items[self.subject_idx]
                )
                contents = csv_items[self.contents_idx]
                address_contents_dict[address_keys] = address_contents_dict.get(address_keys, '') + contents
            return list(map(lambda keys: MailParts(mail_from = keys[0], mail_to = keys[1], subject = keys[2], contents = address_contents_dict[keys]), address_contents_dict))
