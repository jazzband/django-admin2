def model_options(model):
    """
    Wrapper for accessing model._meta. If this access point changes in core
    Django, this function allows django-admin2 to address the change with
    what should hopefully be less disruption to the rest of the code base.

    Works on model classes and objects.
    """
    return model._meta


def admin2_urlname(view, action):
    """
    Converts the view and the specified action into a valid namespaced URLConf name.
    """
    return 'admin2:%s_%s_%s' % (view.app_label, view.model_name, action)


def model_verbose_name(obj):
    """
    Returns the verbose name of a model instance or class.
    """
    return model_options(obj).verbose_name


def model_verbose_name_plural(obj):
    """
    Returns the pluralized verbose name of a model instance or class.
    """
    return model_options(obj).verbose_name_plural
