try:
    import hashlib
except ImportError:
    import md5 as hashlib

from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt

from authorizenet.forms import AIMPaymentForm, BillingAddressForm
from authorizenet.models import Response
from authorizenet.signals import payment_was_successful, payment_was_flagged
from authorizenet.utils import process_payment, combine_form_data


@csrf_exempt
def sim_payment(request):
    response = Response.objects.create_from_dict(request.POST)
    MD5_HASH = getattr(settings, "AUTHNET_MD5_HASH", "")
    hash_is_valid = True

    #if MD5-Hash value is provided, use it to validate response
    if MD5_HASH:
        hash_is_valid = False
        hash_value = hashlib.md5(''.join([MD5_HASH,
                                          settings.AUTHNET_LOGIN_ID,
                                          response.trans_id,
                                          response.amount])).hexdigest()

        hash_is_valid = hash_value.upper() == response.MD5_Hash

    if response.is_approved and hash_is_valid:
        payment_was_successful.send(sender=response)
    else:
        payment_was_flagged.send(sender=response)

    return direct_to_template(request, 'authorizenet/sim_payment.html')


class AIMPayment(object):
    """
    Class to handle credit card payments to Authorize.NET
    """

    processing_error = ("There was an error processing your payment. "
                        "Check your information and try again.")
    form_error = "Please correct the errors below and try again."

    def __init__(self,
                 extra_data={},
                 payment_form_class=AIMPaymentForm,
                 context={},
                 billing_form_class=BillingAddressForm,
                 shipping_form_class=None,
                 payment_template="authorizenet/aim_payment.html",
                 success_template='authorizenet/aim_success.html',
                 initial_data={}):
        self.extra_data = extra_data
        self.payment_form_class = payment_form_class
        self.payment_template = payment_template
        self.success_template = success_template
        self.context = context
        self.initial_data = initial_data
        self.billing_form_class = billing_form_class
        self.shipping_form_class = shipping_form_class

    def __call__(self, request):
        self.request = request
        if request.method == "GET":
            return self.render_payment_form()
        else:
            return self.validate_payment_form()

    def render_payment_form(self):
        self.context['payment_form'] = self.payment_form_class(
                initial=self.initial_data)
        self.context['billing_form'] = self.billing_form_class(
                initial=self.initial_data)
        if self.shipping_form_class:
            self.context['shipping_form'] = self.shipping_form_class(
                    initial=self.initial_data)
        return direct_to_template(self.request,
                                  self.payment_template,
                                  self.context)

    def validate_payment_form(self):
        payment_form = self.payment_form_class(self.request.POST)
        billing_form = self.billing_form_class(self.request.POST)
        
        if self.shipping_form_class:
            shipping_form = self.shipping_form_class(self.request.POST)

        #if shipping for exists also validate it
        if payment_form.is_valid() and billing_form.is_valid() and (not self.shipping_form_class or shipping_form.is_valid()):
            
            if not self.shipping_form_class:
                args = payment_form, billing_form
            else:
                args = payment_form, billing_form, shipping_form
            
            form_data = combine_form_data(*args)
            response = process_payment(form_data, self.extra_data)
            self.context['response'] = response
            if response.is_approved:
                return direct_to_template(self.request,
                                          self.success_template,
                                          self.context)
            else:
                self.context['errors'] = self.processing_error
        self.context['payment_form'] = payment_form
        self.context['billing_form'] = billing_form
        if self.shipping_form_class:
            self.context['shipping_form'] = shipping_form
        self.context.setdefault('errors', self.form_error)
        return direct_to_template(self.request,
                                  self.payment_template,
                                  self.context)
