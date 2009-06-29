import urllib, urllib2
from django.conf import settings
from authorizenet import AUTHNET_POST_URL, AUTHNET_TEST_POST_URL 

class AIMPaymentHelper(object):
    def __init__(self, defaults):
        self.defaults = defaults
        if settings.AUTHNET_DEBUG:
            self.endpoint = AUTHNET_TEST_POST_URL
        else:
            self.endpoint = AUTHNET_POST_URL
        

    def get_response(self, data):
        final_data = dict(self.defaults)
        final_data.update(data)
        c = final_data['x_delim_char']
        request_string = urllib.urlencode(final_data)
        response = urllib2.urlopen(self.endpoint, request_string).read()
        return response.split(c)


