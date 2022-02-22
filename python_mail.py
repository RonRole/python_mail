import sys
import os
import json
import re
import settings
import app
import time

def calc_func_time(func_name):
    def decorator(func):
        def target_func(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func_name} took {end - start} sec")
            return result
        return target_func
    return decorator

args = sys.argv
LOAD_FILE_NAME = args[1]

FULLPATH_SETTINGS_JSON = f'{os.path.dirname(os.path.abspath(__file__))}/settings.json'


@calc_func_time('load_settings')
def load_settings():
    mailserver = settings.SettingsToMailServer.load(FULLPATH_SETTINGS_JSON)
    loadtypes = settings.SettingsToLoadTypes.load(FULLPATH_SETTINGS_JSON)
    (loadtype, load_settings) = loadtypes.matched_item(LOAD_FILE_NAME)
    return (mailserver, loadtype, load_settings)

@calc_func_time('load_mailpartslist')
def load_mailpartslist(loadtype, **load_settings):
    mailpartsloader = app.MailPartsLoaderFactory.create(loadtype, **load_settings)
    mailpartslist = mailpartsloader.load(LOAD_FILE_NAME).group_by_address_and_subject()
    return mailpartslist

@calc_func_time('send_mails')
def send_mails(mailserver, mailpartslist):
    with mailserver:
        for mailparts in mailpartslist:
            mailserver.send(mailparts)

(mailserver, loadtype, load_settings) = load_settings()
mailpartslist = load_mailpartslist(loadtype, **load_settings)
send_mails(mailserver, mailpartslist)

