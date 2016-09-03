=====
Views
=====

TODO list

* Describe customization of model views
* Show how to use ModelAdmin2 inheritance so an entire project works off a custom base view.

Customizing the Dashboard view
==============================

When you first log into django-admin2, just like ``django.contrib.admin`` you are presented with a display of apps and models. While this is useful for developers, it isn't friendly for end-users. Fortunately, django-admin2 makes it trivial to switch out the standard dashboard view.

However, because this is the dashboard view, the method of customization and configuration is different than other django-admin2 views.

In your Django project's root URLconf module (``urls.py``) modify the code to include the commented code before the ``djadmin2_site.autodiscover()``:

.. code-block:: python

    from django.conf.urls import include, url

    from djadmin2.site import djadmin2_site
    from djadmin2.views import IndexView


    ######### Begin django-admin2 customization code
    # Create a new django-admin2 index view
    class CustomIndexView(IndexView):

        # specify the template
        default_template_name = "custom_dashboard_template.html"

    # override the default index_view
    djadmin2_site.index_view = CustomIndexView
    ######### end django-admin2 customization code

    djadmin2_site.autodiscover()

    urlpatterns = [
        url(r'^admin2/', include(djadmin2_site.urls)),
        # ... Place the rest of the project URLs here
    ]

In real projects the new IndexView would likely be placed into a ``views.py`` module.

.. note:: Considering that dashboard is more intuitive of a name, perhaps the ``IndexView`` should be renamed ``DashboardView``?

Customizing the Login view
==========================

The login view could also be customized.

In your Django project's root URLconf module (``urls.py``) modify the code to include the commented code before the ``djadmin2.default.autodiscover()``:

.. code-block:: python

    from django.conf.urls import patterns, include, url

    from djadmin2.site import djadmin2_site
    from djadmin2.views import LoginView


    ######### Begin django-admin2 customization code
    # Create a new django-admin2 index view
    class CustomLoginView(LoginView):

        # specify the template
        default_template_name = "custom_login_template.html"

    # override the default index_view
    djadmin2_site.login_view = CustomLoginView
    ######### end django-admin2 customization code

    djadmin2_site.autodiscover()

    urlpatterns = patterns('',
        url(r'^admin2/', include(djadmin2_site.urls)),
        # ... Place the rest of the project URLs here
    )

In real projects the new LoginView would likely be placed into a ``views.py`` module.
