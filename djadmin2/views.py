from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

import extra_views

from . import permissions
from .viewmixins import Admin2Mixin, AdminModel2Mixin, Admin2ModelFormMixin


class IndexView(Admin2Mixin, generic.TemplateView):
    default_template_name = "index.html"
    registry = None
    apps = None

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data.update({
            'apps': self.apps,
        })
        return data


class AppIndexView(Admin2Mixin, generic.TemplateView):
    default_template_name = "app_index.html"
    registry = None
    apps = None

    def get_context_data(self, **kwargs):
        data = super(AppIndexView, self).get_context_data(**kwargs)
        app_label = self.kwargs['app_label']
        registry = self.apps[app_label]

        data.update({
            'app_label': app_label,
            'registry': registry,
        })
        return data


class ModelListView(AdminModel2Mixin, generic.ListView):
    default_template_name = "model_list.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelViewPermission)

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
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelViewPermission)


class ModelEditFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.UpdateWithInlinesView):
    form_class = None
    default_template_name = "model_update_form.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelChangePermission)

    def get_context_data(self, **kwargs):
        context = super(ModelEditFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Change"
        return context


class ModelAddFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.CreateWithInlinesView):
    form_class = None
    default_template_name = "model_update_form.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelAddPermission)

    def get_context_data(self, **kwargs):
        context = super(ModelAddFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Add"
        return context


class ModelDeleteView(AdminModel2Mixin, generic.DeleteView):
    success_url = "../../"  # TODO - fix this!
    default_template_name = "model_confirm_delete.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelDeletePermission)
