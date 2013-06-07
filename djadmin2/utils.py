from django.db.models import ProtectedError
from django.db.models import ManyToManyRel
from django.db.models.deletion import Collector
from django.db.models.related import RelatedObject


def lookup_needs_distinct(opts, lookup_path):
    """
    Returns True if 'distinct()' should be used to query the given lookup path.

    This is adopted from the Django core. django-admin2 mandates that code
    doesn't depend on imports from django.contrib.admin.

    https://github.com/django/django/blob/1.5.1/django/contrib/admin/util.py#L20
    """
    field_name = lookup_path.split('__', 1)[0]
    field = opts.get_field_by_name(field_name)[0]
    if ((hasattr(field, 'rel') and
         isinstance(field.rel, ManyToManyRel)) or
        (isinstance(field, RelatedObject) and
         not field.field.unique)):
         return True
    return False

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


def model_app_label(obj):
    """
    Returns the app label of a model instance or class.
    """
    return model_options(obj).app_label


class NestedObjects(Collector):
    """
    This is adopted from the Django core. django-admin2 mandates that code
    doesn't depend on imports from django.contrib.admin.

    https://github.com/django/django/blob/1.5.1/django/contrib/admin/util.py#L144
    """
    def __init__(self, *args, **kwargs):
        super(NestedObjects, self).__init__(*args, **kwargs)
        self.edges = {}  # {from_instance: [to_instances]}
        self.protected = set()

    def add_edge(self, source, target):
        self.edges.setdefault(source, []).append(target)

    def collect(self, objs, source_attr=None, **kwargs):
        for obj in objs:
            if source_attr:
                self.add_edge(getattr(obj, source_attr), obj)
            else:
                self.add_edge(None, obj)
        try:
            return super(NestedObjects, self).collect(
                objs, source_attr=source_attr, **kwargs)
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
