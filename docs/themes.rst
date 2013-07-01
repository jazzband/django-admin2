======
Themes
======

How To Create a Theme
---------------------

A Django Admin 2 theme is merely a packaged Django app. Here are the necessary steps to create a theme called '*dandy*':

1. Make sure you have Django 1.5 or higher installed. 

2. Create the package:

.. code-block:: bash

    $ mkdir djadmin2-theme-fancy

4. Create a :file:`setup.py` module

.. code-block:: bash

    $ cd djadmin2-theme-fancy
    $ touch setup.py
    
Then enter the following information:

.. code-block:: python
    :emphasize-lines: 25
    

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

.. code-block:: bash

    $ django-admin2 startapp djadmin2_dandy
    $ cd djadmin2_dandy
    
.. note:: Why the djadmin2 prefix?

    This is so we don't pollute our eligible app infrastructure with django-admin2 themes and utilities.
    
6. Add a :file:`static/` file directory.

.. code-block:: bash

    $ mkdir static

    

This is where the dandy theme's custom CSS, JavaScript, and Image files are placed.

7. Add a :file:`templates/djadmin2_dandy` directory.

.. code-block:: bash

    $ mkdir templates
    $ mkdir templates/djadmin2_dandy

Inside of :file:`templates/djadmin2_dandy` is where the templates for dandy are defined.

Now you can start working on templates and static files!

Installing the custom theme
------------------------------

In the settings module:

.. code-block:: python

    ADMIN2_THEME_DIRECTORY = "djadmin2_dandy"
    INSTALLED_APPS += (
        ...
        'djadmin2',
        'djadmin2_dandy'
    )

4. You will also need 

Look at the "bootstrap" theme as an example. If you run into any problems, please file an issue.

Available Themes
----------------

Currently, only the "bootstrap" theme exists. The goal of this theme is to replicate the original Django admin UI functionality as closely as possible. This helps us ensure that we are not forgetting any functionality that Django users might be dependent on.

If you'd like to experiment with UI design that differs from the original Django admin UI, please create a new theme. It would be great to have at least 1 experimental theme!

Future
------

Keep in mind that this project is an experiment just to get our ideas down. We are looking at other similar projects to see if we can merge or borrow things.