'''
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
'''
import re
from django.utils import six


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

        permission_name = permission.format(
            app_label=model_class._meta.app_label,
            model_name=model_class._meta.module_name)
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

    The attribute access of ``has_create_permission`` will be done via a
    dictionary lookup (implemented in ``__getitem__``). This will return a
    callable (instance of ``TemplatePermission``, that can take an object to
    check object-level permissions.

    In the future any view assigned to the admin will be possible to check for
    permissions, like with
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
        new_permissions._model_admin = admin
        return new_permissions

    def bind_object(self, obj):
        '''
        Return a clone of the permission wrapper with a new object bind
        to it for object-level permissions.
        '''
        new_permissions = self.clone()
        new_permissions._obj = obj
        return new_permissions

    def get_view_by_name(self, view_name):
        view_name = self.view_name_mapping[view_name]
        model_admin = self._model_admin
        view_class = getattr(model_admin, view_name)
        view = view_class(
            request=self._request,
            **model_admin.get_default_view_kwargs())
        return view

    #########################################
    # interface exposed to the template users

    def __getitem__(self, key):
        match = self._has_named_permission_regex.match(key)
        if match:
            # the key was a has_*_permission, so get the *has permission
            # wrapper*
            view_name = match.groupdict()['name']
            if view_name not in self.view_name_mapping:
                raise KeyError
            view = self.get_view_by_name(view_name)
            return self.bind_view(view)
        # the name might be a named object admin. So get that one and try to
        # check the permission there for further traversal
        try:
            admin_site = self._model_admin.admin
            model_admin = admin_site.get_admin_by_name(key)
        except ValueError:
            raise KeyError
        return self.bind_admin(model_admin)

    def __nonzero__(self):
        # if no view is bound we will return false, since we don't know which
        # permission to check we stay save in disallowing the access
        if self._view is None:
            return False
        if self._obj is None:
            return self._view.has_permission()
        else:
            return self._view.has_permission(self._obj)

    def __unicode__(self):
        if self._view is None:
            return ''
        return unicode(bool(self))
