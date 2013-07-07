=========================================
Welcome to django-admin2's documentation!
=========================================

.. image:: https://travis-ci.org/pydanny/django-admin2.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/django-admin2

**Warning:** This project is currently in an **alpha** state and currently not meant for real projects.

One of the most useful parts of ``django.contrib.admin`` is the ability to configure various views that touch and alter data. django-admin2 is a complete rewrite of that library using modern Class-Based Views and enjoying a design focused on extendibility and adaptability. By starting over, we can avoid the legacy code and make it easier to write extensions and themes.

**django-admin2** aims to replace django's built-in admin that lives in
``django.contrib.admin``. Come and help us, read the :doc:`design` and
:doc:`contributing` pages, and visit the `GitHub`_ project.

This project is intentionally backwards-incompatible with ``django.contrib.admin``.

Features
=============

* Rewrite of the Django Admin backend
* Drop-in themes
* Built-in RESTful API


Basic API
==============

If you've worked with Django, this implementation should look familiar:

.. code-block:: python

  # myapp/admin2.py
  # Import your custom models
  from django.contrib.auth.forms import UserCreationForm, UserChangeForm
  from django.contrib.auth.models import User

  from .models import Post, Comment

  import djadmin2


  class UserAdmin2(djadmin2.ModelAdmin2):
      create_form_class = UserCreationForm
      update_form_class = UserChangeForm


  #  Register each model with the admin
  djadmin2.default.register(Post)
  djadmin2.default.register(Comment)
  djadmin2.default.register(User, UserAdmin2)


.. _GitHub: https://github.com/twoscoops/django-admin2

Content
-------

.. toctree::
   :maxdepth: 2

   installation
   contributing
   design
   internationalization
   tutorial

Reference
-----------


.. toctree::
   :maxdepth: 2

   ref/themes
   ref/api
   ref/actions
   ref/forms
   ref/permissions
   ref/views
   ref/built-in-views
   ref/renderers
   ref/meta

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
