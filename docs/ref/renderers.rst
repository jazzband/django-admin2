================
Custom Renderers
================

It is possible to create custom renderers for specific fields. Currently they
are only used in the object list view, for example to render boolean values
using icons. Another example would be to customize the rendering of dates.


Renderers
---------

A renderer is a function that accepts a value and the field and returns a HTML
representation of it. For example, the very simple builtin datetime renderer
works like this:

.. code-block:: python

    def title_renderer(value, field):
        """Render a string in title case (capitalize every word)."""
        return unicode(value).title()

In this case the ``field`` argument is not used. Sometimes it useful though:

.. code-block:: python

    def number_renderer(value, field):
        """Format a number."""
        if isinstance(field, models.DecimalField):
            return formats.number_format(value, field.decimal_places)
        return formats.number_format(value)

You can create your renderers anywhere in your code, but it is recommended to
put them in a file called ``renderers.py`` in your project.


Using Renderers
---------------

The renderers can be specified in the Admin2 class using the
``field_renderers`` attribute. The attribute contains a dictionary that maps a
field name to a renderer function.

By default, some renderers are automatically applied, for example the boolean
renderer when processing boolean values. If you want to suppress that renderer,
you can assign ``None`` to the field in the ``field_renderers`` dictionary.

.. code-block:: python

    class PostAdmin(djadmin2.ModelAdmin2):
        list_display = ('title', 'body', 'published')
        field_renderers = {
            'title': renderers.title_renderer,
            'published': None,
        }


Builtin Renderers
-----------------

.. automodule:: djadmin2.renderers
    :members:
