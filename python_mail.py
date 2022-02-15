import sys
import os
import json
import re
import settings
import app

args = sys.argv
LOAD_FILE_NAME = args[1]

FULLPATH_SETTINGS_JSON = f'{os.path.dirname(os.path.abspath(__file__))}/settings.json'

mailserver = settings.SettingsToMailServer.load(FULLPATH_SETTINGS_JSON)
loadtypes = settings.SettingsToLoadTypes.load(FULLPATH_SETTINGS_JSON)
(loadtype, load_settings) = loadtypes.matched_item(LOAD_FILE_NAME)

mailpartsloader = app.MailPartsLoaderFactory.create(loadtype, **load_settings)
mailpartslist = mailpartsloader.load(LOAD_FILE_NAME).group_by_address_and_subject()

for mailparts in mailpartslist:
    mailserver.send(mailparts)

