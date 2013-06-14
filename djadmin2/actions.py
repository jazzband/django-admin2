from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext as _

from . import permissions, utils
from .viewmixins import AdminModel2Mixin


def get_description(action):
    if hasattr(action, 'description'):
        return action.description
    else:
        return capfirst(action.__name__.replace('_', ' '))


class BaseListAction(AdminModel2Mixin, TemplateView):

    permission_classes = (permissions.IsStaffPermission,)

    empty_message = 'Items must be selected in order to perform actions on them. No items have been changed.'
    success_message = 'Successfully deleted %d %s'

    queryset = None

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.model = queryset.model

        options = utils.model_options(self.model)

        self.app_label = options.app_label
        self.model_name = options.module_name

        self.item_count = len(queryset)

        if self.item_count <= 1:
            objects_name = options.verbose_name
        else:
            objects_name = options.verbose_name_plural
        self.objects_name = unicode(objects_name)

        super(BaseListAction, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """ Replaced `get_queryset` from `AdminModel2Mixin`"""
        return self.queryset

    def description(self):
        raise NotImplementedError("List action classes require"
                                  " a description attribute.")

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

        collector = utils.NestedObjects(using=None)
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
        if request.POST.get('confirmed'):
            if self.process_queryset() is None:

                message = _(self.success_message % (
                    self.item_count, self.objects_name)
                )
                messages.add_message(request, messages.INFO, message)

                return None
        else:
            # The user has not confirmed that they want to delete the objects, so
            # render a template asking for their confirmation.
            return self.get(request)

    def process_queryset(self):
        raise NotImplementedError('Must be provided to do some actions with queryset')


class DeleteSelectedAction(BaseListAction):
    # TODO: Check that user has permission to delete all related obejcts.  See
    # `get_deleted_objects` in contrib.admin.util for how this is currently
    # done.  (Hint: I think we can do better.)

    default_template_name = "actions/delete_selected_confirmation.html"

    description = ugettext_lazy("Delete selected items")
    permission_classes = BaseListAction.permission_classes + (
        permissions.ModelDeletePermission,
    )

    def process_queryset(self):
        # The user has confirmed that they want to delete the objects.
        self.get_queryset().delete()
