from django.conf.urls.defaults import *

urlpatterns = patterns('samplestore.views',
     url(r'^commit/(\d+)/$', 'commit_to_buy', name="samplestore_commit_to_buy"),
     url(r'^make_payment/(\d+)/$', 'make_payment', name="samplestore_make_payment"),
     url(r'^$', 'items', name="samplestore_items"),
     url(r'^create_invoice/(\d+)/$', 'create_invoice', name="samplestore_create_invoice"),
     url(r'^make_direct_payment/(\d+)/$', 'make_direct_payment', name="samplestore_make_direct_payment"),
)
