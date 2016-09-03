from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from djadmin2.site import djadmin2_site

from djadmin2.views import LoginView


class CustomLoginView(LoginView):
    default_template_name = "custom_login_template.html"

djadmin2_site.login_view = CustomLoginView
djadmin2_site.autodiscover()

urlpatterns = [
    url(r'^admin2/', include(djadmin2_site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
