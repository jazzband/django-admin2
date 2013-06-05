from django.conf.urls import patterns, include, url

import djadmin2

djadmin2.default.autodiscover()

urlpatterns = patterns('',
    url(r'^admin2/', include(djadmin2.default.urls)),
)
