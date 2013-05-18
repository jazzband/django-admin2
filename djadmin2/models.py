"""

For wont of a better name, this module is called 'models'. It's role is
synonymous with the django.contrib.admin.sites model.

"""
from django.conf.urls import patterns, include, url
from django.contrib.auth import models as auth_app
from django.db.models import get_models, signals

from djadmin2 import views

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
    form_class = None
    filter_vertical = ()
    filter_horizontal = ()
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = ()
    ordering = None


    def __init__(self, model):
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

    def has_permission(self, request, permission_type, obj=None):
        return self._user_has_permission(request.user, permission_type, obj)

    def has_view_permission(self, request, obj=None):
        """ Can view this object """
        return self.has_permission(request, 'view', obj)

    def has_edit_permission(self, request, obj=None):
        """ Can edit this object """
        return self.has_permission(request, 'change', obj)

    def has_add_permission(self, request, obj=None):
        """ Can add this object """
        return self.has_permission(request, 'add', obj)

    def has_delete_permission(self, request, obj=None):
        """ Can delete this object """
        return self.has_permission(request, 'delete', obj)


class ModelAdmin2(BaseAdmin2):
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
    verbose_name = None
    verbose_name_plural = None

    create_form_class = None
    update_form_class = None

    #  Views
    index_view = views.ModelListView
    create_view = views.ModelAddFormView
    update_view = views.ModelEditFormView
    detail_view = views.ModelDetailView
    delete_view = views.ModelDeleteView

    def __init__(self, model, **kwargs):
        self.model = model

        if self.verbose_name is None:
            self.verbose_name = self.model._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = self.model._meta.verbose_name_plural

    def get_default_view_kwargs(self):
        return {
            'model': self.model,
            'modeladmin': self,
        }

    def get_index_kwargs(self):
        return self.get_default_view_kwargs()

    def get_create_kwargs(self):
        kwargs = self.get_default_view_kwargs()
        kwargs.update({
            'form_class': self.create_form_class if self.create_form_class else self.form_class,
        })
        return kwargs

    def get_update_kwargs(self):
        kwargs = self.get_default_view_kwargs()
        kwargs.update({
            'form_class': self.update_form_class if self.update_form_class else self.form_class,
        })
        return kwargs

    def get_detail_kwargs(self):
        return self.get_default_view_kwargs()

    def get_delete_kwargs(self):
        return self.get_default_view_kwargs()

    def get_urls(self):
        return patterns('',
            url(
                regex=r'^$',
                view=self.index_view.as_view(**self.get_index_kwargs()),
                name='index'
            ),
            url(
                regex=r'^create/$',
                view=self.create_view.as_view(**self.get_create_kwargs()),
                name='create'
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/$',
                view=self.detail_view.as_view(**self.get_detail_kwargs()),
                name='detail'
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/update/$',
                view=self.update_view.as_view(**self.get_update_kwargs()),
                name='update'
            ),
            url(
                regex=r'^(?P<pk>[0-9]+)/delete/$',
                view=self.delete_view.as_view(**self.get_delete_kwargs()),
                name='delete'
            ),
        )

    @property
    def urls(self):
        # We set the application and instance namespace here
        return self.get_urls(), None, None



def create_permissions(app, created_models, verbosity, **kwargs):
    """
    Creates 'view' permissions for all models.
    django.contrib.auth only creates add, change and delete permissions. Since we also support read-only views, we need
    to add our own extra permission.
    Copied from django.contrib.auth.management.create_permissions
    """
    from django.contrib.contenttypes.models import ContentType

    def _get_permission_codename(action, opts):
        return u'%s_%s' % (action, opts.object_name.lower())

    app_models = get_models(app)

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in app_models:
        ctype = ContentType.objects.get_for_model(klass)
        ctypes.add(ctype)

        opts = klass._meta
        perm = (_get_permission_codename('view', opts), u'Can view %s' % opts.verbose_name_raw)
        searched_perms.append((ctype, perm))

    # Find all the Permissions that have a context_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(auth_app.Permission.objects.filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    objs = [
        auth_app.Permission(codename=codename, name=name, content_type=ctype)
        for ctype, (codename, name) in searched_perms
        if (ctype.pk, codename) not in all_perms
    ]
    auth_app.Permission.objects.bulk_create(objs)
    if verbosity >= 2:
        for obj in objs:
            print "Adding permission '%s'" % obj


signals.post_syncdb.connect(create_permissions,
    dispatch_uid = "django-admin2.djadmin2.models.create_permissions")
