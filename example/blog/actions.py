from djadmin2.actions import BaseListAction
from djadmin2 import permissions

from django.utils.translation import ugettext_lazy


class CustomPublishAction(BaseListAction):

    permission_classes = BaseListAction.permission_classes + (
        permissions.ModelChangePermission,
    )

    description = ugettext_lazy('Publish selected items')
    success_message = 'Successfully published %d %s'

    default_template_name = "actions/publish_selected_items.html"

    def process_queryset(self):
        self.get_queryset().update(published=True)
