from django.views import generic

import extra_views

from .viewmixins import Admin2Mixin, AdminModel2Mixin, Admin2ModelFormMixin


class IndexView(Admin2Mixin, generic.TemplateView):
    default_template_name = "index.html"
    registry = None
    apps = None

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data.update({
            'apps': self.apps,
            'registry': self.registry,
        })
        return data


class ModelListView(Admin2Mixin, generic.ListView):
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


class ModelEditFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.UpdateWithInlinesView):
    form_class = None
    default_template_name = "model_update_form.html"
    permission_type = 'change'

    def get_context_data(self, **kwargs):
        context = super(ModelEditFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()._meta.verbose_name
        context['action'] = "Change"
        return context


class ModelAddFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.CreateWithInlinesView):
    form_class = None
    default_template_name = "model_update_form.html"
    permission_type = 'add'

    def get_context_data(self, **kwargs):
        context = super(ModelAddFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()._meta.verbose_name
        context['action'] = "Add"
        return context


class ModelDeleteView(AdminModel2Mixin, generic.DeleteView):
    success_url = "../../"
    default_template_name = "model_confirm_delete.html"
    permission_type = 'delete'
