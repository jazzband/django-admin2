from django.conf.urls import patterns, include, url
from django.conf import settings
from django.utils.importlib import import_module


from . import models
from . import views


class Admin2(object):
    index_view = views.IndexView

    def __init__(self):
        self.registry = {}

    def register(self, model, modeladmin=models.ModelAdmin2, **kwargs):
        self.registry[model] = modeladmin(model, **kwargs)

    def deregister(self, model):
        del self.registry[model]

    def autodiscover(self):
        apps = []
        for app_name in [x for x in settings.INSTALLED_APPS]:
            try:
                import_module("%s.admin2" % app_name)
            except ImportError as e:
                if str(e) == "No module named admin2":
                    continue
                raise e

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.index_view.as_view(), name='index'),
        )
        for model, modeladmin in self.registry.iteritems():
            urlpatterns += patterns('',
                url('^{}/{}/'.format(model._meta.app_label, model._meta.object_name.lower()),
                    include(modeladmin.urls)),
            )
        return urlpatterns

    @property
    def urls(self):
        # We set the application and instance namespace here
        return self.get_urls(), None, None