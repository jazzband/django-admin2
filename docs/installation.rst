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
      'rest_framework', # for the browsable API templates
      'floppyforms', # For HTML5 form fields
      'crispy_forms', # Required for the default theme's layout
      ...
   )

Add djadmin2 urls to your URLconf:

.. code-block:: python

   # urls.py
   from django.conf.urls import patterns, include
   
   import djadmin2
   
   djadmin2.default.autodiscover()


   urlpatterns = patterns(
      ...
      url(r'^admin2/', include(djadmin2.default.urls)),
   )

Development Installation
=========================

See :doc:`contributing`.
