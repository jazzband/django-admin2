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


def is_authenticated(request, view, obj=None):
    return request.user.is_authenticated()


def is_staff(request, view, obj=None):
    return request.user.is_staff


def is_superuser(request, view, obj=None):
    return request.user.is_superuser


def model_permission(permission):
    def has_permission(request, view, obj=None):
        model_class = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)

        if model_class is None and queryset is not None:
            model_class = queryset.model

        assert model_class, (
            'Cannot apply DjangoModelPermissions on a view that does not '
            'have `.model` or `.queryset` property.')

        kwargs = {
            'app_label': model_class._meta.app_label,
            'model_name': model_class._meta.module_name
        }
        permission_name = permission % kwargs
        return request.user.has_perm(permission_name, obj)
    return has_permission


class AdminPermission(object):
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


class IsStaffPermission(AdminPermission):
    '''
    It ensures that the user is authenticated and is a staff member.
    '''
    permissions = (
        is_authenticated,
        is_staff)


class ModelPermission(AdminPermission):
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
        'POST': (model_permission('%(app_label)s.add_%(model_name)s'),),
        'PUT': (model_permission('%(app_label)s.change_%(model_name)s'),),
        'PATCH': (model_permission('%(app_label)s.change_%(model_name)s'),),
        'DELETE': (model_permission('%(app_label)s.delete_%(model_name)s'),),
    }


class ModelViewPermission(AdminPermission):
    permissions = (model_permission('%(app_label)s.view_%(model_name)s'),)


class ModelAddPermission(AdminPermission):
    permissions = (model_permission('%(app_label)s.add_%(model_name)s'),)


class ModelChangePermission(AdminPermission):
    permissions = (model_permission('%(app_label)s.change_%(model_name)s'),)


class ModelDeletePermission(AdminPermission):
    permissions = (model_permission('%(app_label)s.delete_%(model_name)s'),)
