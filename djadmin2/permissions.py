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


class TemplatePermission(object):
    do_not_call_in_templates = True

    def __init__(self, permission_check):
        self._permission_check = permission_check

    def __nonzero__(self):
        return self._permission_check()

    def __call__(self, obj=None):
        return self._permission_check(obj)

    def __unicode__(self):
        return unicode(bool(self))


class TemplatePermissionChecker(object):
    '''
    Can be used in the template like::

        {{ permissions.has_view_permission }}
        {{ permissions.has_add_permission }}
        {{ permissions.has_change_permission }}
        {{ permissions.has_delete_permission|for_object:object }}

    The attribute access of ``has_create_permission`` will be done via a
    dictionary lookup (implemented in ``__getitem__``). This will return a
    callable that can be passed in an object to check object-level
    permissions.
    '''
    has_named_permission_regex = re.compile('^has_(?P<name>\w+)_permission$')

    view_name_mapping = {
        'view': 'detail_view',
        'add': 'create_view',
        'change': 'update_view',
        'delete': 'delete_view',
    }

    def __init__(self, request, view):
        self.request = request
        self.view = view

    def get_permission_check(self, view_name):
        def permission_check(obj=None):
            return self.view.has_permission(obj, view_name=view_name)
        return permission_check

    def __getitem__(self, key):
        match = self.has_named_permission_regex.match(key)
        if not match:
            raise KeyError
        view_name = match.groupdict()['name']
        if view_name not in self.view_name_mapping:
            raise KeyError
        view_name = self.view_name_mapping[view_name]
        return TemplatePermission(self.get_permission_check(view_name))
