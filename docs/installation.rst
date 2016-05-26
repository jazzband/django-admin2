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
        'floppyforms', # For HTML5 form fields
        'crispy_forms', # Required for the default theme's layout
        ...
    )

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10
    }
    CRISPY_TEMPLATE_PACK = "bootstrap3"
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_bootstrap3"

Add djadmin2 urls to your URLconf:

.. code-block:: python

   # urls.py
   from django.conf.urls import include
   
   import djadmin2
   
   djadmin2.default.autodiscover()


   urlpatterns = [
      ...
      url(r'^admin2/', include(djadmin2.default.urls)),
   ]

Development Installation
=========================

See :doc:`contributing`.

Migrating from 0.5.x
====================

Themes are a new default theme based on bootstrap3 and also some new settings to add. Therefore, your `settings` need to include this:

.. code-block:: python

    # In settings.py
    INSTALLED_APPS += ('djadmin2.themes.djadmin2theme_bootstrap3',)
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10
    }
    CRISPY_TEMPLATE_PACK = "bootstrap3"
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_bootstrap3"
