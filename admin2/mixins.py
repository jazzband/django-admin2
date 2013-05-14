# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.importlib import import_module

from admin2.exceptions import NoAdminSpecified
from admin2.forms import ModelForm
from admin2.forms.form_utils import has_digit
from admin2.forms.form_utils import make_key
from admin2.utils import translate_value
from admin2.utils import trim_field_key


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


class Admin2ViewMixin(object):

    def render_to_response(self, context, **response_kwargs):
        if hasattr(self, 'permission') and self.permission not in context:
            return HttpResponseForbidden("You do not have permissions to access this content.")

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

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

    def set_admin2_base(self):
        # TODO - probably delete
        """ Sets a number of commonly used attributes """
        if hasattr(self, "app_label"):
            # prevents us from calling this multiple times
            return None
        self.app_label = self.kwargs.get('app_label')
        self.document_name = self.kwargs.get('document_name')

        # TODO Allow this to be assigned via url variable
        self.models_name = self.kwargs.get('models_name', 'models')

        # import the models file
        self.model_name = "{0}.{1}".format(self.app_label, self.models_name)
        self.models = import_module(self.model_name)

    def set_admin2(self):
        # TODO - probably delete
        """ Returns the Admin2 object for an app_label/document_name style view
        """
        if hasattr(self, "admin2"):
            return None

        if not hasattr(self, "document_name"):
            self.set_admin2_base()

        for admin2 in self.get_admin2s():
            for model in admin2['obj'].models:
                if model.name == self.document_name:
                    self.admin2 = model.admin2
                    break
        # TODO change this to use 'finally' or 'else' or something
        if not hasattr(self, "admin2"):
            raise NoAdmin2Specified("No admin2 for {0}.{1}".format(self.app_label, self.document_name))


    def set_permissions_in_context(self, context={}):
        """ Provides permissions for admin2 for use in the context"""

        context['has_view_permission'] = self.admin2.has_view_permission(self.request)
        context['has_edit_permission'] = self.admin2.has_edit_permission(self.request)
        context['has_add_permission'] = self.admin2.has_add_permission(self.request)
        context['has_delete_permission'] = self.admin2.has_delete_permission(self.request)
        return context