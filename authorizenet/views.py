from django.views.generic.simple import direct_to_template

from authorizenet.forms import AIMPaymentForm, BillingAddressForm
from authorizenet.models import Response
from authorizenet.signals import payment_was_successful, payment_was_flagged
from authorizenet.utils import process_payment, combine_form_data


def sim_payment(request):
    response = Response.objects.create_from_dict(request.POST)
    if response.is_approved:
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
        return direct_to_template(self.request,
                                  self.payment_template,
                                  self.context)

    def validate_payment_form(self):
        payment_form = self.payment_form_class(self.request.POST)
        billing_form = self.billing_form_class(self.request.POST)
        if payment_form.is_valid() and billing_form.is_valid():
            form_data = combine_form_data(payment_form, billing_form)
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
        self.context.setdefault('errors', self.form_error)
        return direct_to_template(self.request,
                                  self.payment_template,
                                  self.context)
