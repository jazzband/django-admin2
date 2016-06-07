===========
ModelAdmin2
===========

The `ModelAdmin2` class is the representation of a model in the admin interface. These are stored in a file named `admin2.py` in your application. Let’s take a look at a very simple example of the ModelAdmin2:

.. code-block:: python

    from .models import Post
    from djadmin2.site import djadmin2_site
    from djadmin2.types import ModelAdmin2

    class PostAdmin(ModelAdmin2):
        pass

    djadmin2_site.register(Post, PostAdmin)

Adding a new view
=================

To add a new view to a ModelAdmin2, it's need add an attribute that is an
instance of the `views.AdminView`.

The `view.AdminView` takes tree parameters: `url`, `view` and `name`.
The `url` is expected a string for the url pattern for your view.
The `view` is expected a view and `name` is an optional parameter and
is expected a string that is the name of your view.

.. code-block:: python

    from .models import Post
    from djadmin2 import views
    from djadmin2.site import djadmin2_site
    from djadmin2.types import ModelAdmin2

    class PostAdmin(ModelAdmin2):
        preview_post = views.AdminView(r'^preview/$', views.PreviewPostView)

    djadmin2_site.register(Post, PostAdmin)

Replacing an existing view
==========================

To replacing an existing admin view, it's need add an attribute with the same name that
the view that you want replace:

.. code-block:: python

    from .models import Post
    from djadmin2 import views
    from djadmin2.site import djadmin2_site
    from djadmin2.types import ModelAdmin2

    class PostAdmin(ModelAdmin2):
        create_view = views.AdminView(r'^create/$', views.MyCustomCreateView)

    djadmin2_site.register(Post, PostAdmin)
