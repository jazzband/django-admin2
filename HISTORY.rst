History
=========

0.5.2 (2013-07-14)

 * setup.py fix

0.5.1 (2013-07-14)

 * No longer pinning dependencies on specific versions
 * `Documentation on built-in views`_ shows context variables.
 * Added django-filter to dependency list
 * Problem with related_name resolved
 * Fixed the height of the change_form
 * Example app actually shows added content
 * Pull requests going forward are internationalized_
 * FAQ_ begun
 
.. _`internationalized`: https://django-admin2.readthedocs.org/en/latest/contributing.html#internationalize
.. _`Documentation on built-in views`: https://django-admin2.readthedocs.org/en/latest/ref/built-in-views.html
.. _faq: https://django-admin2.readthedocs.org/en/latest/faq.html

0.5.0 (2013-07-08)

  * Implemented customizable value renderers
  * Implemented list filters using django-filters. Greatly supersedes what Django provides.
  * Implemented ModelAdmin2.save_on_top and ModelAdmin2.save_on_bottom
  * Implemented BooleanField icons for List and Detail views
  * Implemented default ``django.contrib.auth`` and ``django.contrib.sites`` registrations
  * Implemented the displayed of verbose field/method names in list view
  * Implemented client-side ordering of model list fields in default theme
  * Implemented improved internal naming conventions
  * Improved example project home page
  * Improved internal test coverage
  * Documentation for Context Variables in Themes
  * Corrected early nomenclature decisions
  * Much improved Internationalization
  * Added django-admin2 to Transifex
  * Translations for French, Polish, Slovak, Chinese, German, Catalan, Italian, and Spanish.

0.4.0 (2013-06-30)

  * Implemented both Function- and Class-based Action views
  * Implemented ModelAdmin2.list_display
  * Implemented ModelAdmin2.fieldsets
  * Dropdown widget now displays the selected choice
  * Added support for callables in ModelAdmin2.list_display
  * Added screenshots to README
  * Added second example project
  * Fixed breadcrumbs
  * Default theme: Proper closing of template and media blocks
  * Default theme: Standardized indentation in default theme templates
  * Default theme: Pointed to CDN for JQuery
  * Default theme: Added basic style for login form
  * Default theme: Internationalized all text strings


0.3.0 (2013-05-31)

  * HTML5 forms via floppyforms.
  * Many API improvements.
  * Added Breadcrumbs.
  * Added Login, Logout, ChangePassword views.
  * Added Actions.
  * Added support for inlines.
  * Added view based permission controls
  * Implement delete confirmations for child models.
  * Testrunner now can run on a specific test set or module.
  * Internal code refactoring to follow standards.
  * Moved to git-flow for accepting pull requests.
  * Model create/update pages now have save options.
  * Added i18n to all templates, much of internal code.
  * All print statements replaced with proper logging.
  * Design goals specified in the documentation.

0.2.0 (2013-05-19)

  * Birth! (Working Prototype)
  * Easy-to-extend API that follows similar patterns to django.contrib.admin.
  * Built-in RESTFUL API powered by django-rest-framework.
  * Default theme built on Twitter Bootstrap.
  * Easy to implement theme system.
  * Basic permission controls.
  * Testrunner
  * Documentation

0.1.1 (2013-05-17)

  * Code adoption from django-mongonaut.
  * Preperation for Django Circus sprints.

0.1 (2013-05-13)

  * Discussion with Russell Keith-Magee.
  * Inception.
