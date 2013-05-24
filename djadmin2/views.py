from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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

    def post(self, request):
        # This is where we handle actions
        action_name = request.POST['action']
        action_func = self.get_actions()[action_name]['func']
        selected_model_pks = request.POST.getlist('selected_model_pk')
        queryset = self.model.objects.filter(pk__in=selected_model_pks)
        response = action_func(request, queryset)
        if response is None:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super(ModelListView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['actions'] = self.get_actions().values()
        return context

    def get_success_url(self):
        view_name = 'admin2:{}_{}_index'.format(self.app_label, self.model_name)
        return reverse(view_name)

    def get_actions(self):
        return self.model_admin.get_actions()


class ModelDetailView(AdminModel2Mixin, generic.DetailView):
    default_template_name = "model_detail.html"
    permission_type = 'view'


class ModelEditFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.UpdateWithInlinesView):
    form_class = None
    default_template_name = "model_update_form.html"
    permission_type = 'change'

    def get_context_data(self, **kwargs):
        context = super(ModelEditFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Change"
        return context


class ModelAddFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.CreateWithInlinesView):
    form_class = None
    default_template_name = "model_update_form.html"
    permission_type = 'add'

    def get_context_data(self, **kwargs):
        context = super(ModelAddFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Add"
        return context


class ModelDeleteView(AdminModel2Mixin, generic.DeleteView):
    success_url = "../../"  # TODO - fix this!
    default_template_name = "model_confirm_delete.html"
    permission_type = 'delete'
