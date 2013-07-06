=====================================
Internationalization and localization
=====================================

.. index:: internationalization

Refer to the `Django i18n documentation`_ to get started.

.. _`Django i18n documentation`: https://docs.djangoproject.com/en/dev/topics/i18n/


Using internationalization in your project
==========================================

Make sure you've activated translation for your project
(the fastest way is to check in your ``settings.py`` file if ``MIDDLEWARE_CLASSES`` includes
``django.middleware.locale.LocaleMiddleware``).

Then compile the messages so they can be used by Django.

.. code-block:: bash

  python manage.py compilemessages


It should get you started !

Contributing to localization
============================

Django-admin2 has adopted `Transifex`_ to manage the localization process, `join and
help us`_ making django-admin2 available for everyone !

.. _Transifex: https://www.transifex.com
.. _`join and help us`: https://www.transifex.com/projects/p/django-admin2/


Using internationalization in the django-admin2 project development
===================================================================

Internationalization
--------------------

Python code
###########

Make sure to use ugettext or ugettext_lazy on strings that will be shown to the users,
with string interpolation ( "%(name_of_variable)s" instead of "%s" ) where needed.

Remember that all languages do not use the same word order, so try to provide flexible strings to translate !

Templates
#########

Make sure to load the i18n tags and put ``trans`` tags and ``blocktrans`` blocks where needed.

Block variables are very useful to keep the strings simple.

Adding a new locale
-------------------

.. code-block:: bash

  cd djadmin2
  django-admin.py makemessages -l $LOCALE_CODE

A new file will be created under ``locale/$LOCALE_CODE/LC_MESSAGES/django.po``

Update the headers of the newly created file to match existing files and start the translation !


Updating existing locales
-------------------------

.. code-block:: bash

  cd djadmin2 # or any other package, for instance example/blog
  django-admin.py makemessages -a

  # update the translations
  # make sure to fix all fuzzy translations

  django-admin.py compilemessages
