from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext as _

from . import utils


def get_description(action):
    if hasattr(action, 'description'):
        return action.description
    else:
        return capfirst(action.__name__.replace('_', ' '))


class BaseListAction(object):
    # We check whether the user has permission to delete the objects in the
    # queryset.
    #
    # TODO: This duplicates some of the permission-checking functionality in
    # BaseAdmin2.  Investigate how to DRY this out.
    #
    # TODO: Check that user has permission to delete all related obejcts.  See
    # `get_deleted_objects` in contrib.admin.util for how this is currently
    # done.  (Hint: I think we can do better.)

    def __init__(self, request, queryset):
        self.request = request
        self.queryset = queryset
        self.model = queryset.model
        self.options = utils.model_options(self.model)

        self.item_count = len(queryset)

        if self.item_count <= 1:
            objects_name = self.options.verbose_name
        else:
            objects_name = self.options.verbose_name_plural
        self.objects_name = unicode(objects_name)

    @property
    def permission_name(self):
        return NotImplemented

    def description(self):
        return NotImplemented

    def get_response(self):
        return NotImplemented

    def get_template(self):
        return NotImplemented

    def __call__(self):
        if not self.request.user.has_perm(self.permission_name):
            message = _("Permission to '%s' denied" % force_text(self.description))
            messages.add_message(self.request, messages.INFO, message)
            return None

        if self.item_count > 0:
            return self.get_response()
        else:
            message = _("Items must be selected in order to perform actions on them. No items have been changed.")
            messages.add_message(self.request, messages.INFO, message)
            return None


class DeleteSelectedAction(BaseListAction):

    description = ugettext_lazy("Delete selected items")

    # TODO - power this off the ADMIN2_THEME_DIRECTORY setting
    template = "admin2/bootstrap/actions/delete_selected_confirmation.html"

    def get_response(self):
        if self.request.POST.get('confirmed'):
            # The user has confirmed that they want to delete the objects.
            num_objects_deleted = len(self.queryset)
            self.queryset.delete()
            message = _("Successfully deleted %d %s" % \
                    (num_objects_deleted, self.objects_name))
            messages.add_message(self.request, messages.INFO, message)
            return None
        else:
            # The user has not confirmed that they want to delete the objects, so
            # render a template asking for their confirmation.

            def _format_callback(obj):
                opts = utils.model_options(obj)
                return '%s: %s' % (force_text(capfirst(opts.verbose_name)),
                                   force_text(obj))

            collector = utils.NestedObjects(using=None)
            collector.collect(self.queryset)

            context = {
                'queryset': self.queryset,
                'objects_name': self.objects_name,
                'deletable_objects': collector.nested(_format_callback),
            }
            return TemplateResponse(self.request, self.template, context)
