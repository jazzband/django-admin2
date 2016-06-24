=============
django-admin2
=============

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband
.. image:: https://travis-ci.org/jazzband/django-admin2.png
   :alt: Build Status
   :target: https://travis-ci.org/jazzband/django-admin2
.. image:: https://coveralls.io/repos/github/jazzband/django-admin2/badge.svg?branch=develop
   :alt: Coverage Status
   :target: https://coveralls.io/github/jazzband/django-admin2?branch=develop
.. image:: https://badges.gitter.im/Join Chat.svg
   :target: https://gitter.im/pydanny/django-admin2?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

One of the most useful parts of ``django.contrib.admin`` is the ability to
configure various views that touch and alter data. django-admin2 is a complete
rewrite of that library using modern Class-Based Views and enjoying a design
focused on extendibility and adaptability. By starting over, we can avoid the
legacy code and make it easier to write extensions and themes.

Full Documentation at: https://django-admin2.readthedocs.io/

Features
========

* Rewrite of the Django Admin backend
* Drop-in themes
* Built-in RESTful API

Screenshots
===========

.. image:: https://github.com/jazzband/django-admin2/raw/develop/screenshots/Site_administration.png
    :width: 722px
    :alt: Site administration
    :align: center
    :target: https://github.com/jazzband/django-admin2/raw/develop/screenshots/Site_administration.png

.. image:: https://github.com/jazzband/django-admin2/raw/develop/screenshots/Select_user.png
    :width: 722px
    :alt: Select user
    :align: center
    :target: https://github.com/jazzband/django-admin2/raw/develop/screenshots/Select_user.png

Requirements
============

* Django 1.7+
* Python 2.7+ or Python 3.3+
* django-braces_
* django-extra-views_
* django-rest-framework_
* django-filter_
* Sphinx_ (for documentation)

.. _django-braces: https://github.com/brack3t/django-braces
.. _django-extra-views: https://github.com/AndrewIngram/django-extra-views
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
        ...
    )

Add setting for apps and the default theme in your settings file:

.. code-block:: python

    # In settings.py
    INSTALLED_APPS += ('djadmin2.themes.djadmin2theme_bootstrap3',)
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


How to write django-admin2 modules
==================================

.. code-block:: python

  # myapp/admin2.py
  # Import your custom models
  from django.contrib.auth.forms import UserCreationForm, UserChangeForm
  from django.contrib.auth.models import User
  from djadmin2.site import djadmin2_site
  from djadmin2.types import ModelAdmin2

  from .models import Post, Comment


  class UserAdmin2(ModelAdmin2):
      # Replicates the traditional admin for django.contrib.auth.models.User
      create_form_class = UserCreationForm
      update_form_class = UserChangeForm


  #  Register each model with the admin
  djadmin2_site.register(Post)
  djadmin2_site.register(Comment)
  djadmin2_site.register(User, UserAdmin2)

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

Drop-In Themes
==============

The default theme is whatever bootstrap is most current. Specifically:

.. code-block:: python

    # In settings.py
    INSTALLED_APPS += ('djadmin2.themes.djadmin2theme_bootstrap3',)
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_bootstrap3"

If you create a new theme, you define it thus:

.. code-block:: python

    # In settings.py
    # Mythical theme! This does not exit... YET!
    INSTALLED_APPS += ('djadmin2theme_foundation',)
    ADMIN2_THEME_DIRECTORY = "djadmin2theme_foundation"


Code of Conduct
======================

Everyone interacting in the django-admin2 project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `Jazzband Code of Conduct`_.

.. _`Jazzband Code of Conduct`: https://jazzband.co/about/conduct

Follows Best Practices
======================

.. image:: http://twoscoops.smugmug.com/Two-Scoops-Press-Media-Kit/i-C8s5jkn/0/O/favicon-152.png
   :name: Two Scoops Logo
   :align: center
   :alt: Two Scoops of Django
   :target: http://twoscoopspress.org/products/two-scoops-of-django-1-8

This project follows best practices as espoused in `Two Scoops of Django: Best Practices for Django 1.8`_.

.. _`Two Scoops of Django: Best Practices for Django 1.8`: http://twoscoopspress.org/products/two-scoops-of-django-1-8
