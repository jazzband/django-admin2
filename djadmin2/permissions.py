# -*- coding: utf-8 -*-
"""
djadmin2's permission handling. The permission classes have the same API as
the permission handling classes of the django-rest-framework. That way, we can
reuse them in the admin's REST API.

The permission checks take place in callables that follow the following
interface:

* They get passed in the current ``request``, an instance of the currently
  active ``view`` and optionally the object that should be used for
  object-level permission checking.
* Return ``True`` if the permission shall be granted, ``False`` otherwise.

The permission classes are then just fancy wrappers of these basic checks of
which it can hold multiple.
"""
from __future__ import division, absolute_import, unicode_literals

import logging
import re

from django.contrib.auth import get_permission_codename
from django.db.utils import DEFAULT_DB_ALIAS
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import router
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible, force_text

logger = logging.getLogger('djadmin2')


def is_authenticated(request, view, obj=None):
    '''
    Checks if the current user is authenticated.
    '''
    return request.user.is_authenticated()


def is_staff(request, view, obj=None):
    '''
    Checks if the current user is a staff member.
    '''
    return request.user.is_staff


def is_superuser(request, view, obj=None):
    '''
    Checks if the current user is a superuser.
    '''
    return request.user.is_superuser


def model_permission(permission):
    '''
    This is actually a permission check factory. It means that it will return
    a function that can then act as a permission check. The returned callable
    will check if the user has the with ``permission`` provided model
    permission. You can use ``{app_label}`` and ``{model_name}`` as
    placeholders in the permission name. They will be replaced with the
    ``app_label`` and the ``model_name`` (in lowercase) of the model that the
    current view is operating on.

    Example:

    .. code-block:: python

        check_add_perm = model_permission('{app_label}.add_{model_name}')

        class ModelAddPermission(permissions.BasePermission):
            permissions = [check_add_perm]
    '''
    def has_permission(request, view, obj=None):
        model_class = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)

        if model_class is None and queryset is not None:
            model_class = queryset.model

        assert model_class, (
            'Cannot apply model permissions on a view that does not '
            'have a `.model` or `.queryset` property.')

        try:
            # django 1.8+
            model_name = model_class._meta.model_name
        except AttributeError:
            model_name = model_class._meta.module_name

        permission_name = permission.format(
            app_label=model_class._meta.app_label,
            model_name=model_name)
        return request.user.has_perm(permission_name, obj)
    return has_permission


class BasePermission(object):
    '''
    Provides a base class with a common API. It implements a compatible
    interface to django-rest-framework permission backends.
    '''
    permissions = []
    permissions_for_method = {}

    def get_permission_checks(self, request, view):
        permission_checks = []
        permission_checks.extend(self.permissions)
        method_permissions = self.permissions_for_method.get(request.method, ())
        permission_checks.extend(method_permissions)
        return permission_checks

    # needs to be compatible to django-rest-framework
    def has_permission(self, request, view, obj=None):
        if request.user:
            for permission_check in self.get_permission_checks(request, view):
                if not permission_check(request, view, obj):
                    return False
            return True
        return False

    # needs to be compatible to django-rest-framework
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view, obj)


class IsStaffPermission(BasePermission):
    '''
    It ensures that the user is authenticated and is a staff member.
    '''
    permissions = (
        is_authenticated,
        is_staff)


class IsSuperuserPermission(BasePermission):
    '''
    It ensures that the user is authenticated and is a superuser. However it
    does not check if the user is a staff member.
    '''
    permissions = (
        is_authenticated,
        is_superuser)


# TODO: needs documentation
# TODO: needs integration into the REST API
class ModelPermission(BasePermission):
    '''
    Checks if the necessary model permissions are set for the accessed object.
    '''
    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission checks.
    permissions_for_method = {
        'GET': (),
        'OPTIONS': (),
        'HEAD': (),
        'POST': (model_permission('{app_label}.add_{model_name}'),),
        'PUT': (model_permission('{app_label}.change_{model_name}'),),
        'PATCH': (model_permission('{app_label}.change_{model_name}'),),
        'DELETE': (model_permission('{app_label}.delete_{model_name}'),),
    }


class ModelViewPermission(BasePermission):
    '''
    Checks if the user has the ``<app>.view_<model>`` permission.
    '''
    permissions = (model_permission('{app_label}.view_{model_name}'),)


class ModelAddPermission(BasePermission):
    '''
    Checks if the user has the ``<app>.add_<model>`` permission.
    '''
    permissions = (model_permission('{app_label}.add_{model_name}'),)


class ModelChangePermission(BasePermission):
    '''
    Checks if the user has the ``<app>.change_<model>`` permission.
    '''
    permissions = (model_permission('{app_label}.change_{model_name}'),)


class ModelDeletePermission(BasePermission):
    '''
    Checks if the user has the ``<app>.delete_<model>`` permission.
    '''
    permissions = (model_permission('{app_label}.delete_{model_name}'),)


@python_2_unicode_compatible
class TemplatePermissionChecker(object):
    '''
    Can be used in the template like:

    .. code-block:: html+django

        {{ permissions.has_view_permission }}
        {{ permissions.has_add_permission }}
        {{ permissions.has_change_permission }}
        {{ permissions.has_delete_permission }}
        {{ permissions.blog_post.has_view_permission }}
        {{ permissions.blog_comment.has_add_permission }}

    So in general:

    .. code-block:: html+django

        {{ permissions.has_<view_name>_permission }}
        {{ permissions.<object admin name>.has_<view name>_permission }}

    And using object-level permissions:

    .. code-block:: html+django

        {% load admin2_tags %}
        {{ permissions.has_delete_permission|for_object:object }}
        {% with permissions|for_object:object as object_permissions %}
            {{ object_permissions.has_delete_permission }}
        {% endwith %}

    And dynamically checking the permissions on a different admin:

    .. code-block:: html+django

        {% load admin2_tags %}
        {% for admin in list_of_model_admins %}
            {% with permissions|for_admin:admin as permissions %}
                {{ permissions.has_delete_permission }}
            {% endwith %}
        {% endfor %}

    If you don't know the permission you want to check at compile time (e.g.
    you cannot put ``has_add_permission`` in the template because the exact
    permission name might be passed into the context dynamically) you can bind
    the view name with the ``for_view`` filter:

    .. code-block:: html+django

        {% load admin2_tags %}
        {% with "add" as view_name %}
            {% if permissions|for_view:view_name %}
                <a href="...">{{ view_name|capfirst }} model</a>
            {% endif %}
        {% endwith %}

    The attribute access of ``has_<view name>_permission`` will check for the
    permissions of the view on the currently bound model admin not with the
    name ``<view name>``, but with the name that the ``view_name_mapping``
    returns for it. That step is needed since ``add`` is not the real
    attribute name in which the ``ModelAddFormView`` on the model admin lives.

    In the future we might get rid of that and this will also make it possible
    to check for any view assigned to the admin, like
    ``{{ permissions.auth_user.has_change_password_permission }}``. But this
    needs an interface beeing implemented like suggested in:
    https://github.com/twoscoops/django-admin2/issues/142
    '''
    _has_named_permission_regex = re.compile('^has_(?P<name>\w+)_permission$')

    view_name_mapping = {
        'view': 'detail_view',
        'add': 'create_view',
        'change': 'update_view',
        'delete': 'delete_view',
    }

    def __init__(self, request, model_admin, view=None, obj=None):
        self._request = request
        self._model_admin = model_admin
        self._view = view
        self._obj = obj

    def clone(self):
        return self.__class__(
            request=self._request,
            model_admin=self._model_admin,
            view=self._view,
            obj=self._obj)

    def bind_admin(self, admin):
        '''
        Return a clone of the permission wrapper with a new model_admin bind
        to it.
        '''
        if isinstance(admin, six.string_types):
            try:
                admin = self._model_admin.admin.get_admin_by_name(admin)
            except ValueError:
                return ''
        new_permissions = self.clone()
        new_permissions._view = None
        new_permissions._model_admin = admin
        return new_permissions

    def bind_view(self, view):
        '''
        Return a clone of the permission wrapper with a new view bind to it.
        '''
        if isinstance(view, six.string_types):
            if view not in self.view_name_mapping:
                return ''
            view_name = self.view_name_mapping[view]
            view = getattr(self._model_admin, view_name).view
        # we don't support binding view classes yet, only the name of views
        # are processed. We have the problem with view classes that we cannot
        # tell which model admin it was attached to.
        else:
            return ''
        # if view is a class and not instantiated yet, do it!
        if isinstance(view, type):
            view = view(
                request=self._request,
                **self._model_admin.get_default_view_kwargs())
        new_permissions = self.clone()
        new_permissions._view = view
        return new_permissions

    def bind_object(self, obj):
        '''
        Return a clone of the permission wrapper with a new object bind
        to it for object-level permissions.
        '''
        new_permissions = self.clone()
        new_permissions._obj = obj
        return new_permissions

    #########################################
    # interface exposed to the template users

    def __getitem__(self, key):
        match = self._has_named_permission_regex.match(key)
        if match:
            # the key was a has_*_permission, so bind the correspodning view
            view_name = match.groupdict()['name']
            return self.bind_view(view_name)
        # the name might be a named object admin. So get that one and bind it
        # to the permission checking
        try:
            admin_site = self._model_admin.admin
            model_admin = admin_site.get_admin_by_name(key)
        except ValueError:
            raise KeyError
        return self.bind_admin(model_admin)

    def __nonzero__(self):
        # if no view is bound we will return false, since we don't know which
        # permission to check we stay save in disallowing the access
        return self._cast_bool()

    def __bool__(self):
        return self._cast_bool()

    def _cast_bool(self):
        if self._view is None:
            return False
        if self._obj is None:
            return self._view.has_permission()
        else:
            return self._view.has_permission(self._obj)

    def __str__(self):
        if self._view is None:
            return ''
        return force_text(bool(self))


def create_view_permissions(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, **kwargs):  # noqa
    """
    Create 'view' permissions for all models.

    ``django.contrib.auth`` only creates add, change and delete permissions.
    Since we want to support read-only views, we need to add our own
    permission.

    Copied from ``https://github.com/django/django/blob/1.9.6/django/contrib/auth/management/__init__.py#L60``.

    """
    if not app_config.models_module:
        return

    try:
        Permission = apps.get_model('auth', 'Permission')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Permission):
        return

    from django.contrib.contenttypes.models import ContentType

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in app_config.get_models():
        # Force looking up the content types in the current database
        # before creating foreign keys to them.
        ctype = ContentType.objects.db_manager(using).get_for_model(klass)

        ctypes.add(ctype)
        perm = (get_permission_codename('view', klass._meta), 'Can view %s' % (klass._meta.verbose_name_raw))
        searched_perms.append((ctype, perm))

    # Find all the Permissions that have a content_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(Permission.objects.using(using).filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    perms = [
        Permission(codename=codename, name=name, content_type=ct)
        for ct, (codename, name) in searched_perms
        if (ct.pk, codename) not in all_perms
    ]
    # Validate the permissions before bulk_creation to avoid cryptic
    # database error when the verbose_name is longer than 50 characters
    permission_name_max_length = Permission._meta.get_field('name').max_length
    verbose_name_max_length = permission_name_max_length - 11  # len('Can change ') prefix
    for perm in perms:
        if len(perm.name) > permission_name_max_length:
            raise ValidationError(
                "The verbose_name of %s.%s is longer than %s characters" % (
                    perm.content_type.app_label,
                    perm.content_type.model,
                    verbose_name_max_length,
                )
            )
    Permission.objects.using(using).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)
