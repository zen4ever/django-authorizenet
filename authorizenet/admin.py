from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from authorizenet.models import (Response, CIMResponse, CustomerProfile,
                                 CustomerPaymentProfile)
from authorizenet.forms import CustomerPaymentForm, CustomerPaymentAdminForm
from relatives.utils import object_edit_link


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['response_code',
                    'response_reason_text',
                    'auth_code',
                    'trans_id']

    readonly_fields = ['response_code',
                       'response_subcode',
                       'response_reason_code',
                       'response_reason_text',
                       'auth_code',
                       'avs_code',
                       'trans_id',
                       'invoice_num',
                       'description',
                       'amount',
                       'method',
                       'type',
                       'cust_id',
                       'first_name',
                       'last_name',
                       'company',
                       'address',
                       'city',
                       'state',
                       'zip',
                       'country',
                       'phone',
                       'fax',
                       'email',
                       'ship_to_first_name',
                       'ship_to_last_name',
                       'ship_to_company',
                       'ship_to_address',
                       'ship_to_city',
                       'ship_to_state',
                       'ship_to_zip',
                       'ship_to_country',
                       'tax',
                       'duty',
                       'freight',
                       'tax_exempt',
                       'po_num',
                       'MD5_Hash',
                       'cvv2_resp_code',
                       'cavv_response',
                       'test_request',
                       'card_type',
                       'account_number',
                       'created']

admin.site.register(Response, ResponseAdmin)


class CIMResponseAdmin(admin.ModelAdmin):
    list_display = ['result_code',
                    'result']

    readonly_fields = ['result',
                       'result_code',
                       'result_text',
                       'response_link',
                       'created']

    exclude = ['transaction_response']

    def response_link(self, obj):
        change_url = reverse('admin:authorizenet_response_change',
                args=(obj.transaction_response.id,))
        return mark_safe('<a href="%s">%s</a>' % (change_url,
            obj.transaction_response))
    response_link.short_description = 'transaction response'

admin.site.register(CIMResponse, CIMResponseAdmin)


class CustomerPaymentProfileInline(admin.TabularInline):
    model = CustomerPaymentProfile
    form = CustomerPaymentForm
    fields = [object_edit_link("Edit"), 'first_name', 'last_name',
              'card_number', 'expiration_date']
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_id', 'customer']
    readonly_fields = ['profile_id', 'customer']
    inlines = [CustomerPaymentProfileInline]

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj is not None else ['profile_id']

admin.site.register(CustomerProfile, CustomerProfileAdmin)


class CustomerPaymentProfileAdmin(admin.ModelAdmin):
    list_display = ['payment_profile_id', 'customer_profile', 'customer']
    readonly_fields = ['payment_profile_id', 'customer', 'customer_profile']
    form = CustomerPaymentAdminForm

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj is not None else []

admin.site.register(CustomerPaymentProfile, CustomerPaymentProfileAdmin)
