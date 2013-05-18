from django.conf.urls import patterns, include, url
from django.conf import settings
from django.utils.importlib import import_module


from . import models
from . import views


class Admin2(object):
    index_view = views.IndexView

    def __init__(self, name='admin2', app_name='admin2'):
        self.registry = {}
        self.name = name
        self.app_name = app_name

    def register(self, model, modeladmin=None, **kwargs):
        if not modeladmin:
            modeladmin = models.ModelAdmin2
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

    def get_index_kwargs(self):
        return {
            'registry': self.registry,
        }

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.index_view.as_view(**self.get_index_kwargs()), name='index'),
        )
        for model, modeladmin in self.registry.iteritems():
            app_label = model._meta.app_label
            model_name = model._meta.object_name.lower()        

            urlpatterns += patterns('',
                url('^{}/{}/'.format(app_label, model_name),
                    include(modeladmin.urls)),
            )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name
