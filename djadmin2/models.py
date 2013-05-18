"""

For wont of a better name, this module is called 'models'. It's role is
synonymous with the django.contrib.admin.sites model.

"""


try:
    import floppyforms as forms
except ImportError:
    from django import forms


class BaseAdmin2(object):

    search_fields = []

    # Show the fields to be displayed as columns
    # TODO: Confirm that this is what the Django admin uses
    list_fields = []

    #This shows up on the DocumentListView of the Posts
    list_actions = []

    # This shows up in the DocumentDetailView of the Posts.
    document_actions = []

    # shows up on a particular field
    field_actions = {}

    fields = None
    exclude = None
    fieldsets = None
    form = forms.ModelForm
    filter_vertical = ()
    filter_horizontal = ()
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = ()
    ordering = None


    # TODO: make the model argument required after the registration code has been refactored.
    # def __init__(self, model):
    def __init__(self, model=None):
        super(BaseAdmin2, self).__init__()

        self.model = model


    def _user_has_permission(self, user, permission_type, obj=None):
        """ Generic method for checking whether the user has permission of specified type for the model.
        Type can be one of view, add, change, delete.
        You can also specify instance of the model for object-specific permission check.
        """
        if not user.is_authenticated() or not user.is_staff:
            return False
        opts = self.model._meta
        full_permission_name = '%s.%s_%s' % (opts.app_label, permission_type, opts.object_name.lower())
        return user.has_perm(full_permission_name, obj)

    def has_view_permission(self, request, obj=None):
        """ Can view this object """
        return self._user_has_permission(request.user, 'view', obj)

    def has_edit_permission(self, request, obj=None):
        """ Can edit this object """
        return self._user_has_permission(request.user, 'change', obj)

    def has_add_permission(self, request, obj=None):
        """ Can add this object """
        return self._user_has_permission(request.user, 'add', obj)

    def has_delete_permission(self, request, obj=None):
        """ Can delete this object """
        return self._user_has_permission(request.user, 'delete', obj)


class Admin2(BaseAdmin2):

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
