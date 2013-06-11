from django.http import HttpResponse
from authorizenet.customers.views import PaymentProfileCreationView


class CreateCustomerView(PaymentProfileCreationView):

    def get_success_url(self):
        return '/success'


def success_view(request):
    return HttpResponse("success")
