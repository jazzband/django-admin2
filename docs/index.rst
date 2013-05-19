Welcome to django-admin2's documentation!
=========================================

**django-admin2** aims to replace django's built-in admin that lives in
``django.contrib.admin``. Come and help us, have a look at the
:doc:`contributing` page and see our `GitHub`_ page.

This project is intentionally backwards-incompatible with ``django.contrib.admin``.

Features
==========

* Easy-to-extend API that follows similar patterns to ``django.contrib.admin``.
* Built-in RESTFUL API powered by ``django-rest-framework``
* Default theme built on Twitter Bootstrap
* Easy to implement theme system.

Requirements
=============

* Django 1.5+
* Python 2.7+ (Python 3.3+ support is pending)
* django-braces
* django-rest-framework
* Sphinx (for documentation)


Basic API
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


.. _GitHub: https://github.com/pydanny/django-admin2

Content
-------

.. toctree::
   :maxdepth: 2

   contributing
   api
   design
   meta


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
