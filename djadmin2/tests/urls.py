from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from djadmin2.site import djadmin2_site

from djadmin2.views import LoginView


class CustomLoginView(LoginView):
    default_template_name = "custom_login_template.html"


djadmin2_site.login_view = CustomLoginView
djadmin2_site.autodiscover()

urlpatterns = [
    re_path(r'^admin2/', djadmin2_site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
