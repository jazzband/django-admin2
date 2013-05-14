===============
django-admin2
===============

One of the most useful parts of ``django.contrib.admin`` is the ability to configure various views that touch and alter data. django-admin2 is a complete rewrite of that library using modern Class-Based Views and enjoying a design focused on extendibility. By starting over, we can avoid the legacy code and make it easier to write extensions and themes.

Basic Pattern
==============

Our goal is to make this API work:

.. code-block::

    # myapp/admin2.py

    # Import the MongoAdmin base class
    from admin2.sites import Admin

    # Import your custom models
    from blog.models import Post

    # Instantiate the Admin class
    # Then attach the admin object to your model
    Post.mongoadmin = Admin()
    
.. note:: You will notice a difference between how and django.contrib.admin and django-mongonaut do configuration. The former associates the configuration class with the model object via a registration utility, and the latter does so by adding the configuration class as an attribute of the model object.