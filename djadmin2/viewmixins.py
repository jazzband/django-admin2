import os

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory

from braces.views import AccessMixin

from . import constants
from .utils import admin2_urlname, model_options


class Admin2Mixin(object):
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
    # Permission type to check for when a request is sent to this view.
    permission_type = None

    def dispatch(self, request, *args, **kwargs):
        # Check if user has necessary permissions. If the permission_type isn't specified then check for staff status.
        has_permission = self.model_admin.has_permission(request, self.permission_type) \
            if self.permission_type else request.user.is_staff
        # Raise exception or redirect to login if user doesn't have permissions.
        if not has_permission:
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
            'has_add_permission': self.model_admin.has_add_permission(self.request),
            'has_edit_permission': self.model_admin.has_edit_permission(self.request),
            'has_delete_permission': self.model_admin.has_delete_permission(self.request),
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
