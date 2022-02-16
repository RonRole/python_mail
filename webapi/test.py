import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import router

temp_router = router.Router()

class SettingsController:
    @temp_router.route('GET', '^/settings$')
    def all():
        return 'dammy settings'

    @temp_router.route('POST', '^/settings$')
    def merge(smtpserver="",smtpport="",mail_account="", mail_password=""):
        return 'dammy set settings'

def router():
    return temp_router
