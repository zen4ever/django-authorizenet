import urllib
import urllib2
import re
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
        # Escape delimiter characters in request fields
        for k, v in final_data.items():
            if k != 'x_delim_char':
                final_data[k] = unicode(v).replace(c, "\\%s" % c)
        request_string = urllib.urlencode(final_data)
        response = urllib2.urlopen(self.endpoint, request_string).read()
        # Split response by delimiter, unescaping delimiter characters in fields
        response_list = re.split("(?<!\\\\)\%s" % c, response)
        response_list = map(lambda s: s.replace("\\%s" % c, c), response_list)
        return response_list
