from django import template

register = template.Library()


@register.filter
def admin2_urlname(value, arg):
    return 'admin2:%s_%s_%s' % (value.app_label, value.model_name, arg)
