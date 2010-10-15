from django.contrib import admin
from authorizenet.models import Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['response_code',
                    'response_reason_text',
                    'auth_code',
                    'trans_id']

admin.site.register(Response, ResponseAdmin)
