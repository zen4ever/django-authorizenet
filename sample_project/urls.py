from django.conf.urls import url, include, patterns
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', RedirectView.as_view(url='/store/')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="auth_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="auth_logout"),
    url(r'^authnet/', include('authorizenet.urls')),
    url(r'^store/', include('samplestore.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()
