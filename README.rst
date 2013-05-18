===============
django-admin2
===============

.. image:: https://travis-ci.org/pydanny/django-admin2.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/django-admin2

One of the most useful parts of ``django.contrib.admin`` is the ability to configure various views that touch and alter data. django-admin2 is a complete rewrite of that library using modern Class-Based Views and enjoying a design focused on extendibility. By starting over, we can avoid the legacy code and make it easier to write extensions and themes.

**Note:** This is pre-alpha and currently non-functional. We'll try and have a rough working prototype by the end of May 18th, 2013.

Contributing
=============

Yes please! Please read our formal contributing document at: https://github.com/pydanny/django-admin2/blob/master/docs/contributing.rst


Basic Pattern
==============

Our goal is to make this API work:

.. code-block:: python

    # myapp/admin2.py

    # Import the Admin2 base class
    from admin2.models import Admin2

    # Import your custom models
    from blog.models import Post

    # Instantiate the Admin2 class
    # Then attach the admin2 object to your model
    Post.admin2 = Admin2()

    
.. note:: You will notice a difference between how and django.contrib.admin and django-admin2 do configuration. The former associates the configuration class with the model object via a registration utility, and the latter does so by adding the configuration class as an attribute of the model object.

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

