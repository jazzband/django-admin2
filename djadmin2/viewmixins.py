# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import os

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from braces.views import AccessMixin

from . import settings, permissions
from .utils import admin2_urlname, model_options


class PermissionMixin(AccessMixin):
    do_not_call_in_templates = True
    permission_classes = (permissions.IsStaffPermission,)
    login_url = reverse_lazy('admin2:dashboard')

    def __init__(self, **kwargs):
        self.permissions = [
            permission_class()
            for permission_class in self.permission_classes]
        super(PermissionMixin, self).__init__(**kwargs)

    def has_permission(self, obj=None):
        '''
        Return ``True`` if the permission for this view shall be granted,
        ``False`` otherwise. Supports object-level permission by passing the
        related object as first argument.
        '''
        for permission in self.permissions:
            if not permission.has_permission(self.request, self, obj):
                return False
        return True

    def dispatch(self, request, *args, **kwargs):
        # Raise exception or redirect to login if user doesn't have
        # permissions.
        if not self.has_permission():
            if self.raise_exception:
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                    self.get_login_url(), self.get_redirect_field_name())
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PermissionMixin, self).get_context_data(**kwargs)
        permission_checker = permissions.TemplatePermissionChecker(
            self.request, self.model_admin)
        context.update({
            'permissions': permission_checker,
        })
        return context


class Admin2Mixin(PermissionMixin):
    # are set in the ModelAdmin2 class when creating the view via
    # .as_view(...)
    model_admin = None
    model_name = None
    app_label = None

    index_path = reverse_lazy('admin2:dashboard')

    def get_template_names(self):
        return [os.path.join(settings.ADMIN2_THEME_DIRECTORY, self.default_template_name)]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        return modelform_factory(self.get_model())

    def is_user(self, request):
        return hasattr(request, 'user') and not (request.user.is_active and
                                                 request.user.is_staff)

    def dispatch(self, request, *args, **kwargs):

        if self.is_user(request):
            from .views import LoginView

            if request.path == reverse('admin2:logout'):
                return HttpResponseRedirect(self.index_path)

            if request.path == self.index_path:
                extra = {
                    'next': request.GET.get('next', self.index_path)
                }
                return LoginView().dispatch(request, extra_context=extra,
                                            *args, **kwargs)

        return super(Admin2Mixin, self).dispatch(request, *args, **kwargs)


class AdminModel2Mixin(Admin2Mixin):
    model_admin = None

    def get_context_data(self, **kwargs):
        context = super(AdminModel2Mixin, self).get_context_data(**kwargs)
        model = self.get_model()
        model_meta = model_options(model)
        context.update({
            'app_label': model_meta.app_label,
            'model_name': model_meta.verbose_name,
            'model_name_pluralized': model_meta.verbose_name_plural
        })
        return context

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        return modelform_factory(self.get_model())


class Admin2ModelFormMixin(object):
    def get_success_url(self):
        if '_continue' in self.request.POST:
            view_name = admin2_urlname(self, 'update')
            return reverse(view_name, kwargs={'pk': self.object.pk})

        if '_addanother' in self.request.POST:
            return reverse(admin2_urlname(self, 'create'))

        # default to index view
        return reverse(admin2_urlname(self, 'index'))
