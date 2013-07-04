Welcome to django-admin2's documentation!
=========================================

**django-admin2** aims to replace django's built-in admin that lives in
``django.contrib.admin``. Come and help us, have a look at the
:doc:`contributing` page and see our `GitHub`_ page.

This project is intentionally backwards-incompatible with ``django.contrib.admin``.

Requirements
=============

* Django 1.5+
* Python 2.7+ or Python 3.3+
* django-braces
* django-extra-views
* django-floppyforms
* django-rest-framework
* Sphinx (for documentation)



Basic API
==============

Our goal is to make this API work:

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

   contributing
   design
   architecture
   api
   themes
   built-in-views
   meta
   tutorial

Reference
-----------

Most of django-admin2 is designed to be extensible, which means with a little bit of Python code you can do amazing things. You can easily create custom actions, implement alternative forms, set permissions per view, add new views, and even trivially replace the base views with those of your own design. Combined with the REST API, django-admin2 provides a wealth of customization options.

One of the core design goals of django-admin2 is to embrace object-oriented design, making it easy to take one of the built-in classes and extend it to suit your needs. 


.. toctree::
   :maxdepth: 2

   ref/actions
   ref/forms
   ref/permissions
   ref/views

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
