from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('samplestore.views',
    url(r'^commit/(\d+)/$', 'commit_to_buy', name="samplestore_commit_to_buy"),
    url(r'^make_payment/(\d+)/$', 'make_payment',
        name="samplestore_make_payment"),
    url(r'^$', 'items', name="samplestore_items"),
    url(r'^capture/(\d+)/$', 'capture', name="samplestore_capture"),
    url(r'^capture/index/$', 'capture_index',
        name="samplestore_capture_index"),
    url(r'^create_invoice/(\d+)/$', 'create_invoice',
        name="samplestore_create_invoice"),
    url(r'^create_invoice/(\d+)/auth/$', 'create_invoice',
        {'auth_only': True}, name="samplestore_create_invoice_auth"),
    url(r'^make_direct_payment/(\d+)/$', 'make_direct_payment',
        name="samplestore_make_direct_payment"),
    url(r'^make_direct_payment/(\d+)/auth/$', 'make_direct_payment',
        {'auth_only': True}, name="samplestore_make_direct_payment_auth"),
    
    url(r'^edit_cim_profile/$', 'edit_cim_profile',
        name='edit_cim_profile'),
)
