from django.shortcuts import render_to_response
from django.template import RequestContext
from authorizenet.models import Response
from authorizenet.forms import AIMPaymentForm, BillingAddressForm
from django.http import HttpResponseRedirect
from authorizenet.signals import payment_was_successful, payment_was_flagged

def sim_payment(request):
    response = Response.objects.create_from_dict(request.POST)
    if response.is_approved:
        payment_was_successful.send(sender=response)
    else:
        payment_was_flagged.send(sender=response)
    return render_to_response('authorizenet/sim_payment.html', context_instance=RequestContext(request))

class AIMPayment(object):
    """
    Class to handle credit card payments to Authorize.NET
    """

    processing_error = "There was an error processing your payment. Check your information and try again."
    form_error = "Please correct the errors below and try again."

    def __init__(self, extra_data=None, payment_form_class=AIMPaymentForm, context=None, billing_form_class=BillingAddressForm, payment_template="authorizenet/aim_payment.html", success_template='authorizenet/aim_success.html', initial_data={}):
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

    def create_initial_forms(self):
        self.context['billing_form'] = self.billing_form_class(initial=self.initial_data)

    def render_payment_form(self):
        self.context['form'] = self.payment_form_class(initial=self.initial_data)
        self.create_initial_forms()
        return render_to_response(self.payment_template, self.context, context_instance=RequestContext(self.request))

    def combine_form_data(self, payment_form, *args):
        billing_form = args[0]
        data = dict(billing_form.cleaned_data)
        data.update(payment_form.cleaned_data)
        return data

    def create_forms(self):
        billing_form = self.billing_form_class(self.request.POST)
        return [billing_form]

    def forms_are_valid(self, forms):
        return reduce(lambda x,y: x and y, map(lambda x: x.is_valid(), forms))

    def add_forms_to_context(self, forms):
        self.context['billing_form'] = forms[0]

    def validate_payment_form(self):
        form = self.payment_form_class(self.request.POST)
        forms = self.create_forms()
        if form.is_valid() and self.forms_are_valid(forms):
            form_data = self.combine_form_data(form, *forms)
            from authorizenet.utils import process_payment
            response = process_payment(form_data, self.extra_data)
            if response.is_approved:
                self.context['response'] = response
                return render_to_response(self.success_template, self.context, context_instance=RequestContext(self.request))
            else:
                self.context['errors'] = self.processing_error
        self.context['form'] = form
        self.add_forms_to_context(forms)
        self.context.setdefault('errors', self.form_error)
        return render_to_response(self.payment_template, self.context, context_instance=RequestContext(self.request))


