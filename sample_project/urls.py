from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/store/'}),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="auth_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="auth_logout"),
    (r'^authnet/', include('authorizenet.urls')),
    (r'^store/', include('samplestore.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
