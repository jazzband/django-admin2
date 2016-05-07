# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from collections import defaultdict

from django.db.models import ProtectedError
from django.db.models import ManyToManyRel
from django.db.models.deletion import Collector
from django.db.models.fields.related import ForeignObjectRel
from django.utils import six
from django.utils.encoding import force_bytes, force_text


def lookup_needs_distinct(opts, lookup_path):
    """
    Returns True if 'distinct()' should be used to query the given lookup path.

    This is adopted from the Django core. django-admin2 mandates that code
    doesn't depend on imports from django.contrib.admin.

    https://github.com/django/django/blob/1.5.1/django/contrib/admin/util.py#L20
    """
    field_name = lookup_path.split('__', 1)[0]
    field = opts.get_field_by_name(field_name)[0]
    condition1 = hasattr(field, 'rel') and isinstance(field.rel, ManyToManyRel)
    condition2 = isinstance(field, ForeignObjectRel) and not field.field.unique
    return condition1 or condition2


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


def model_verbose_name(model):
    """
    Returns the verbose name of a model instance or class.
    """
    return model_options(model).verbose_name


def model_verbose_name_plural(model):
    """
    Returns the pluralized verbose name of a model instance or class.
    """
    return model_options(model).verbose_name_plural


def model_field_verbose_name(model, field_name):
    """
    Returns the verbose name of a model field.
    """
    meta = model_options(model)
    field = meta.get_field_by_name(field_name)[0]
    return field.verbose_name


def model_method_verbose_name(model, method_name):
    """
    Returns the verbose name / short description of a model field.
    """
    method = getattr(model, method_name)
    try:
        return method.short_description
    except AttributeError:
        return method_name


def model_app_label(obj):
    """
    Returns the app label of a model instance or class.
    """
    return model_options(obj).app_label


def get_attr(obj, attr):
    """
    Get the right value for the attribute. Handle special cases like callables
    and the __str__ attribute.
    """
    if attr == '__str__':
        from builtins import str as text
        value = text(obj)
    else:
        attribute = getattr(obj, attr)
        value = attribute() if callable(attribute) else attribute
    return value


class NestedObjects(Collector):
    """
    This is adopted from the Django core. django-admin2 mandates that code
    doesn't depend on imports from django.contrib.admin.

    https://github.com/django/django/blob/1.8c1/django/contrib/admin/utils.py#L160-L221
    """

    def __init__(self, *args, **kwargs):
        super(NestedObjects, self).__init__(*args, **kwargs)
        self.edges = {}  # {from_instance: [to_instances]}
        self.protected = set()
        self.model_count = defaultdict(int)

    def add_edge(self, source, target):
        self.edges.setdefault(source, []).append(target)

    def collect(self, objs, source=None, source_attr=None, **kwargs):
        for obj in objs:
            if source_attr and not source_attr.endswith('+'):
                related_name = source_attr % {
                    'class': source._meta.model_name,
                    'app_label': source._meta.app_label,
                }
                self.add_edge(getattr(obj, related_name), obj)
            else:
                self.add_edge(None, obj)
            self.model_count[obj._meta.verbose_name_plural] += 1
        try:
            return super(NestedObjects, self).collect(objs, source_attr=source_attr, **kwargs)
        except ProtectedError as e:
            self.protected.update(e.protected_objects)

    def related_objects(self, related, objs):
        qs = super(NestedObjects, self).related_objects(related, objs)
        return qs.select_related(related.field.name)

    def _nested(self, obj, seen, format_callback):
        if obj in seen:
            return []
        seen.add(obj)
        children = []
        for child in self.edges.get(obj, ()):
            children.extend(self._nested(child, seen, format_callback))
        if format_callback:
            ret = [format_callback(obj)]
        else:
            ret = [obj]
        if children:
            ret.append(children)
        return ret

    def nested(self, format_callback=None):
        """
        Return the graph as a nested list.

        """
        seen = set()
        roots = []
        for root in self.edges.get(None, ()):
            roots.extend(self._nested(root, seen, format_callback))
        return roots

    def can_fast_delete(self, *args, **kwargs):
        """
        We always want to load the objects into memory so that we can display
        them to the user in confirm page.
        """
        return False


def quote(s):
    """
    Ensure that primary key values do not confuse the admin URLs by escaping
    any '/', '_' and ':' and similarly problematic characters.
    Similar to urllib.quote, except that the quoting is slightly different so
    that it doesn't get automatically unquoted by the Web browser.

    This is adopted from the Django core. django-admin2 mandates that code
    doesn't depend on imports from django.contrib.admin.

    https://github.com/django/django/blob/1.5.1/django/contrib/admin/util.py#L48-L62
    """
    if not isinstance(s, six.string_types):
        return s
    res = list(s)
    for i in range(len(res)):
        c = res[i]
        if c in """:/_#?;@&=+$,"<>%\\""":
            res[i] = '_%02X' % ord(c)
    return ''.join(res)


def type_str(text):
    if six.PY2:
        return force_bytes(text)
    else:
        return force_text(text)
