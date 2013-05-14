from django.conf import settings
from django.utils.importlib import import_module


class AppStore(object):

    def __init__(self, module):
        self.models = []
        for key in module.__dict__.keys():
            model_candidate = getattr(module, key)
            if hasattr(model_candidate, 'admin2'):
                self.add_model(model_candidate)

    def add_model(self, model):
        model.name = model.__name__
        self.models.append(model)


def get_admin2s(self):
    """ Returns a list of all admin2 implementations for the site """
    apps = []
    for app_name in settings.INSTALLED_APPS:
        admin2 = "{0}.admin2".format(app_name)
        try:
            module = import_module(admin2)
        except ImportError as e:
            if str(e) == "No module named admin2":
                continue
            raise e

        app_store = AppStore(module)
        apps.append(dict(
            app_name=app_name,
            obj=app_store
        ))
    return apps
