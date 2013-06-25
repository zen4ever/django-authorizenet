import hmac

from django.core.exceptions import ImproperlyConfigured

from authorizenet.conf import settings
from authorizenet.helpers import AIMPaymentHelper
from authorizenet.models import Response
from authorizenet.signals import payment_was_successful, payment_was_flagged


def get_fingerprint(x_fp_sequence, x_fp_timestamp, x_amount):
    msg = '^'.join([settings.LOGIN_ID,
           x_fp_sequence,
           x_fp_timestamp,
           x_amount
           ]) + '^'

    return hmac.new(settings.TRANSACTION_KEY, msg).hexdigest()


def extract_form_data(form_data):
    return dict(map(lambda x: ('x_' + x[0], x[1]),
                    form_data.items()))

AIM_DEFAULT_DICT = {
    'x_login': settings.LOGIN_ID,
    'x_tran_key': settings.TRANSACTION_KEY,
    'x_delim_data': "TRUE",
    'x_delim_char': settings.DELIM_CHAR,
    'x_relay_response': "FALSE",
    'x_type': "AUTH_CAPTURE",
    'x_method': "CC"
}


def create_response(data):
    helper = AIMPaymentHelper(defaults=AIM_DEFAULT_DICT)
    response_list = helper.get_response(data)
    response = Response.objects.create_from_list(response_list)
    if response.is_approved:
        payment_was_successful.send(sender=response)
    else:
        payment_was_flagged.send(sender=response)
    return response


def process_payment(form_data, extra_data):
    data = extract_form_data(form_data)
    data.update(extract_form_data(extra_data))
    data['x_exp_date'] = data['x_exp_date'].strftime('%m%y')
    if settings.FORCE_TEST_REQUEST:
        data['x_test_request'] = 'TRUE'
    if settings.EMAIL_CUSTOMER is not None:
        data['x_email_customer'] = settings.EMAIL_CUSTOMER
    return create_response(data)


def combine_form_data(*args):
    data = {}
    for form in args:
        data.update(form.cleaned_data)
    return data


def capture_transaction(response, extra_data=None):
    if response.type.lower() != 'auth_only':
        raise ImproperlyConfigured(
                "You can capture only transactions with AUTH_ONLY type")
    if extra_data is None:
        extra_data = {}
    data = dict(extra_data)
    data['x_trans_id'] = response.trans_id
    #if user already specified x_amount, don't override it with response value
    if not data.get('x_amount', None):
        data['x_amount'] = response.amount
    data['x_type'] = 'PRIOR_AUTH_CAPTURE'
    if settings.FORCE_TEST_REQUEST:
        data['x_test_request'] = 'TRUE'
    return create_response(data)
