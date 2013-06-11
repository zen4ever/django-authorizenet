from django.http import HttpResponse
from authorizenet.customers.views import PaymentProfileCreationView


from httmock import HTTMock
from .mocks import cim_url_match, success_response


@cim_url_match
def create_customer_success(url, request):
    return success_response.format('createCustomerProfileResponse')


class CreateCustomerView(PaymentProfileCreationView):

    def get_success_url(self):
        return '/success'

    def form_valid(self, *args, **kwargs):
        with HTTMock(create_customer_success):
            return super(CreateCustomerView, self).form_valid(*args, **kwargs)


def success_view(request):
    return HttpResponse("success")
