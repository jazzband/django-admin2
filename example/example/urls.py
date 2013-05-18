from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

import djadmin2

djadmin2.default.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin2/', include(djadmin2.default.urls)),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
