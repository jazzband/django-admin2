from django import template

register = template.Library()


@register.filter
def admin2_urlname(view, action):
    """
    Converts the view and the specified action into a valid namespaced URLConf name.
    """
    return 'admin2:%s_%s_%s' % (view.app_label, view.model_name, action)
