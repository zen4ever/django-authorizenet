from django import forms
from django.conf import settings

AUTHNET_POST_URL = "http://secure.authorize.net/gateway/transact.dll"  
AUTHNET_TEST_POST_URL = "https://test.authorize.net/gateway/transact.dll"


class SIMPaymentForm(forms.Form):
     x_login = forms.CharField(max_length=20, required=True, widget=forms.HiddenInput, initial=settings.AUTHNET_LOGIN_ID)
     x_type = forms.CharField(max_length=20, widget=forms.HiddenInput, initial="AUTH_CAPTURE")
     x_amount = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.HiddenInput)
     x_show_form = forms.CharField(max_length=20, widget=forms.HiddenInput, initial="PAYMENT_FORM")
     x_method = forms.CharField(max_length=10, widget=forms.HiddenInput, initial="CC")
     x_fp_sequence = forms.CharField(max_length=10, widget=forms.HiddenInput, initial="CC")
     x_version = forms.CharField(max_length=10, widget=forms.HiddenInput, initial="3.1")
     x_relay_response = forms.CharField(max_length=8, widget=forms.HiddenInput, initial="TRUE")
     x_fp_timestamp = forms.CharField(max_length=55, widget=forms.HiddenInput)
     x_relay_url = forms.CharField(max_length=55, widget=forms.HiddenInput)
     x_fp_hash = forms.CharField(max_length=55, widget=forms.HiddenInput)
     x_invoice_num = forms.CharField(max_length=55, required=False, widget=forms.HiddenInput)
     x_description = forms.CharField(max_length=255, required=False, widget=forms.HiddenInput)

class SIMBillingForm(forms.Form):
    x_first_name = forms.CharField(max_length=50, widget=forms.HiddenInput)
    x_last_name = forms.CharField(max_length=50, widget=forms.HiddenInput)
    x_company = forms.CharField(max_length=50, widget=forms.HiddenInput)
    x_address = forms.CharField(max_length=60, widget=forms.HiddenInput)
    x_city = forms.CharField(max_length=40, widget=forms.HiddenInput)
    x_state = forms.CharField(max_length=40, widget=forms.HiddenInput)
    x_zip = forms.CharField(max_length=20, widget=forms.HiddenInput)
    x_country = forms.CharField(max_length=60, widget=forms.HiddenInput)
    x_phone = forms.CharField(max_length=25, widget=forms.HiddenInput)
    x_fax = forms.CharField(max_length=25, widget=forms.HiddenInput)
    x_email = forms.CharField(max_length=255, widget=forms.HiddenInput)
    x_cust_id = forms.CharField(max_length=20, widget=forms.HiddenInput)
