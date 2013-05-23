import os

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory

from braces.views import AccessMixin

from . import constants, permissions
from .utils import admin2_urlname, model_options


class PermissionMixin(object):
    permission_classes = (permissions.IsStaffPermission,)

    def __init__(self, **kwargs):
        self.permissions = [
            permission_class()
            for permission_class in self.permission_classes]
        super(PermissionMixin, self).__init__(**kwargs)

    def has_permission(self, obj=None, view_name=None):
        '''
        Return ``True`` if the permission for this view shall be granted,
        ``False`` otherwise. Supports object-level permission by passing the
        related object as first argument.

        You can also check for the permission of a different view in the same
        ``ModelAdmin2`` by passing in the attribute name which holds the view
        in the ``ModelAdmin2`` instance.
        '''
        if view_name:
            view_class = getattr(self.model_admin, view_name)
            view = view_class(
                request=self.request,
                **self.model_admin.get_default_view_kwargs())
            return view.has_permission(obj)
        for backend in self.permissions:
            if not backend.has_permission(self.request, self, obj):
                return False
        return True


class Admin2Mixin(PermissionMixin):
    # are set in the ModelAdmin2 class when creating the view via
    # .as_view(...)
    model_admin = None
    model_name = None
    app_label = None

    def get_template_names(self):
        return [os.path.join(constants.ADMIN2_THEME_DIRECTORY, self.default_template_name)]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        return modelform_factory(self.get_model())


class AdminModel2Mixin(Admin2Mixin, AccessMixin):
    model_admin = None

    def dispatch(self, request, *args, **kwargs):
        # Raise exception or redirect to login if user doesn't have
        # permissions.
        if not self.has_permission():
            if self.raise_exception:
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                    self.get_login_url(), self.get_redirect_field_name())
        return super(AdminModel2Mixin, self).dispatch(request, *args, **kwargs)

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
