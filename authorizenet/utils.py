import hmac
from django.conf import settings 

def get_fingerprint(x_fp_sequence, x_fp_timestamp, x_amount):
    msg = '^'.join([settings.AUTHNET_LOGIN_ID,
           x_fp_sequence,
           x_fp_timestamp,
           x_amount
           ])+'^'

    return hmac.new(settings.AUTHNET_TRANSACTION_KEY, msg).hexdigest()
