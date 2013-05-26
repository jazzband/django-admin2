from django import template

register = template.Library()

from .. import utils


@register.filter
def admin2_urlname(view, action):
    """
    Converts the view and the specified action into a valid namespaced URLConf name.
    """
    return utils.admin2_urlname(view, action)


@register.filter
def model_app_label(obj):
    """
    Returns the app label of a model instance or class.
    """
    return utils.model_app_label(obj)


@register.filter
def model_verbose_name(obj):
    """
    Returns the verbose name of a model instance or class.
    """
    return utils.model_verbose_name(obj)


@register.filter
def model_verbose_name_plural(obj):
    """
    Returns the pluralized verbose name of a model instance or class.
    """
    return utils.model_verbose_name_plural(obj)


@register.filter
def formset_visible_fieldlist(formset):
    """
    Returns the labels of a formset's visible fields as an array.
    """
    return [f.label for f in formset.forms[0].visible_fields()]


@register.filter
def for_object(permissions, obj):
    """
    Only useful in the permission handling. This filter binds a new object to
    the permission handler to check for object-level permissions.
    """
    # some permission check has failed earlier, so we don't bother trying to
    # bind a new object to it.
    if permissions == '':
        return permissions
    return permissions.bind_object(obj)


@register.filter
def for_admin(permissions, admin):
    """
    Only useful in the permission handling. This filter binds a new admin to
    the permission handler to allow checking views of an arbitrary admin.
    """
    # some permission check has failed earlier, so we don't bother trying to
    # bind a new admin to it.
    if permissions == '':
        return permissions
    return permissions.bind_admin(admin)
