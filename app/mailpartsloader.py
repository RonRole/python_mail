import enum
from .mailparts import MailParts, MailPartsList

class LoadType(enum.Enum):
    CSV_LINE = enum.auto()
    CSV_FILE = enum.auto()

class MailPartsLoaderFactory:
    def create(loadtype, **settings):
        if loadtype == LoadType.CSV_LINE:
            return MailPartsCsvLineLoader(settings)
        if loadtype == LoadType.CSV_FILE:
            return FileReadLoaderDecorator(
                decorated_loader = MailPartsCsvLineLoader(settings),
                encoding = settings['encoding']    
            )
class CsvIndexes:
    def __init__(self, **idx_names):
        self.__idx_name_dict = idx_names
    
    def max_value(self):
        return max(self.__idx_name_dict.values())

    def value_of(self, idx_name, default=-1):
        return self.__idx_name_dict.get(idx_name, default)

class MailPartsCsvLineLoader:
    def __init__(self, settings):
        self.__indexes = CsvIndexes(
            mailfrom_idx = settings.get('mailfrom_idx', 0),
            mailto_idx   = settings.get('mailto_idx', 1),
            subject_idx  = settings.get('subject_idx', 2),
            contents_idx = settings.get('contents_idx', 3)
        )

    def load(self, csv_lines):
        csv_items_list = list(map(lambda csv_line: csv_line.split(','), csv_lines))
        filtered_items_list = list(filter(lambda items: len(items) > self.__indexes.max_value(), csv_items_list))
        mailpartslist = list(
            map(
                lambda items: MailParts(
                    mail_from = items[self.__indexes.value_of('mailfrom_idx')],
                    mail_to   = items[self.__indexes.value_of('mailto_idx')],
                    subject   = items[self.__indexes.value_of('subject_idx')],
                    contents  = items[self.__indexes.value_of('contents_idx')]
                ),
                filtered_items_list
            )
        )
        return MailPartsList(*mailpartslist)

class FileReadLoaderDecorator:
    import sys
    def __init__(self, decorated_loader, encoding):
        self.__decorated_loader = decorated_loader
        self.__encoding = encoding
    
    def load(self, file_name):
        with open(file_name, encoding=self.__encoding) as f:
            lines = f.readlines()
            return self.__decorated_loader.load(lines)


