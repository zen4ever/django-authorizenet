"""Application-specific settings for django-authorizenet"""

from django.conf import settings as django_settings


class Settings(object):

    """
    Retrieves django.conf settings, using defaults from Default subclass

    All usable settings are specified in settings attribute.  Use an
    ``AUTHNET_`` prefix when specifying settings in django.conf.
    """

    prefix = 'AUTHNET_'
    settings = {'DEBUG', 'LOGIN_ID', 'TRANSACTION_KEY', 'CUSTOMER_MODEL',
                'DELIM_CHAR', 'FORCE_TEST_REQUEST', 'EMAIL_CUSTOMER',
                'MD5_HASH'}

    class Default:
        CUSTOMER_MODEL = getattr(
            django_settings, 'AUTH_USER_MODEL', "auth.User")
        DELIM_CHAR = "|"
        FORCE_TEST_REQUEST = False
        EMAIL_CUSTOMER = None
        MD5_HASH = ""

    def __init__(self):
        self.defaults = Settings.Default()

    def __getattr__(self, name):
        if name not in self.settings:
            raise AttributeError("Setting %s not understood" % name)
        try:
            return getattr(django_settings, self.prefix + name)
        except AttributeError:
            return getattr(self.defaults, name)

settings = Settings()
