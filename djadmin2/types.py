from collections import namedtuple


def immutable_admin_factory(model_admin):
    """ Provide an ImmutableAdmin to make it harder for developers to dig themselves into holes.
        See https://github.com/twoscoops/django-admin2/issues/99
        Frozen class implementation as namedtuple suggested by Audrey Roy

        Note: This won't stop developers from saving mutable objects to the result, but hopefully
                developers attempting that 'workaround/hack' will read our documentation.
    """
    ImmutableAdmin = namedtuple("ImmutableAdmin", model_admin.model_admin_attributes, verbose=False)
    return ImmutableAdmin(*[getattr(model_admin, x) for x in model_admin.model_admin_attributes])

