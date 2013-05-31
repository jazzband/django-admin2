from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy, ugettext as _

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
        self.permission_name = '%s.delete.%s' \
                % (self.options.app_label, self.options.object_name.lower())
        self.has_permission = request.user.has_perm(self.permission_name)
        if queryset.count() == 1:
            objects_name = self.options.verbose_name
        else:
            objects_name = self.options.verbose_name_plural
        self.objects_name = unicode(objects_name)

    def description(self):
        return NotImplemented

    def get_response(self):
        return NotImplemented

    def get_template(self):
        return NotImplemented

    def __call__(self):
        return self.get_response()


class DeleteSelectedAction(BaseListAction):

    description = ugettext_lazy("Delete selected items")

    def get_response(self):
        if self.request.POST.get('confirmed'):
            # The user has confirmed that they want to delete the objects.
            if self.has_permission:
                num_objects_deleted = len(self.queryset)
                self.queryset.delete()
                message = _("Successfully deleted %d %s" % \
                        (num_objects_deleted, self.objects_name))
                messages.add_message(self.request, messages.INFO, message)
                return None
            else:
                raise PermissionDenied
        else:
            # The user has not confirmed that they want to delete the objects, so
            # render a template asking for their confirmation.
            if self.has_permission:
                template = 'admin2/bootstrap/actions/delete_selected_confirmation.html'

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
                return TemplateResponse(self.request, template, context)
            else:
                message = _("Permission to delete %s denied" % self.objects_name)
                messages.add_message(self.request, messages.INFO, message)
                return None
