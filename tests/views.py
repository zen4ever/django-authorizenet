from django.http import HttpResponse
from authorizenet.views import PaymentProfileCreateView, PaymentProfileUpdateView


class CreateCustomerView(PaymentProfileCreateView):
    def get_success_url(self):
        return '/success'


class UpdateCustomerView(PaymentProfileUpdateView):

    def get_object(self):
        return self.request.user.customer_profile.payment_profiles.get()

    def get_success_url(self):
        return '/success'


def success_view(request):
    return HttpResponse("success")
