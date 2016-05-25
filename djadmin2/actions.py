# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.contrib import messages
from django.db import router
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy, ungettext, pgettext_lazy
from django.views.generic import TemplateView

from . import permissions, utils
from .viewmixins import Admin2ModelMixin


def get_description(action):
    if hasattr(action, 'description'):
        # This is for classes
        return action.description
    else:
        # This if for functions
        return capfirst(action.__name__.replace('_', ' '))


class BaseListAction(Admin2ModelMixin, TemplateView):

    permission_classes = (permissions.IsStaffPermission,)

    empty_message = ugettext_lazy(
        'Items must be selected in order to perform actions '
        'on them. No items have been changed.'
    )

    only_selected = True

    queryset = None

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.model = queryset.model

        options = utils.model_options(self.model)

        self.app_label = options.app_label
        self.model_name = options.model_name

        self.item_count = len(queryset)

        if self.item_count <= 1:
            objects_name = options.verbose_name
        else:
            objects_name = options.verbose_name_plural
        self.objects_name = force_text(objects_name)

        super(BaseListAction, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """ Replaced `get_queryset` from `Admin2ModelMixin`"""
        return self.queryset

    def description(self):
        raise NotImplementedError("List action classes require"
                                  " a description attribute.")

    @property
    def success_message(self):
        raise NotImplementedError(
            "List actions classes require a success_message"
        )

    @property
    def success_message_plural(self):
        """
        A plural form for the success_message

        If not provided, falls back to the regular form
        """
        return self.success_message

    @property
    def default_template_name(self):
        raise NotImplementedError(
            "List actions classes using display_nested_response"
            " require a template"
        )

    def get_context_data(self, **kwargs):
        """ Utility method when you want to display nested objects
            (such as during a bulk update/delete)
        """
        context = super(BaseListAction, self).get_context_data()

        def _format_callback(obj):
            opts = utils.model_options(obj)
            return '%s: %s' % (force_text(capfirst(opts.verbose_name)),
                               force_text(obj))

        using = router.db_for_write(self.model)

        collector = utils.NestedObjects(using=using)
        collector.collect(self.queryset)

        context.update({
            'view': self,
            'objects_name': self.objects_name,
            'queryset': self.queryset,
            'deletable_objects': collector.nested(_format_callback),
        })

        return context

    def get(self, request):
        if self.item_count > 0:
            return super(BaseListAction, self).get(request)

        message = _(self.empty_message)
        messages.add_message(request, messages.INFO, message)

        return None

    def post(self, request):
        if self.process_queryset() is None:

            # objects_name should already be pluralized, see __init__
            message = ungettext(
                self.success_message,
                self.success_message_plural,
                self.item_count
            ) % {
                'count': self.item_count, 'items': self.objects_name
            }

            messages.add_message(request, messages.INFO, message)

            return None

    def process_queryset(self):
        msg = 'Must be provided to do some actions with queryset'
        raise NotImplementedError(msg)


class DeleteSelectedAction(BaseListAction):
    # TODO: Check that user has permission to delete all related obejcts.  See
    # `get_deleted_objects` in contrib.admin.util for how this is currently
    # done.  (Hint: I think we can do better.)

    default_template_name = "actions/delete_selected_confirmation.html"

    description = ugettext_lazy("Delete selected items")

    success_message = pgettext_lazy(
        'singular form',
        'Successfully deleted %(count)s %(items)s',
    )
    success_message_plural = pgettext_lazy(
        'plural form',
        'Successfully deleted %(count)s %(items)s',
    )

    permission_classes = BaseListAction.permission_classes + (
        permissions.ModelDeletePermission,
    )

    def post(self, request):
        if request.POST.get('confirmed'):
            super(DeleteSelectedAction, self).post(request)
        else:
            # The user has not confirmed that they want to delete the
            # objects, so render a template asking for their confirmation.
            return self.get(request)

    def process_queryset(self):
        # The user has confirmed that they want to delete the objects.
        self.get_queryset().delete()
