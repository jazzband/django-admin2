# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import operator

from django.contrib.auth.forms import (PasswordChangeForm,
                                       AdminPasswordChangeForm)
from django.contrib.auth.views import (logout as auth_logout,
                                       login as auth_login)
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.views import generic
from django.db.models.fields import FieldDoesNotExist

import extra_views


from . import permissions, utils
from .forms import AdminAuthenticationForm
from .viewmixins import Admin2Mixin, AdminModel2Mixin, Admin2ModelFormMixin
from .filters import build_list_filter


class IndexView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :apps: A dictionary of apps, each app being a dictionary with keys
           being models and the value being djadmin2.types.ModelAdmin2
           objects.
    """
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
    """Context Variables

    :is_paginated: If the page is paginated (page has a next button)
    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    """
    default_template_name = "model_list.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelViewPermission)

    def post(self, request):
        action_name = request.POST['action']
        action_callable = self.get_actions()[action_name]['action_callable']
        selected_model_pks = request.POST.getlist('selected_model_pk')
        queryset = self.model.objects.filter(pk__in=selected_model_pks)

        #  If action_callable is a class subclassing from actions.BaseListAction
        #       then we generate the callable object.
        if hasattr(action_callable, "process_queryset"):
            response = action_callable.as_view(queryset=queryset)(request)
        else:
            # generate the reponse if a function.
            response = action_callable(request, queryset)

        if response is None:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return response

    def get_search_results(self, queryset, search_term):
        # Lifted from django.contrib.admin
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        use_distinct = False

        orm_lookups = [construct_search(str(search_field))
                       for search_field in self.model_admin.search_fields]

        for bit in search_term.split():
            or_queries = [models.Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups]
            queryset = queryset.filter(reduce(operator.or_, or_queries))

        if not use_distinct:
            for search_spec in orm_lookups:
                opts = utils.model_options(self.get_model())
                if utils.lookup_needs_distinct(opts, search_spec):
                    use_distinct = True
                    break

        return queryset, use_distinct

    def get_queryset(self):
        queryset = super(ModelListView, self).get_queryset()
        search_term = self.request.GET.get('q', None)
        search_use_distinct = False
        if self.model_admin.search_fields and search_term:
            queryset, search_use_distinct = self.get_search_results(queryset, search_term)

        if self.model_admin.list_filter:
            queryset = self.build_list_filter(queryset).qs

        queryset = self._modify_queryset_for_sort(queryset)

        if search_use_distinct:
            return queryset.distinct()
        else:
            return queryset

    def _modify_queryset_for_sort(self, queryset):
        # If we are sorting AND the field exists on the model
        sort_by = self.request.GET.get('sort', None)
        if sort_by:
            # Special case when we are not explicityly displaying fields
            if sort_by == '-__str__':
                queryset = queryset[::-1]
            try:
                # If we sort on '-' remove it before looking for that field
                field_exists = sort_by
                if field_exists[0] == '-':
                    field_exists = field_exists[1:]

                options = utils.model_options(self.model)
                options.get_field(field_exists)
                queryset = queryset.order_by(sort_by)
            except FieldDoesNotExist:
                # If the field does not exist then we dont sort on it
                pass
        return queryset

    def build_list_filter(self, queryset=None):
        if not hasattr(self, '_list_filter'):
            if queryset is None:
                queryset = self.get_queryset()
            self._list_filter = build_list_filter(
                self.request,
                self.model_admin,
                queryset,
            )
        return self._list_filter

    def get_context_data(self, **kwargs):
        context = super(ModelListView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['actions'] = self.get_actions().values()
        context['search_fields'] = self.get_search_fields()
        context['search_term'] = self.request.GET.get('q', '')
        context['list_filter'] = self.build_list_filter()
        context['sort_term'] = self.request.GET.get('sort', '')
        return context

    def get_success_url(self):
        view_name = 'admin2:{}_{}_index'.format(self.app_label, self.model_name)
        return reverse(view_name)

    def get_actions(self):
        return self.model_admin.get_list_actions()

    def get_search_fields(self):
        return self.model_admin.search_fields


class ModelDetailView(AdminModel2Mixin, generic.DetailView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    """
    default_template_name = "model_detail.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelViewPermission)


class ModelEditFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.UpdateWithInlinesView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    """
    form_class = None
    default_template_name = "model_update_form.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelChangePermission)

    def get_context_data(self, **kwargs):
        context = super(ModelEditFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Change"
        context['action_name'] = ugettext_lazy("Change")
        return context


class ModelAddFormView(AdminModel2Mixin, Admin2ModelFormMixin, extra_views.CreateWithInlinesView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    """
    form_class = None
    default_template_name = "model_update_form.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelAddPermission)

    def get_context_data(self, **kwargs):
        context = super(ModelAddFormView, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Add"
        context['action_name'] = ugettext_lazy("Add")
        return context


class ModelDeleteView(AdminModel2Mixin, generic.DeleteView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :deletable_objects: Objects to delete
    """
    success_url = "../../"  # TODO - fix this!
    default_template_name = "model_confirm_delete.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelDeletePermission)

    def get_context_data(self, **kwargs):
        context = super(ModelDeleteView, self).get_context_data(**kwargs)

        def _format_callback(obj):
            opts = utils.model_options(obj)
            return '%s: %s' % (force_text(capfirst(opts.verbose_name)),
                               force_text(obj))

        collector = utils.NestedObjects(using=None)
        collector.collect([self.get_object()])
        context.update({
            'deletable_objects': collector.nested(_format_callback)
        })
        return context


class PasswordChangeView(Admin2Mixin, generic.UpdateView):

    default_template_name = 'auth/password_change_form.html'
    form_class = AdminPasswordChangeForm
    admin_form_class = PasswordChangeForm
    model = get_user_model()
    success_url = reverse_lazy('admin2:password_change_done')

    def get_form_kwargs(self, **kwargs):
        data = {'user': self.get_object()}

        if self.request.method in ('POST', 'PUT'):
            data.update({
                'data': self.request.POST
            })

        return data

    def get_form_class(self):
        if self.request.user == self.get_object():
            return self.admin_form_class
        return super(PasswordChangeView, self).get_form_class()


class PasswordChangeDoneView(Admin2Mixin, generic.TemplateView):

    default_template_name = 'auth/password_change_done.html'


class LoginView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :site_name: Name of the site
    """

    default_template_name = 'auth/login.html'
    authentication_form = AdminAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        return auth_login(request,
                          authentication_form=self.authentication_form,
                          template_name=self.get_template_names(),
                          *args, **kwargs)


class LogoutView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :site_name: Name of the site
    """

    default_template_name = 'auth/logout.html'

    def get(self, request, *args, **kwargs):
        return auth_logout(request, template_name=self.get_template_names(),
                           *args, **kwargs)
