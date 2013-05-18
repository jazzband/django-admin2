from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

import djadmin2

djadmin2.default.autodiscover()

urlpatterns = patterns('',
    url(r'^admin2/', include(djadmin2.default.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
