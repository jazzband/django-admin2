from blog.views import BlogListView, BlogDetailView
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from djadmin2 import site

admin.autodiscover()

site.default.autodiscover()

urlpatterns = [
    url(r'^admin2/', include(site.default.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', BlogListView.as_view(template_name="blog/blog_list.html"), name='blog_list'),
    url(r'^blog/detail(?P<pk>\d+)/$', BlogDetailView.as_view(template_name="blog/blog_detail.html"), name='blog_detail'),
    url(r'^$', BlogListView.as_view(template_name="blog/home.html"), name='home'),
]