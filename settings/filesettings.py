import re
import json
import sys
sys.path.append('../')
import app

class SettingsToLoadTypes(object):
    def load(fullpath_settings_json):
        settings_json = open(fullpath_settings_json, 'r')
        settings = json.load(settings_json)
        return FileNamePatternToLoadTypeAndSettings(**{
            '^.*\.csv$'  : (app.LoadType.CSV_FILE , SettingsToCsvLoadType(settings).read_dict()),
            '^.*\.json$' : (app.LoadType.JSON_FILE, SettingsToJsonLoadType(settings).read_dict()),
            '^.*$'       : (None, None)
        })

class SettingsToCsvLoadType(object):
    def __init__(self, settings):
        csv_settings = settings['csv']
        self.__CSV_MAILFROM_IDX = csv_settings['mailfrom_idx']
        self.__CSV_MAILTO_IDX   = csv_settings['mailto_idx']
        self.__CSV_SUBJECT_IDX  = csv_settings['subject_idx']
        self.__CSV_CONTENTS_IDX = csv_settings['contents_idx']
        self.__CSV_ENCODING     = csv_settings['encoding']

    def read_dict(self):
        return {
            'mailfrom_idx' : self.__CSV_MAILFROM_IDX,
            'mailto_idx'   : self.__CSV_MAILTO_IDX,
            'subject_idx'  : self.__CSV_SUBJECT_IDX,
            'contents_idx' : self.__CSV_CONTENTS_IDX,
            'encoding'     : self.__CSV_ENCODING
        }  

class SettingsToJsonLoadType(object):
    def __init__(self, settings):
        json_settings = settings['json']
        self.__MAILFROM_PROP_NAME = json_settings['mailfrom_prop_name']      
        self.__MAILTO_PROP_NAME   = json_settings['mailto_prop_name']      
        self.__SUBJECT_PROP_NAME  = json_settings['subject_prop_name']      
        self.__CONTENTS_PROP_NAME = json_settings['contents_prop_name']      

    def read_dict(self):
        return {
            'mailfrom_prop_name' : self.__MAILFROM_PROP_NAME,
            'mailto_prop_name'   : self.__MAILTO_PROP_NAME,
            'subject_prop_name'  : self.__SUBJECT_PROP_NAME, 
            'contents_prop_name' : self.__CONTENTS_PROP_NAME
        }
class FileNamePatternToLoadTypeAndSettings(object):

    def __init__(self, **pattern_to_loadtypes):
        self.__pattern_loadtype_dict = pattern_to_loadtypes.copy()

    def matched_item(self,file_name):
        matched_key_values_iter = iter(filter(lambda key_value: re.match(key_value[0], file_name), self.__pattern_loadtype_dict.items()))
        return next(matched_key_values_iter)[1]