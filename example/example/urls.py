from blog.views import BlogListView, BlogDetailView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

from djadmin2.site import djadmin2_site


djadmin2_site.autodiscover()

urlpatterns = [
    re_path(r"^admin2/", djadmin2_site.urls),
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^blog/",
        BlogListView.as_view(template_name="blog/blog_list.html"),
        name="blog_list",
    ),
    re_path(
        r"^blog/detail(?P<pk>\d+)/$",
        BlogDetailView.as_view(template_name="blog/blog_detail.html"),
        name="blog_detail",
    ),
    re_path(r"^$", BlogListView.as_view(template_name="blog/home.html"), name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
