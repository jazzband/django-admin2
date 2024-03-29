import operator
from datetime import datetime
from functools import reduce

import extra_views
from django.core.exceptions import FieldDoesNotExist
from django.conf import settings
from django.contrib.auth import (logout as auth_logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import (PasswordChangeForm,
                                       AdminPasswordChangeForm)
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.contenttypes.models import ContentType
from django.db import models, router
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy
from django.urls import reverse, reverse_lazy

from django.views import generic

from . import permissions, utils
from .filters import build_list_filter, build_date_filter
from .forms import AdminAuthenticationForm
from .models import LogEntry
from .viewmixins import Admin2Mixin, Admin2ModelMixin, Admin2ModelFormMixin


class AdminView:

    def __init__(self, url, view, name=None):
        self.url = url
        self.view = view
        self.name = name

    def get_view_kwargs(self):
        return {
            'app_label': self.model_admin.app_label,
            'model': self.model_admin.model,
            'model_name': self.model_admin.model_name,
            'model_admin': self.model_admin,
        }


class IndexView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :apps: A dictionary of apps, each app being a dictionary with keys
           being models and the value being djadmin2.types.ModelAdmin2
           objects.
    :app_verbose_names: A dictionary containing the app verbose names,
                        each item has a key being the `app_label` and
                        the value being a string, (or even a lazy
                        translation object), with the custom app name.
    """
    default_template_name = "index.html"
    registry = None
    apps = None
    app_verbose_names = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'apps': self.apps,
            'app_verbose_names': self.app_verbose_names,
        })
        return data


class AppIndexView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :app_label: Name of your app
    :registry: A dictionary of registered models for a given app, each
               item has a key being the model and the value being
               djadmin2.types.ModelAdmin2 objects.
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
    """
    default_template_name = "app_index.html"
    registry = None
    apps = None
    app_verbose_names = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        app_label = self.kwargs['app_label']
        registry = self.apps[app_label]
        data.update({
            'app_label': app_label,
            'registry': registry,
            'app_verbose_names': self.app_verbose_names,
        })
        return data


class ModelListView(Admin2ModelMixin, generic.ListView):
    """Context Variables

    :is_paginated: If the page is paginated (page has a next button)
    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
    """
    default_template_name = "model_list.html"
    paginate_by = 10
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelViewPermission)

    def post(self, request):
        action_name = request.POST['action']
        action_callable = self.get_actions()[action_name]['action_callable']
        selected_model_pks = request.POST.getlist('selected_model_pk')
        if getattr(action_callable, "only_selected", True):
            queryset = self.model.objects.filter(pk__in=selected_model_pks)
        else:
            queryset = self.model.objects.all()

        #  If action_callable is a class subclassing from
        #  actions.BaseListAction then we generate the callable object.
        if hasattr(action_callable, "process_queryset"):
            response = action_callable.as_view(queryset=queryset, model_admin=self.model_admin)(request)
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
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q', None)
        search_use_distinct = False
        if self.model_admin.search_fields and search_term:
            queryset, search_use_distinct = self.get_search_results(
                queryset, search_term)

        queryset = self._modify_queryset_for_ordering(queryset)

        if self.model_admin.list_filter:
            queryset = self.build_list_filter(queryset).qs

        if self.model_admin.date_hierarchy:
            queryset = self.build_date_filter(queryset, self.model_admin.date_hierarchy).qs

        queryset = self._modify_queryset_for_sort(queryset)

        if search_use_distinct:
            return queryset.distinct()
        else:
            return queryset

    def _modify_queryset_for_ordering(self, queryset):
        ordering = self.model_admin.get_ordering(self.request)
        if ordering:
            queryset = queryset.order_by(*ordering)
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

    def build_date_filter(self, queryset=None, field_name=None):
        if not hasattr(self, "_date_filter"):
            if queryset is None:
                queryset = self.get_queryset()
            self._date_filter = build_date_filter(
                self.request,
                self.model_admin,
                queryset,
                field_name
            )

        return self._date_filter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['actions'] = self.get_actions().values()
        context['search_fields'] = self.get_search_fields()
        context['search_term'] = self.request.GET.get('q', '')
        context['list_filter'] = self.build_list_filter()
        context['sort_term'] = self.request.GET.get('sort', '')

        if self.model_admin.date_hierarchy:
            year = self.request.GET.get("year", False)
            month = self.request.GET.get("month", False)
            day = self.request.GET.get("day", False)

            if year and month and day:
                new_date = datetime.strptime(
                    "%s %s %s" % (month, day, year),
                    "%m %d %Y",
                )
                context["previous_date"] = {
                    "link": "?year=%s&month=%s" % (year, month),
                    "text": "‹ %s" % new_date.strftime("%B %Y")
                }

                context["active_day"] = new_date.strftime("%B %d")

                context["dates"] = self._format_days(self.get_queryset())
            elif year and month:
                context["previous_date"] = {
                    "link": "?year=%s" % (year),
                    "text": "‹ %s" % year,
                }

                context["dates"] = self._format_days(self.get_queryset())
            elif year:
                context["previous_date"] = {
                    "link": "?",
                    "text": gettext_lazy("‹ All dates"),
                }

                context["dates"] = self._format_months(self.get_queryset())
            else:
                context["dates"] = self._format_years(self.get_queryset())

        return context

    def _format_years(self, queryset):
        years = self._qs_date_or_datetime(queryset, 'year')
        if len(years) == 1:
            return self._format_months(queryset)
        else:
            return [
                (("?year=%s" % year.strftime("%Y")), year.strftime("%Y"))
                for year in
                self._qs_date_or_datetime(queryset, 'year')
            ]

    def _format_months(self, queryset):
        return [
            (
                "?year=%s&month=%s" % (
                    date.strftime("%Y"), date.strftime("%m")
                ),
                date.strftime("%B %Y")
            ) for date in
            self._qs_date_or_datetime(queryset, 'month')
        ]

    def _format_days(self, queryset):
        return [
            (
                "?year=%s&month=%s&day=%s" % (
                    date.strftime("%Y"),
                    date.strftime("%m"),
                    date.strftime("%d"),
                ),
                date.strftime("%B %d")
            ) for date in
            self._qs_date_or_datetime(queryset, 'day')
        ]

    def _qs_date_or_datetime(self, object_list, type):
        if isinstance(self.model._meta.get_field(self.model_admin.date_hierarchy), models.DateTimeField):
            qs = object_list.datetimes(self.model_admin.date_hierarchy, type)
        else:
            qs = object_list.dates(self.model_admin.date_hierarchy, type)
        return qs

    def get_success_url(self):
        view_name = 'admin2:{}_{}_index'.format(
            self.app_label, self.model_name)
        return reverse(view_name)

    def get_actions(self):
        return self.model_admin.get_list_actions()

    def get_search_fields(self):
        return self.model_admin.search_fields


class ModelDetailView(Admin2ModelMixin, generic.DetailView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
    """
    default_template_name = "model_detail.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelViewPermission)


class ModelEditFormView(Admin2ModelMixin, Admin2ModelFormMixin,
                        extra_views.UpdateWithInlinesView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
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
        context['action_name'] = gettext_lazy("Change")
        return context

    def forms_valid(self, form, inlines):
        response = super(ModelEditFormView, self).forms_valid(form, inlines)
        LogEntry.objects.log_action(
            self.request.user.id,
            self.object,
            LogEntry.CHANGE,
            self.construct_change_message(self.request, form, inlines))
        return response


class ModelAddFormView(Admin2ModelMixin, Admin2ModelFormMixin,
                       extra_views.CreateWithInlinesView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
    """
    form_class = None
    default_template_name = "model_update_form.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelAddPermission)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['action'] = "Add"
        context['action_name'] = gettext_lazy("Add")
        return context

    def forms_valid(self, form, inlines):
        response = super().forms_valid(form, inlines)
        LogEntry.objects.log_action(
            self.request.user.id,
            self.object,
            LogEntry.ADDITION,
            'Object created.')
        return response


class ModelDeleteView(Admin2ModelMixin, generic.DeleteView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :deletable_objects: Objects to delete
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
    """
    success_url = "../../"  # TODO - fix this!
    default_template_name = "model_confirm_delete.html"
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelDeletePermission)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def _format_callback(obj):
            opts = utils.model_options(obj)
            return '%s: %s' % (force_str(capfirst(opts.verbose_name)),
                               force_str(obj))

        using = router.db_for_write(self.get_object()._meta.model)
        collector = utils.NestedObjects(using=using)
        collector.collect([self.get_object()])
        context.update({
            'deletable_objects': collector.nested(_format_callback)
        })
        return context

    def delete(self, request, *args, **kwargs):
        LogEntry.objects.log_action(
            request.user.id,
            self.get_object(),
            LogEntry.DELETION,
            'Object deleted.')
        return super().delete(request, *args, **kwargs)


class ModelHistoryView(Admin2ModelMixin, generic.ListView):
    """Context Variables

    :model: Type of object you are editing
    :model_name: Name of the object you are editing
    :app_label: Name of your app
    :app_verbose_names: A dictionary containing the app verbose name for
                        a given app, the item has a key being the
                        `app_label` and the value being a string, (or
                        even a lazy translation object), with the custom
                        app name.
    """
    default_template_name = "model_history.html"
    paginate_by = 10
    permission_classes = (
        permissions.IsStaffPermission,
        permissions.ModelChangePermission
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['object'] = self.get_object()
        return context

    def get_object(self):
        return get_object_or_404(self.get_model(), pk=self.kwargs.get('pk'))

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(self.get_object())
        return LogEntry.objects.filter(
            content_type=content_type,
            object_id=self.get_object().id
        )


class PasswordChangeView(Admin2Mixin, generic.UpdateView):

    default_template_name = 'auth/password_change_form.html'
    form_class = AdminPasswordChangeForm
    admin_form_class = PasswordChangeForm
    model = settings.AUTH_USER_MODEL
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
        return super().get_form_class()

    def get_queryset(self):
        from django.contrib.auth import get_user_model
        return get_user_model()._default_manager.all()

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user == self.get_object():
            update_session_auth_hash(self.request, form.user)
        return HttpResponseRedirect(self.get_success_url())


class PasswordChangeDoneView(Admin2Mixin, generic.TemplateView):

    default_template_name = 'auth/password_change_done.html'


class LoginView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :site_name: Name of the site
    """

    default_template_name = 'auth/login.html'
    authentication_form = AdminAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        return DjangoLoginView.as_view(template_name=self.get_templates(), authentication_form=self.authentication_form, *args, **kwargs)(request)


class LogoutView(Admin2Mixin, generic.TemplateView):
    """Context Variables

    :site_name: Name of the site
    """

    default_template_name = 'auth/logout.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
