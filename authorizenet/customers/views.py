from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from authorizenet.forms import CIMPaymentForm, BillingAddressForm
from .models import CustomerProfile, CustomerPaymentProfile


class PaymentProfileCreationView(TemplateView):
    template_name = 'authorizenet/payment_profile_creation.html'
    payment_form_class = CIMPaymentForm
    billing_form_class = BillingAddressForm

    def post(self, *args, **kwargs):
        payment_form = self.get_payment_form()
        billing_form = self.get_billing_form()
        if payment_form.is_valid() and billing_form.is_valid():
            return self.forms_valid(payment_form, billing_form)
        else:
            return self.forms_invalid(payment_form, billing_form)

    def get(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data(
            payment_form=self.get_payment_form(),
            billing_form=self.get_billing_form(),
        ))

    def forms_valid(self, payment_form, billing_form):
        """If the form is valid, save the payment profile and redirect"""
        self.create_payment_profile(
            payment_data=payment_form.cleaned_data,
            billing_data=billing_form.cleaned_data,
        )
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, payment_form, billing_form):
        """If the form is invalid, show the page again"""
        return self.render_to_response(self.get_context_data(
            payment_form=payment_form,
            billing_form=billing_form,
        ))

    def get_payment_form(self):
        """Returns an instance of the payment form"""
        if self.request.method in ('POST', 'PUT'):
            kwargs = {'data': self.request.POST}
        else:
            kwargs = {}
        return self.payment_form_class(**kwargs)

    def get_billing_form(self):
        """Returns an instance of the billing form"""
        if self.request.method in ('POST', 'PUT'):
            kwargs = {'data': self.request.POST}
        else:
            kwargs = {}
        return self.billing_form_class(**kwargs)

    def create_payment_profile(self, **kwargs):
        """Create and return payment profile"""
        customer_profile = self.get_customer_profile()
        if customer_profile:
            return CustomerPaymentProfile.objects.create(
                customer_profile=customer_profile, **kwargs)
        else:
            customer_profile = CustomerProfile.objects.create(
                user=self.request.user, **kwargs)
            return customer_profile.payment_profiles.get()

    def get_customer_profile(self):
        """Return customer profile or ``None`` if none exists"""
        try:
            return CustomerProfile.objects.get(user=self.request.user)
        except CustomerProfile.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        return kwargs
