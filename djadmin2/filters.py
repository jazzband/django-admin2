# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import collections
from itertools import chain

import django_filters
from django import forms
from django.forms import widgets as django_widgets
from django.forms.utils import flatatt
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

from .utils import type_str

LINK_TEMPLATE = '<a href=?{0}={1} {2}>{3}</a>'


class NumericDateFilter(django_filters.DateFilter):
    field_class = forms.IntegerField


class ChoicesAsLinksWidget(django_widgets.Select):
    """Select form widget taht renders links for choices
    instead of select element with options.
    """
    def render(self, name, value, attrs=None, choices=()):
        links = []
        for choice_value, choice_label in chain(self.choices, choices):
            links.append(format_html(
                LINK_TEMPLATE,
                name, choice_value, flatatt(attrs), force_text(choice_label),
            ))
        return mark_safe(u"<br />".join(links))


class NullBooleanLinksWidget(
    ChoicesAsLinksWidget,
    django_widgets.NullBooleanSelect
):
    def __init__(self, attrs=None, choices=()):
        super(ChoicesAsLinksWidget, self).__init__(attrs)
        self.choices = [
            ('1', ugettext_lazy('Unknown')),
            ('2', ugettext_lazy('Yes')),
            ('3', ugettext_lazy('No')),
        ]

#: Maps `django_filter`'s field filters types to our
#: custom form widget.
FILTER_TYPE_TO_WIDGET = {
    django_filters.BooleanFilter: NullBooleanLinksWidget,
    django_filters.ChoiceFilter: ChoicesAsLinksWidget,
    django_filters.ModelChoiceFilter: ChoicesAsLinksWidget,
}


def build_list_filter(request, model_admin, queryset):
    """Builds :class:`~django_filters.FilterSet` instance
    for :attr:`djadmin2.ModelAdmin2.Meta.list_filter` option.

    If :attr:`djadmin2.ModelAdmin2.Meta.list_filter` is not
    sequence, it's considered to be class with interface like
    :class:`django_filters.FilterSet` and its instantiate wit
    `request.GET` and `queryset`.
    """
    # if ``list_filter`` is not iterable return it right away
    if not isinstance(model_admin.list_filter, collections.Iterable):
        return model_admin.list_filter(
            request.GET,
            queryset=queryset,
        )
    # otherwise build :mod:`django_filters.FilterSet`
    filters = []
    for field_filter in model_admin.list_filter:
        if isinstance(field_filter, six.string_types):
            filters.append(get_filter_for_field_name(
                queryset.model,
                field_filter,
            ))
        else:
            filters.append(field_filter)
    filterset_dict = {}
    for field_filter in filters:
        filterset_dict[field_filter.name] = field_filter
    fields = list(filterset_dict.keys())
    filterset_dict['Meta'] = type(
        type_str('Meta'),
        (),
        {
            'model': queryset.model,
            'fields': fields,
        },
    )
    return type(type_str('%sFilterSet' % queryset.model.__name__), (django_filters.FilterSet, ), filterset_dict,)(request.GET, queryset=queryset)


def build_date_filter(request, model_admin, queryset, field_name="published_date"):
    filterset_dict = {
        "year": NumericDateFilter(
            name=field_name,
            lookup_type="year",
        ),
        "month": NumericDateFilter(
            name=field_name,
            lookup_type="month",
        ),
        "day": NumericDateFilter(
            name=field_name,
            lookup_type="day",
        )
    }

    return type(
        type_str('%sDateFilterSet' % queryset.model.__name__),
        (django_filters.FilterSet,),
        filterset_dict,
    )(request.GET, queryset=queryset)


def get_filter_for_field_name(model, field_name):
    """Returns filter for model field by field name.
    """
    filter_ = django_filters.FilterSet.filter_for_field(
        django_filters.filterset.get_model_field(model, field_name,),
        field_name,
    )
    filter_.widget = FILTER_TYPE_TO_WIDGET.get(
        filter_.__class__,
        filter_.widget,
    )
    return filter_
