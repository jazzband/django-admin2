# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from collections import namedtuple
import logging
import os

from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url

import extra_views

from . import apiviews
from . import settings
from . import views
from . import actions
from . import utils
from .forms import modelform_factory


logger = logging.getLogger('djadmin2')


class ModelAdmin2(object):
    """
    Adding new ModelAdmin2 attributes:

        Step 1: Add the attribute to this class
        Step 2: Add the attribute to djadmin2.settings.MODEL_ADMIN_ATTRS

        Reasoning:

            Changing values on ModelAdmin2 objects or their attributes from
            within a view results in leaky scoping issues. Therefore, we use
            the immutable_admin_factory to render the ModelAdmin2 class
            practically immutable before passing it to the view. To constrain
            things further (in order to protect ourselves from causing
            hard-to-find security problems), we also restrict which attrs are
            passed to the final ImmutableAdmin object (i.e. a namedtuple).
            This prevents us from easily implementing methods/setters which
            bypass the blocking features of the ImmutableAdmin.
    """

    list_display = ('__str__',)
    list_display_links = ()
    list_filter = ()
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ()
    search_fields = ()
    save_as = False
    save_on_top = False
    verbose_name = None
    verbose_name_plural = None
    model_admin_attributes = settings.MODEL_ADMIN_ATTRS
    save_on_top = False
    save_on_bottom = True

    # Not yet implemented. See #267 and #268
    actions_on_bottom = False
    actions_on_top = True

    search_fields = []

    # Show the fields to be displayed as columns
    # TODO: Confirm that this is what the Django admin uses
    list_fields = []

    # This shows up on the DocumentListView of the Posts
    list_actions = [actions.DeleteSelectedAction]

    # This shows up in the DocumentDetailView of the Posts.
    document_actions = []

    # Shows up on a particular field
    field_actions = {}

    # Defines custom field renderers
    field_renderers = {}

    fields = None
    exclude = None
    fieldsets = None
    form_class = None
    filter_vertical = ()
    filter_horizontal = ()
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = ()
    ordering = None

    create_form_class = None
    update_form_class = None

    inlines = []

    #  Views
    index_view = views.ModelListView
    create_view = views.ModelAddFormView
    update_view = views.ModelEditFormView
    detail_view = views.ModelDetailView
    delete_view = views.ModelDeleteView
    history_view = views.ModelHistoryView

    # API configuration
    api_serializer_class = None

    # API Views
    api_list_view = apiviews.ListCreateAPIView
    api_detail_view = apiviews.RetrieveUpdateDestroyAPIView

    def __init__(self, model, admin, name=None, **kwargs):
        self.name = name
        self.model = model
        self.admin = admin
        model_options = utils.model_options(model)
        self.app_label = model_options.app_label
        self.model_name = model_options.object_name.lower()

        if self.name is None:
            self.name = '{}_{}'.format(self.app_label, self.model_name)

        if self.verbose_name is None:
            self.verbose_name = model_options.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = model_options.verbose_name_plural

    def get_default_view_kwargs(self):
        return {
            'app_label': self.app_label,
            'model': self.model,
            'model_name': self.model_name,
            'model_admin': immutable_admin_factory(self),
        }

    def get_default_api_view_kwargs(self):
        kwargs = self.get_default_view_kwargs()
        kwargs.update({
            'serializer_class': self.api_serializer_class,
        })
        return kwargs

    def get_prefixed_view_name(self, view_name):
        return '{}_{}'.format(self.name, view_name)

    def get_index_kwargs(self):
        return self.get_default_view_kwargs()

    def get_create_kwargs(self):
        kwargs = self.get_default_view_kwargs()
        kwargs.update({
            'inlines': self.inlines,
            'form_class': (self.create_form_class if
                           self.create_form_class else self.form_class),
        })
        return kwargs

    def get_update_kwargs(self):
        kwargs = self.get_default_view_kwargs()
        form_class = (self.update_form_class if
                      self.update_form_class else self.form_class)
        if form_class is None:
            form_class = modelform_factory(self.model)
        kwargs.update({
            'inlines': self.inlines,
            'form_class': form_class,
        })
        return kwargs

    def get_detail_kwargs(self):
        return self.get_default_view_kwargs()

    def get_delete_kwargs(self):
        return self.get_default_view_kwargs()

    def get_history_kwargs(self):
        return self.get_default_view_kwargs()

    def get_index_url(self):
        return reverse('admin2:{}'.format(
            self.get_prefixed_view_name('index')))

    def get_api_list_kwargs(self):
        kwargs = self.get_default_api_view_kwargs()
        kwargs.update({
            'paginate_by': self.list_per_page,
        })
        return kwargs

    def get_api_detail_kwargs(self):
        return self.get_default_api_view_kwargs()

    def get_urls(self):
        return patterns(
            '',
            url(
                regex=r'^$',
                view=self.index_view.as_view(**self.get_index_kwargs()),
                name=self.get_prefixed_view_name('index')
            ),
            url(
                regex=r'^create/$',
                view=self.create_view.as_view(**self.get_create_kwargs()),
                name=self.get_prefixed_view_name('create')
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/$',
                view=self.detail_view.as_view(**self.get_detail_kwargs()),
                name=self.get_prefixed_view_name('detail')
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/update/$',
                view=self.update_view.as_view(**self.get_update_kwargs()),
                name=self.get_prefixed_view_name('update')
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/delete/$',
                view=self.delete_view.as_view(**self.get_delete_kwargs()),
                name=self.get_prefixed_view_name('delete')
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/history/$',
                view=self.history_view.as_view(**self.get_history_kwargs()),
                name=self.get_prefixed_view_name('history')
            )
        )

    def get_api_urls(self):
        return patterns(
            '',
            url(
                regex=r'^$',
                view=self.api_list_view.as_view(**self.get_api_list_kwargs()),
                name=self.get_prefixed_view_name('api_list'),
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/$',
                view=self.api_detail_view.as_view(
                    **self.get_api_detail_kwargs()),
                name=self.get_prefixed_view_name('api_detail'),
            ),
        )

    @property
    def urls(self):
        # We set the application and instance namespace here
        return self.get_urls(), None, None

    @property
    def api_urls(self):
        return self.get_api_urls(), None, None

    def get_list_actions(self):
        actions_dict = {}

        for cls in type(self).mro()[::-1]:
            class_actions = getattr(cls, 'list_actions', [])
            for action in class_actions:
                actions_dict[action.__name__] = {
                    'name': action.__name__,
                    'description': actions.get_description(action),
                    'action_callable': action
                }
        return actions_dict


class Admin2Inline(extra_views.InlineFormSet):
    """
    A simple extension of django-extra-view's InlineFormSet that
    adds some useful functionality.
    """
    template = None

    def construct_formset(self):
        """
        Overrides construct_formset to attach the model class as
        an attribute of the returned formset instance.
        """
        formset = super(Admin2Inline, self).construct_formset()
        formset.model = self.inline_model
        formset.template = self.template
        return formset


class Admin2TabularInline(Admin2Inline):
    template = os.path.join(
        settings.ADMIN2_THEME_DIRECTORY, 'edit_inlines/tabular.html')


class Admin2StackedInline(Admin2Inline):
    template = os.path.join(
        settings.ADMIN2_THEME_DIRECTORY, 'edit_inlines/stacked.html')


def immutable_admin_factory(model_admin):
    """
    Provide an ImmutableAdmin to make it harder for developers to
    dig themselves into holes.
    See https://github.com/twoscoops/django-admin2/issues/99
    Frozen class implementation as namedtuple suggested by Audrey Roy

    Note: This won't stop developers from saving mutable objects to
    the result, but hopefully developers attempting that
    'workaround/hack' will read our documentation.
    """
    ImmutableAdmin = namedtuple('ImmutableAdmin',
                                model_admin.model_admin_attributes,
                                verbose=False)
    return ImmutableAdmin(*[getattr(
        model_admin, x) for x in model_admin.model_admin_attributes])
