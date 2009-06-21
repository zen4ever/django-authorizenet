from django.conf.urls.defaults import *

urlpatterns = patterns('authorizenet.views',
     url(r'^sim/payment/$', 'sim_payment', name="authnet_sim_payment"),
)
