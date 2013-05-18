Welcome to django-admin2's documentation!
=========================================

**django-admin2** aims to replace django's builtin admin that lives in
``django.contrib.admin``. Come and help us, have a look at the
:doc:`contributing` page and see our `GitHub`_ page.

Basic API
==============

Our goal is to make this API work:

.. code-block:: python

    # myapp/admin2.py

    # Import the Admin2 base class
    from djadmin2.models import Admin2

    # Import your custom models
    from blog.models import Post

    # Instantiate the Admin2 class
    # Then attach the admin2 object to your model
    Post.admin2 = Admin2()


.. _GitHub: https://github.com/pydanny/django-admin2

Content
-------

.. toctree::
   :maxdepth: 2

   contributing
   design
   meta

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

