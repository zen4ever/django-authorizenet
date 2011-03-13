from django.contrib import admin
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
    readonly_fields = ('created',)

admin.site.register(CIMResponse, CIMResponseAdmin)
