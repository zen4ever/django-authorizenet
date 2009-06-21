from django.contrib import admin
from samplestore.models import Invoice, Item, Customer, Address

admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Address)
