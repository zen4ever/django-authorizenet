from django.views.generic.edit import FormView

from authorizenet.forms import CustomerPaymentForm
from .models import CustomerProfile, CustomerPaymentProfile


class PaymentProfileCreationView(FormView):
    template_name = 'authorizenet/payment_profile_creation.html'
    form_class = CustomerPaymentForm

    def form_valid(self, form):
        """If the form is valid, save the payment profile"""
        self.create_payment_profile(
            payment_data=form.payment_data,
            billing_data=form.billing_data,
        )
        return super(PaymentProfileCreationView, self).form_valid(form)

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
