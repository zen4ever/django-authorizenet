import sys
from os.path import abspath, dirname

from django.conf import settings

sys.path.insert(0, abspath(dirname(__file__)))

if not settings.configured:
    settings.configure(
        AUTHNET_DEBUG=False,
        AUTHNET_LOGIN_ID="loginid",
        AUTHNET_TRANSACTION_KEY="key",
        INSTALLED_APPS=(
            'authorizenet.tests',
            'authorizenet',
        ),
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    )


def runtests():
    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(failfast=False).run_tests(['tests'])
    sys.exit(failures)
