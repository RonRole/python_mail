class MailSettingsController:
    def __init__(self, router):
        self.__router = router

    @router.route('GET', '/settings/mailserver')
    def read(self):
        print('GET MailSettingsController/read')

    @router.route('POST', '/settings/mailserver')
    def merge(self):
        print('POST MailSettingsController/merge')

