import os

from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms.models import modelform_factory
from django.views import generic
from django.db import models

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin


ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")

class Admin2Mixin(object):
    modeladmin = None
    model_name = None
    app_label = None

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


class IndexView(Admin2Mixin, generic.TemplateView):
    default_template_name = "index.html"
    registry = None

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data.update({
            'registry': self.registry
        })
        return data


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

    def get_success_url(self):
        view_name = 'admin2:{}_{}_detail'.format(self.app_label, self.model_name)
        return reverse(view_name, kwargs={'pk': self.object.pk})


class ModelDeleteView(Admin2Mixin, generic.DeleteView):
    success_url = "../../"
    default_template_name = "model_delete.html"
