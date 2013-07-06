=====================================
Internationalization and localization
=====================================

.. index:: internationalization

Refer to the `Django i18n documentation`_ to get started with
internationalization (i18n).


Enabling i18n in Django
=======================

Make sure you've activated translation for your project
(the fastest way is to check in your ``settings.py`` file if ``MIDDLEWARE_CLASSES`` includes
``django.middleware.locale.LocaleMiddleware``).

Then compile the messages so they can be used by Django.

.. code-block:: bash

  python manage.py compilemessages

It should get you started !


Translating django-admin2
=========================

The translation of the language files is handled using Transifex_.

Improving existing translations
-------------------------------

To check out what languages are currently being worked on, check out the
`Project page`_. If you want to help with one of the translations, open the
team page by clicking on the language and request to join the team.

.. image:: _static/join_team.png
    :alt: Button labeled "Join team"

Now you can start translating. Open the language page, select a language
resource (e.g. *djadmin2.po*).

.. image:: _static/translate_now.png
    :alt: Button labeled "Translate now"

Then select a string from the list on the left and enter a translation on the
right side. Finally, click the *Save* button on the top right and you're done.

It is also possible to suggest better translations for existing ones with the
*Suggest* button on the bottom.

Requesting a new language
-------------------------

If a language is not available on Transifex_ yet, you can request it with the
*Request language* button on the `Project page`_.

.. image:: _static/request_language.png
    :alt: Button labeled "Request language"


Using i18n in the django-admin2 project development
===================================================

This section is mainly directed at 

Marking strings for translation
-------------------------------

**Python code**

Make sure to use ugettext or ugettext_lazy on strings that will be shown to the users,
with string interpolation ( "%(name_of_variable)s" instead of "%s" ) where needed.

Remember that all languages do not use the same word order, so try to provide flexible strings to translate !

**Templates**

Make sure to load the i18n tags and put ``trans`` tags and ``blocktrans`` blocks where needed.

Block variables are very useful to keep the strings simple.

Adding a new locale
-------------------

.. code-block:: bash

  cd djadmin2
  django-admin.py makemessages -l $LOCALE_CODE

A new file will be created under ``locale/$LOCALE_CODE/LC_MESSAGES/django.po``

Update the headers of the newly created file to match existing files and start the translation!

If you need help to adjust the *Plural-Forms* configuration in the .po file,
refer to the `gettext docs`_.


Updating existing locales
-------------------------

To update the language files with new strings in your .py files / templates:

.. code-block:: bash

  cd djadmin2 # or any other package, for instance example/blog
  django-admin.py makemessages -a

Then translate the files directly or upload them to Transifex_.

When the translation is done, you need to recompile the new translations:

.. code-block:: bash

  django-admin.py compilemessages


.. _`django i18n documentation`: https://docs.djangoproject.com/en/dev/topics/i18n/
.. _transifex: https://www.transifex.com/projects/p/django-admin2/
.. _project page: https://www.transifex.com/projects/p/django-admin2/
.. _gettext docs: http://www.gnu.org/savannah-checkouts/gnu/gettext/manual/html_node/Plural-forms.html
