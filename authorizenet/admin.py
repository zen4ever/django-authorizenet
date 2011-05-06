from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from authorizenet.models import Response, CIMResponse


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['response_code',
                    'response_reason_text',
                    'auth_code',
                    'trans_id']
    readonly_fields = ('created',)

admin.site.register(Response, ResponseAdmin)


class CIMResponseAdmin(admin.ModelAdmin):
    list_display = ['result_code',
                    'result']
    readonly_fields = ('created', 'response_link')
    exclude = ['transaction_response',]

    def response_link(self, obj):
        change_url = reverse('admin:authorizenet_response_change',
                args=(obj.transaction_response.id,))
        return mark_safe('<a href="%s">%s</a>' % (change_url,
            obj.transaction_response))
    response_link.short_description = 'transaction response'

admin.site.register(CIMResponse, CIMResponseAdmin)
