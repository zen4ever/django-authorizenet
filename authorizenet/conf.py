"""
Application-specific settings for django-authorizenet

Available settings:

    - AUTHNET_DEBUG: Set to ``True`` if using Authorize.NET test account
    - AUTHNET_LOGIN_ID: Set to value of Authorize.NET login ID
    - AUTHNET_TRANSACTION_KEY: Set to value of Authorize.NET transaction key
    - AUTHNET_CUSTOMER_MODEL: Used to set customer model used for CIM customers
    (defaults to Django user)
    - AUTHNET_DELIM_CHAR: Used to set delimiter character for CIM requests
    (defaults to "|")
    - AUTHNET_FORCE_TEST_REQUEST
    - AUTHNET_EMAIL_CUSTOMER
    - AUTHNET_MD5_HASH

"""

from django.conf import settings as django_settings


class Settings(object):

    """
    Retrieves django.conf settings, using defaults from Default subclass

    All usable settings are specified in settings attribute.  Use an
    ``AUTHNET_`` prefix when specifying settings in django.conf.
    """

    prefix = 'AUTHNET_'
    settings = set(('DEBUG', 'LOGIN_ID', 'TRANSACTION_KEY', 'CUSTOMER_MODEL',
                   'DELIM_CHAR', 'FORCE_TEST_REQUEST', 'EMAIL_CUSTOMER',
                   'MD5_HASH'))

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
