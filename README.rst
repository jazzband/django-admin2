===============
django-admin2
===============

.. image:: https://travis-ci.org/pydanny/django-admin2.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/django-admin2
.. image:: https://coveralls.io/repos/pydanny/django-admin2/badge.png?branch=develop
   :alt: Coverage Status
   :target: https://coveralls.io/r/pydanny/django-admin2
.. image:: https://pypip.in/v/django-admin2/badge.png
   :target: https://crate.io/packages/django-admin2/
.. image:: https://pypip.in/d/django-admin2/badge.png
   :target: https://crate.io/packages/django-admin2/

One of the most useful parts of ``django.contrib.admin`` is the ability to
configure various views that touch and alter data. django-admin2 is a complete
rewrite of that library using modern Class-Based Views and enjoying a design
focused on extendibility and adaptability. By starting over, we can avoid the
legacy code and make it easier to write extensions and themes.

Full Documentation at: http://django-admin2.rtfd.org/

Features
=============

* Rewrite of the Django Admin backend
* Drop-in themes
* Built-in RESTful API

Screenshots
===========

.. image:: https://github.com/pydanny/django-admin2/raw/develop/screenshots/Site_administration.png
    :width: 722px
    :alt: Site administration
    :align: center
    :target: https://github.com/pydanny/django-admin2/raw/develop/screenshots/Site_administration.png

.. image:: https://github.com/pydanny/django-admin2/raw/develop/screenshots/Select_user.png
    :width: 722px
    :alt: Select user
    :align: center
    :target: https://github.com/pydanny/django-admin2/raw/develop/screenshots/Select_user.png

Requirements
=============

* Django 1.5+
* Python 2.7+ or Python 3.3+
* django-braces_
* django-extra-views_
* django-floppyforms_
* django-rest-framework_
* django-filter_
* Sphinx_ (for documentation)

.. _django-braces: https://github.com/brack3t/django-braces
.. _django-extra-views: https://github.com/AndrewIngram/django-extra-views
.. _django-floppyforms: https://github.com/brutasse/django-floppyforms
.. _django-rest-framework: https://github.com/tomchristie/django-rest-framework
.. _django-filter: https://github.com/alex/django-filter
.. _Sphinx: http://sphinx-doc.org/



Installation
============

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


How to write django-admin2 modules
=====================================

.. code-block:: python

  # myapp/admin2.py
  # Import your custom models
  from django.contrib.auth.forms import UserCreationForm, UserChangeForm
  from django.contrib.auth.models import User

  from .models import Post, Comment

  import djadmin2


  class UserAdmin2(djadmin2.ModelAdmin2):
      # Replicates the traditional admin for django.contrib.auth.models.User
      create_form_class = UserCreationForm
      update_form_class = UserChangeForm


  #  Register each model with the admin
  djadmin2.default.register(Post)
  djadmin2.default.register(Comment)
  djadmin2.default.register(User, UserAdmin2)


Drop-In Themes
===============

The default theme is whatever bootstrap is most current. Specifically:

.. code-block:: python

    # In settings.py
    INSTALLED_APPS += ('djadmin2.themes.djadmin2theme_default',)
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_default/"

If you create a new theme, you define it thus:

.. code-block:: python

    # In settings.py
    # Mythical theme! This does not exit... YET!
    INSTALLED_APPS += ('djadmin2theme_foundation',)
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_foundation/"


Support this project!
======================

You can hire the lead maintainer to perform dedicated work on this package. Please email pydanny@cartwheelweb.com.

