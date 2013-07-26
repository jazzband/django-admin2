# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from djadmin2.actions import BaseListAction
from djadmin2 import permissions

from django.utils.translation import ugettext_lazy, pgettext_lazy


class CustomPublishAction(BaseListAction):

    permission_classes = BaseListAction.permission_classes + (
        permissions.ModelChangePermission,
    )

    description = ugettext_lazy('Publish selected items')
    success_message = pgettext_lazy('singular form',
            'Successfully published %(count)s %(items)s')
    success_message_plural = pgettext_lazy('plural form',
            'Successfully published %(count)s %(items)s')

    default_template_name = "actions/publish_selected_items.html"

    def process_queryset(self):
        self.get_queryset().update(published=True)
