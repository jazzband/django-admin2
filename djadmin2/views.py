from os.path import join

from django.conf import settings

from django.forms.models import modelform_factory
from django.db import models
from django.views import generic

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from .utils import get_admin2s

ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")


class IndexView(generic.ListView): #(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "index.html")]

    def get_queryset(self):
        return get_admin2s()


class ModelListView(generic.ListView):
    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_list.html")]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()


class ModelDetailView(generic.DetailView):

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_detail.html")]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()



class ModelEditFormView(generic.UpdateView):
    form_class = None
    success_url = "../../"


    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_edit_form.html")]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()


class ModelAddFormView(generic.CreateView):
    form_class = None
    success_url = "../"

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_add_form.html")]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()


class ModelDeleteView(generic.DeleteView):
    success_url = "../../"

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_delete_form.html")]

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.get_model()._default_manager.all()
