# -*- coding: utf-8 -*-:
"""
WARNING: This file about to undergo major refactoring by @pydanny per
Issue #99.
"""
from __future__ import division, absolute_import, unicode_literals

from importlib import import_module

from django.conf import settings
from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured

from . import apiviews
from . import types
from . import utils
from . import views


class Admin2(object):
    """
    The base Admin2 object.
    It keeps a registry of all registered Models and collects the urls of their
    related ModelAdmin2 instances.

    It also provides an index view that serves as an entry point to the
    admin site.
    """
    index_view = views.IndexView
    login_view = views.LoginView
    app_index_view = views.AppIndexView
    api_index_view = apiviews.IndexAPIView

    def __init__(self, name='admin2'):
        self.registry = {}
        self.apps = {}
        self.app_verbose_names = {}
        self.name = name

    def register(self, model, model_admin=None, **kwargs):
        """
        Registers the given model with the given admin class. Once a model is
        registered in self.registry, we also add it to app registries in
        self.apps.

        If no model_admin is passed, it will use ModelAdmin2. If keyword
        arguments are given they will be passed to the admin class on
        instantiation.

        If a model is already registered, this will raise ImproperlyConfigured.
        """
        if model in self.registry:
            raise ImproperlyConfigured(
                '%s is already registered in django-admin2' % model)
        if not model_admin:
            model_admin = types.ModelAdmin2
        self.registry[model] = model_admin(model, admin=self, **kwargs)

        # Add the model to the apps registry
        app_label = utils.model_options(model).app_label
        if app_label in self.apps.keys():
            self.apps[app_label][model] = self.registry[model]
        else:
            self.apps[app_label] = {model: self.registry[model]}

    def deregister(self, model):
        """
        Deregisters the given model. Remove the model from the self.app as well

        If the model is not already registered, this will raise
        ImproperlyConfigured.
        """
        try:
            del self.registry[model]
        except KeyError:
            raise ImproperlyConfigured(
                '%s was never registered in django-admin2' % model)

        # Remove the model from the apps registry
        # Get the app label
        app_label = utils.model_options(model).app_label
        # Delete the model from it's app registry
        del self.apps[app_label][model]

        # if no more models in an app's registry
        # then delete the app from the apps.
        if self.apps[app_label] is {}:
            del self.apps[app_label]  # no

    def register_app_verbose_name(self, app_label, app_verbose_name):
        """
        Registers the given app label with the given app verbose name.

        If a app_label is already registered, this will raise
        ImproperlyConfigured.
        """
        if app_label in self.app_verbose_names:
            raise ImproperlyConfigured(
                '%s is already registered in django-admin2' % app_label)

        self.app_verbose_names[app_label] = app_verbose_name

    def deregister_app_verbose_name(self, app_label):
        """
        Deregisters the given app label. Remove the app label from the
        self.app_verbose_names as well.

        If the app label is not already registered, this will raise
        ImproperlyConfigured.
        """
        try:
            del self.app_verbose_names[app_label]
        except KeyError:
            raise ImproperlyConfigured(
                '%s app label was never registered in django-admin2' % app_label)

    def autodiscover(self):
        """
        Autodiscovers all admin2.py modules for apps in INSTALLED_APPS by
        trying to import them.
        """
        for app_name in [x for x in settings.INSTALLED_APPS]:
            try:
                import_module("%s.admin2" % app_name)
            except ImportError as e:
                if str(e).startswith("No module named") and 'admin2' in str(e):
                    continue
                raise e

    def get_admin_by_name(self, name):
        """
        Returns the admin instance that was registered with the passed in
        name.
        """
        for object_admin in self.registry.values():
            if object_admin.name == name:
                return object_admin
        raise ValueError(
            u'No object admin found with name {}'.format(repr(name)))

    def get_index_kwargs(self):
        return {
            'registry': self.registry,
            'app_verbose_names': self.app_verbose_names,
            'apps': self.apps,
            'login_view': self.login_view,
        }

    def get_app_index_kwargs(self):
        return {
            'registry': self.registry,
            'app_verbose_names': self.app_verbose_names,
            'apps': self.apps,
        }

    def get_api_index_kwargs(self):
        return {
            'registry': self.registry,
            'app_verbose_names': self.app_verbose_names,
            'apps': self.apps,
        }

    def get_urls(self):
        urlpatterns = [
            url(regex=r'^$',
                view=self.index_view.as_view(**self.get_index_kwargs()),
                name='dashboard'
                ),
            url(regex='^auth/user/(?P<pk>\d+)/update/password/$',
                view=views.PasswordChangeView.as_view(),
                name='password_change'
                ),
            url(regex='^password_change_done/$',
                view=views.PasswordChangeDoneView.as_view(),
                name='password_change_done'
                ),
            url(regex='^logout/$',
                view=views.LogoutView.as_view(),
                name='logout'
                ),
            url(regex=r'^(?P<app_label>\w+)/$',
                view=self.app_index_view.as_view(
                    **self.get_app_index_kwargs()),
                name='app_index'
                ),
            url(regex=r'^api/v0/$',
                view=self.api_index_view.as_view(
                    **self.get_api_index_kwargs()),
                name='api_index'
                ),
        ]
        for model, model_admin in self.registry.items():
            model_options = utils.model_options(model)
            urlpatterns += [
                url('^{}/{}/'.format(
                    model_options.app_label,
                    model_options.object_name.lower()),
                    include(model_admin.urls)),
                url('^api/v0/{}/{}/'.format(
                    model_options.app_label,
                    model_options.object_name.lower()),
                    include(model_admin.api_urls)),
            ]
        return urlpatterns

    @property
    def urls(self):
        # We set the application and instance namespace here
        return self.get_urls(), self.name, self.name
