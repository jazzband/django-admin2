======
Themes
======

How To Create a Theme
---------------------

A Django Admin 2 theme is merely a packaged Django app. Here are the necessary steps to create a theme called '*dandy*':


1. Make sure you have Django 1.5 or higher installed. 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    $ python -c 'import django; print(django.get_version())'

2. Create the package:
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ mkdir djadmin2-theme-dandy

4. Create a :file:`setup.py` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd djadmin2-theme-dandy
    $ touch setup.py
    
Then enter the following information (you will probably want to change the highlighted lines below to match your package name):

.. code-block:: python
    :emphasize-lines: 25, 27, 28, 40, 41, 42, 44
    

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from setuptools import setup
    import re
    import os
    import sys
    
    def get_packages(package):
        """
        Return root package and all sub-packages.
        """
        return [dirpath
                for dirpath, dirnames, filenames in os.walk(package)
                if os.path.exists(os.path.join(dirpath, '__init__.py'))]

    if sys.argv[-1] == 'publish':
        os.system("python setup.py sdist upload")
        print("You probably want to also tag the version now:")
        print("  git tag -a %s -m 'version %s'" % (version, version))
        print("  git push --tags")
        sys.exit()

    setup(
        name='djadmin2-theme-dandy',
        version=0.1.0,
        description="A dandy theme for django-admin2.",
        long_description="A dandy theme for django-admin2.",
        classifiers=[
            "Environment :: Web Environment",
            "Framework :: Django",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        keywords='django,djadmin2',
        author="Your Name Here",
        author_email='Your Email Here',
        url='http://github.com/your-repo-here',
        license='MIT',
        packages=get_packages('djadmin2_dandy'),
        include_package_data=True,
        install_requires=[
            'django-admin2>=0.4.0',
            ],
        zip_safe=False,
    )


5. Create a Django App called 'dandy' and go inside. 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ django-admin2 startapp djadmin2_dandy
    $ cd djadmin2_dandy
    
.. note:: Why the djadmin2 prefix?

    This is so we don't pollute our eligible app infrastructure with django-admin2 themes and utilities.
    
6. Add a :file:`static/` file directory set:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
    :emphasize-lines: 3,4,5

    $ mkdir -p static/djadmin2_dandy/{js,css,img}

These directories are where the dandy theme's custom CSS, JavaScript, and Image files are placed.

7. Add a :file:`templates/djadmin2_dandy` directory:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
    :emphasize-lines: 2

    $ mkdir -p templates/djadmin2_dandy

Inside of :file:`templates/djadmin2_dandy` is where the templates for dandy are defined.

Now you can start working on templates and static files!

Installing the custom theme
------------------------------

In the settings module, place the theme right after djadmin2 (change the highlighted line to your package's name):

.. code-block:: python
    :emphasize-lines: 5

    ########### DJANGO-ADMIN2 CONFIGURATION
    ADMIN2_THEME_DIRECTORY = "djadmin2_dandy"
    INSTALLED_APPS += (
        'djadmin2',
        'djadmin2_dandy'
    )
    ########### END DJANGO-ADMIN2 CONFIGURATION
    
.. todo:: Have someone besides pydanny test this!

Views and their Templates
-------------------------

See doc:`built-in-views`


Available Themes
----------------

Currently, only the default "bootstrap" theme exists. The goal of this theme is to replicate the original Django admin UI functionality as closely as possible. This helps us ensure that we are not forgetting any functionality that Django users might be dependent on.

If you'd like to experiment with UI design that differs from the original Django admin UI, please create a new theme. It would be great to have at least 1 experimental theme!

Future
------

Keep in mind that this project is an experiment just to get our ideas down. We are looking at other similar projects to see if we can merge or borrow things.
