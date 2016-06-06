============
Installation
============

.. index:: installation

Adding django-admin2 to your project
====================================


Use pip to install from PyPI:

.. code-block:: python

   pip install django-admin2

Add djadmin2 and rest_framework to your settings file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'djadmin2',
        'djadmin2.themes.djadmin2theme_bootstrap3', # for the default theme
        'rest_framework', # for the browsable API templates
        ...
    )

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10
    }
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_bootstrap3"

Add djadmin2 urls to your URLconf:

.. code-block:: python

    # urls.py
    from django.conf.urls import include

    from djadmin2.site import djadmin2_site

    djadmin2_site.autodiscover()

    urlpatterns = [
      ...
      url(r'^admin2/', include(djadmin2_site.urls)),
    ]

Development Installation
=========================

See :doc:`contributing`.

Migrating from 0.6.x
====================

- The default theme has been updated to bootstrap3, be sure to replace your reference to the new one.
- Django rest framework also include multiple pagination system, the only one supported now is the PageNumberPagination.

Therefore, your `settings` need to include this:

.. code-block:: python

    # In settings.py
    INSTALLED_APPS += ('djadmin2.themes.djadmin2theme_bootstrap3',)
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_bootstrap3"

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10
    }


The default admin2 site has move into djadmin2.site make sure your use the news djadmin2_site in your urls.py:

.. code-block:: python

    # urls.py
    from django.conf.urls import include

    from djadmin2.site import djadmin2_site

    djadmin2_site.autodiscover()

    urlpatterns = [
      ...
      url(r'^admin2/', include(djadmin2_site.urls)),
    ]


Migrating from 0.5.x
====================

Themes are now defined explicitly, including the default theme. Therefore, your `settings` need to include this:

.. code-block:: python

    # In settings.py
    INSTALLED_APPS += ('djadmin2.themes.djadmin2theme_default',)
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_default"
