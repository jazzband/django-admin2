# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.contrib import messages
from django.utils.translation import ugettext_lazy, pgettext_lazy

from djadmin2 import permissions
from djadmin2.actions import BaseListAction


class CustomPublishAction(BaseListAction):

    permission_classes = BaseListAction.permission_classes + (
        permissions.ModelChangePermission,
    )

    description = ugettext_lazy('Publish selected items')
    success_message = pgettext_lazy(
        'singular form',
        'Successfully published %(count)s %(items)s')
    success_message_plural = pgettext_lazy(
        'plural form',
        'Successfully published %(count)s %(items)s')

    default_template_name = "actions/publish_selected_items.html"

    def process_queryset(self):
        self.get_queryset().update(published=True)


class PublishAllItemsAction(BaseListAction):
    permission_classes = BaseListAction.permission_classes + (
        permissions.ModelChangePermission,
    )

    description = ugettext_lazy('Publish all items')
    success_message = pgettext_lazy(
        'singular form',
        'Successfully published %(count)s %(items)s',
    )

    success_message_plural = pgettext_lazy(
        'plural form',
        'Successfully published %(count)s %(items)s',
    )

    default_template_name = "model_list.html"
    only_selected = False

    def process_queryset(self):
        self.get_queryset().update(published=True)


def unpublish_items(request, queryset):
    queryset.update(published=False)
    messages.add_message(request, messages.INFO,
                         ugettext_lazy(u'Items unpublished'))


# Translators : action description
unpublish_items.description = ugettext_lazy('Unpublish selected items')


def unpublish_all_items(request, queryset):
    queryset.update(published=False)
    messages.add_message(
        request,
        messages.INFO,
        ugettext_lazy('Items unpublished'),
    )


unpublish_all_items.description = ugettext_lazy('Unpublish all items')
unpublish_all_items.only_selected = False
