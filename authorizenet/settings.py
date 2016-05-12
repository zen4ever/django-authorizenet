from django.conf import settings

try:
    AUTHNET_POST_URL = settings.AUTHNET_POST_URL
except AttributeError:
    AUTHNET_POST_URL = "https://secure2.authorize.net/gateway/transact.dll"

try:
    AUTHNET_TEST_POST_URL = settings.AUTHNET_TEST_POST_URL
except AttributeError:
    AUTHNET_TEST_POST_URL = "https://test.authorize.net/gateway/transact.dll"

try:
    AUTHNET_TEST_CIM_URL = settings.AUTHNET_TEST_CIM_URL
except AttributeError:
    AUTHNET_TEST_CIM_URL = "https://apitest.authorize.net/xml/v1/request.api"

try:
    AUTHNET_CIM_URL = settings.AUTHNET_CIM_URL
except AttributeError:
    AUTHNET_CIM_URL = "https://api2.authorize.net/xml/v1/request.api"
