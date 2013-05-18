import os

from django.conf import settings
from django.forms.models import modelform_factory
from django.views import generic
from django.db import models

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from .utils import get_admin2s

ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")

class Admin2Mixin(object):
    modeladmin = None

    def get_template_names(self):
        return [os.path.join(ADMIN2_THEME_DIRECTORY, self.default_template_name)]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        return modelform_factory(self.get_model())


class IndexView(Admin2Mixin, generic.ListView):
    default_template_name = "index.html"

    def get_queryset(self):
        return get_admin2s()


class ModelListView(Admin2Mixin, generic.ListView):
    default_template_name = "model_list.html"


class ModelDetailView(Admin2Mixin, generic.DetailView):
    default_template_name = "model_detail.html"


class ModelEditFormView(Admin2Mixin, generic.UpdateView):
    form_class = None
    success_url = "../../"
    default_template_name = "model_edit_form.html"


class ModelAddFormView(Admin2Mixin, generic.CreateView):
    form_class = None
    success_url = "../"
    default_template_name = "model_add_form.html"


class ModelDeleteView(Admin2Mixin, generic.DeleteView):
    success_url = "../../"
    default_template_name = "model_delete.html"
