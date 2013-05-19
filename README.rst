===============
django-admin2
===============

.. image:: https://travis-ci.org/pydanny/django-admin2.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/django-admin2

**Warning:** This project is currently in an **alpha** state and currently not meant for real projects.

One of the most useful parts of ``django.contrib.admin`` is the ability to configure various views that touch and alter data. django-admin2 is a complete rewrite of that library using modern Class-Based Views and enjoying a design focused on extendibility and adaptability. By starting over, we can avoid the legacy code and make it easier to write extensions and themes.

Features (current)
====================

* Easy-to-extend API that follows similar patterns to ``django.contrib.admin``.
* Built-in RESTFUL API powered by ``django-rest-framework``.
* Default theme built on Twitter Bootstrap that is just starting to act like the current Django admin.
* Easy to implement theme system.
* Basic permission controls.

Features (Planned)
====================

* Much improved documentation including tutorials and reference guides.

  * Extending existing views
  * Interacting with the basic Admin2 object.

* Improved permission controls

Requirements
=============

* Django 1.5+
* Python 2.7+ (Python 3.3+ support is pending)
* django-braces
* django-rest-framework
* django-floppyforms
* Sphinx (for documentation)

Contributing
=============

Yes please! Please read our formal contributing document at: https://github.com/pydanny/django-admin2/blob/master/docs/contributing.rst

Basic Pattern
==============

Our goal is to make this API work:

.. code-block:: python

  # Import your custom models
  from .models import Post, Comment
  from django.contrib.auth.forms import UserCreationForm, UserChangeForm
  from django.contrib.auth.models import User

  import djadmin2
  from djadmin2.models import ModelAdmin2


  class UserAdmin2(ModelAdmin2):
      create_form_class = UserCreationForm
      update_form_class = UserChangeForm


  #  Register each model with the admin
  djadmin2.default.register(Post)
  djadmin2.default.register(Comment)
  djadmin2.default.register(User, UserAdmin2)


Themes
========

The default theme is whatever bootstrap is most current. Specifically:

.. code-block:: python

    ADMIN2_THEME_DIRECTORY = "admin2/bootstrap/"

If you create a new theme, please define it thus:

.. code-block:: python

    ADMIN2_THEME_DIRECTORY = "admin2/foundation/"

REST API
==========

We plan to expose a REST API using Django Rest Framework. From this, you can define new themes powered by the client framework of your choice.

