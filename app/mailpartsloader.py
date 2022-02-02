import sys
import enum
from .mailparts import MailParts, MailPartsList

class LoadType(enum.Enum):
    CSV = enum.auto()        

class MailPartsLoaderFactory:
    def create(loadtype, **settings):
        if loadtype == LoadType.CSV:
            return MailPartsCsvLoader(settings)

class CsvIndexes:
    def __init__(self, **idx_names):
        self.idx_name_dict = idx_names
    
    def max_value(self):
        return max(idx_name_dict.values())

    def value_of(self, idx_name, default=-1):
        return self.idx_name_dict.get(idx_name, default)


class MailPartsCsvLoader:
    def __init__(self, settings):
        self.indexes = CsvIndexes(
            mailfrom_idx = self.mailfrom_idx = settings.get('mailfrom_idx', 0)
            mailto_idx = self.mailto_idx = settings.get('mailto_idx', 1)
            subject_idx = self.subject_idx = settings.get('subject_idx', 2)
            contents_idx = self.contents_idx = settings.get('contents_idx', 3)
        )
        self.encoding = settings.get('encoding', 'utf-8')

    def load(self, csv_file_name):
        with open(csv_file_name, encoding=self.encoding) as f:
            csv_lines = f.readlines()            
            csv_items_list = list(map(lambda csv_line: csv_line.split(','), csv_lines))
            filtered_items_list = list(filter(lambda items: len(items) < max(self.indexes.max_value()), csv_items_list))
            mailpartslist = list(
                map(
                    lambda items: MailParts(
                        mail_from = items[self.indexes.value_of('mailfrom_idx')], 
                        mail_to   = items[self.indexes.value_of('mailto_idx')],
                        subject   = items[self.indexes.value_of('subject_idx')],
                        contents  = items[self.indexes.value_of('contents_idx')]
                    ),
                    csv_items_list
                )
            )
            return MailPartsList(*mailpartslist)
