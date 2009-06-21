from django.conf.urls.defaults import *

urlpatterns = patterns('samplestore.views',
     url(r'^make_payment/(\d+)/$', 'make_payment', name="samplestore_make_payment"),
)
