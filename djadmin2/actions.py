from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.text import capfirst

from . import utils


def get_description(action):
    if hasattr(action, 'description'):
        return action.description
    else:
        return capfirst(action.__name__.replace('_', ' '))


def delete_selected(request, queryset):
    # We check whether the user has permission to delete the objects in the
    # queryset.
    #
    # TODO: This duplicates some of the permission-checking functionality in
    # BaseAdmin2.  Investigate how to DRY this out.
    #
    # TODO: Check that user has permission to delete all related obejcts.  See
    # `get_deleted_objects` in contrib.admin.util for how this is currently
    # done.  (Hint: I think we can do better.)

    model = queryset.model
    opts = utils.model_options(model)
    permission_name = '%s.delete.%s' \
            % (opts.app_label, opts.object_name.lower())
    has_permission = request.user.has_perm(permission_name)

    if len(queryset) == 1:
        objects_name = opts.verbose_name
    else:
        objects_name = opts.verbose_name_plural
    objects_name = unicode(objects_name)

    if request.POST.get('confirmed'):
        # The user has confirmed that they want to delete the objects.
        if has_permission:
            num_objects_deleted = len(queryset)
            queryset.delete()
            message = "Successfully deleted %d %s" % \
                    (num_objects_deleted, objects_name)
            messages.add_message(request, messages.INFO, message)
            return None
        else:
            raise PermissionDenied
    else:
        # The user has not confirmed that they want to delete the objects, so
        # render a template asking for their confirmation.
        if has_permission:
            template = 'admin2/bootstrap/delete_selected_confirmation.html'

            def _format_callback(obj):
                opts = utils.model_options(obj)
                return '%s: %s' % (force_text(capfirst(opts.verbose_name)),
                                   force_text(obj))

            collector = utils.NestedObjects(using=None)
            collector.collect(queryset)

            context = {
                'queryset': queryset,
                'objects_name': objects_name,
                'deletable_objects': collector.nested(_format_callback),
            }
            return TemplateResponse(request, template, context)
        else:
            message = "Permission to delete %s denied" % objects_name
            messages.add_message(request, messages.INFO, message)
            return None

delete_selected.description = "Delete selected items"
