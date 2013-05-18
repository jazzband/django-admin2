from os.path import join

from django.conf import settings
from django.forms.models import modelform_factory
from django.views.generic import ListView, CreateView
from django.db import models

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .utils import get_admin2s

ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")


class IndexView(ListView): #(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "index.html")]

    def get_queryset(self):
        return get_admin2s()


class ModelListView(ListView):
    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_list.html")]

    def get_model(self):
        return models.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))

    def get_queryset(self):
        return self.get_model()._default_manager.all()




class ModelDetailView(DetailView):

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_detail.html")]

    def get_model(self):
        return models.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))

    def get_queryset(self):
        return self.get_model()._default_manager.all()



class ModelEditFormView(UpdateView):
    form_class = None
    success_url = "../../"

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_edit_form.html")]

    def get_model(self):
        return models.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))

    def get_queryset(self):
        return self.get_model()._default_manager.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        return modelform_factory(self.get_model())


class ModelAddFormView(CreateView):
    form_class = None
    success_url = "../"

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_add_form.html")]

    def get_model(self):
        return models.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))

    def get_queryset(self):
        return self.get_model()._default_manager.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        return modelform_factory(self.get_model())


class ModelDeleteView(DeleteView):
    success_url = "../../"

    def get_template_names(self):
        return [join(ADMIN2_THEME_DIRECTORY, "model_delete_form.html")]

    def get_model(self):
        return models.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))

    def get_queryset(self):
        return self.get_model()._default_manager.all()

