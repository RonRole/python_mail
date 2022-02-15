import json
import enum
from .mailparts import MailParts, MailPartsList

class LoadType(enum.Enum):
    CSV_LINE  = enum.auto()
    CSV_FILE  = enum.auto()
    JSON_FILE = enum.auto()

class MailPartsLoaderFactory:
    def create(loadtype, **settings):
        if loadtype == LoadType.CSV_LINE:
            return MailPartsCsvLineLoader(**settings)
        if loadtype == LoadType.CSV_FILE:
            return FileLineReadLoaderDecorator(
                decorated_loader = MailPartsCsvLineLoader(**settings),
                encoding = settings['encoding']    
            )
        if loadtype == LoadType.JSON_FILE:
            return MailPartsJsonFileLoader(**settings)
            
class CsvIndexes:
    def __init__(self, **idx_names):
        self.__idx_name_dict = idx_names
    
    def max_value(self):
        return max(self.__idx_name_dict.values())

    def value_of(self, idx_name, default=-1):
        return self.__idx_name_dict.get(idx_name, default)

class MailPartsCsvLineLoader:
    def __init__(self, **settings):
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

class FileLineReadLoaderDecorator:
    def __init__(self, decorated_loader, encoding):
        self.__decorated_loader = decorated_loader
        self.__encoding = encoding
    
    def load(self, file_name):
        with open(file_name, encoding=self.__encoding) as f:
            lines = f.readlines()
            return self.__decorated_loader.load(lines)

class MailPartsJsonFileLoader:
    def __init__(self, **settings):
        self.__mailto_prop_name   = settings.get('mailto_prop_name'  , '')
        self.__mailfrom_prop_name = settings.get('mailfrom_prop_name', '')
        self.__subject_prop_name  = settings.get('subject_prop_name' , '')
        self.__contents_prop_name = settings.get('contents_prop_name', '')

    def load(self, json_file_name):
        with open(json_file_name, 'r') as f:
            json_items = json.load(f)
            mailpartslist = list(
                map(
                    lambda key : MailParts(
                        mail_from = json_items[key][self.__mailfrom_prop_name],
                        mail_to   = json_items[key][self.__mailto_prop_name]  ,
                        subject   = json_items[key][self.__subject_prop_name] ,
                        contents  = json_items[key][self.__contents_prop_name],
                    ),
                    json_items
                )
            )
            return MailPartsList(*mailpartslist)
