# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import os

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.text import get_text_list
from django.utils.translation import ugettext as _

# braces 1.3 views exported AccessMixin
# in braces 1.4 this was moved views._access and not exported in views
# not sure if this was the intent of braces or an oversight
# if intent - should look at AccessMixin vs. using a more specific mixin
try:
    from braces.views import AccessMixin
except ImportError:
    from braces.views._access import AccessMixin

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
                return redirect_to_login(
                    request.get_full_path(),
                    self.get_login_url(),
                    self.get_redirect_field_name())
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
    login_view = None

    index_path = reverse_lazy('admin2:dashboard')

    def get_template_names(self):
        return [os.path.join(
            settings.ADMIN2_THEME_DIRECTORY, self.default_template_name)]

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
            if request.path == reverse('admin2:logout'):
                return HttpResponseRedirect(self.index_path)

            if request.path == self.index_path:
                extra = {
                    'next': request.GET.get('next', self.index_path)
                }
                return self.login_view().dispatch(request, extra_context=extra, *args, **kwargs)

        return super(Admin2Mixin, self).dispatch(request, *args, **kwargs)


class Admin2ModelMixin(Admin2Mixin):
    model_admin = None

    def get_context_data(self, **kwargs):
        context = super(Admin2ModelMixin, self).get_context_data(**kwargs)
        model = self.get_model()
        model_meta = model_options(model)
        app_verbose_names = self.model_admin.admin.app_verbose_names
        context.update({
            'app_label': model_meta.app_label,
            'app_verbose_name': app_verbose_names.get(model_meta.app_label),
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
        return modelform_factory(self.get_model(), fields='__all__')


class Admin2ModelFormMixin(object):
    def get_success_url(self):
        if '_continue' in self.request.POST:
            view_name = admin2_urlname(self, 'update')
            return reverse(view_name, kwargs={'pk': self.object.pk})

        if '_addanother' in self.request.POST:
            return reverse(admin2_urlname(self, 'create'))

        # default to index view
        return reverse(admin2_urlname(self, 'index'))

    def construct_change_message(self, request, form, formsets):
        """ Construct a change message from a changed object """
        change_message = []
        if form.changed_data:
            change_message.append(
                _('Changed {0}.'.format(
                    get_text_list(form.changed_data, _('and')))))

        if formsets:
            for formset in formsets:
                for added_object in formset.new_objects:
                    change_message.append(
                        _('Added {0} "{1}".'.format(
                            force_text(added_object._meta.verbose_name),
                            force_text(added_object))))
                for changed_object, changed_fields in formset.changed_objects:
                    change_message.append(
                        _('Changed {0} for {1} "{2}".'.format(
                            get_text_list(changed_fields, _('and')),
                            force_text(changed_object._meta.verbose_name),
                            force_text(changed_object))))
                for deleted_object in formset.deleted_objects:
                    change_message.append(
                        _('Deleted {0} "{1}".'.format(
                            force_text(deleted_object._meta.verbose_name),
                            force_text(deleted_object))))

        change_message = ' '.join(change_message)
        return change_message or _('No fields changed.')
