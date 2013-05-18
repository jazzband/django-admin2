import os

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory
from django.views import generic
from django.db import models

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin, AccessMixin


ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")


class Admin2Mixin(object):
    def get_template_names(self):
        return [os.path.join(ADMIN2_THEME_DIRECTORY, self.default_template_name)]


class AdminModel2Mixin(Admin2Mixin, AccessMixin):
    modeladmin = None
    # Permission type to check for when a request is sent to this view.
    permission_type = None

    def dispatch(self, request, *args, **kwargs):
        # Check if user has necessary permissions. If the permission_type isn't specified then check for staff status.
        print "distpatch perm check:", self.permission_type
        has_permission = self.modeladmin.has_permission(request, self.permission_type) \
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
        context.update({
            'has_add_permission': self.modeladmin.has_add_permission(self.request),
            'has_edit_permission': self.modeladmin.has_edit_permission(self.request),
            'has_delete_permission': self.modeladmin.has_delete_permission(self.request),
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


class IndexView(Admin2Mixin, generic.TemplateView):
    default_template_name = "index.html"
    registry = None

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data.update({
            'registry': self.registry
        })
        return data

class ModelListView(AdminModel2Mixin, generic.ListView):
    default_template_name = "model_list.html"
    permission_type = 'view'

    def get_context_data(self, **kwargs):
        context = super(ModelListView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()._meta.verbose_name
        context['model_pluralized'] = self.get_model()._meta.verbose_name_plural
        return context


class ModelDetailView(AdminModel2Mixin, generic.DetailView):
    default_template_name = "model_detail.html"
    permission_type = 'view'


class ModelEditFormView(AdminModel2Mixin, generic.UpdateView):
    form_class = None
    success_url = "../../"
    default_template_name = "model_edit_form.html"
    permission_type = 'change'


class ModelAddFormView(AdminModel2Mixin, generic.CreateView):
    form_class = None
    success_url = "../"
    default_template_name = "model_add_form.html"
    permission_type = 'add'


class ModelDeleteView(AdminModel2Mixin, generic.DeleteView):
    success_url = "../../"
    default_template_name = "model_delete.html"
    permission_type = 'delete'
