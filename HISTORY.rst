History
=========

0.7.0 (2016-11-16)

* Fix Django 1.8 issues and add 1.9, 1.10 compatibility
* Update django-rest-framework to 3.3.x
* Remove django-crispy-forms and django-floppyforms
* Regenerate example project to make it django 1.9 compatible
* Update tox and travis and add flake8
* Rename AdminModel2Mixin to Admin2ModelMixin
* Add migrations 
* remove south migrations
* Replace IPAddressField with GenericIPAddressField
* Fix password link in user admin
* Fix user logout on password change
* Fix tests
* Drop support of django versions lower then 1.8
* Drop older url.patterns



0.6.1 (2014-02-26)

 * Fix empty form display
 * Added more explicit installation instructions
 * Added migration instructions
 * Added view descriptions for "registry" and "app_verbose_names"
 * Show a nice message and margin if there are no visible fields
 * Updated widget controls for Django 1.6 changes.
 * Better error messages for admin views that fail to instantiate
 * Added png glyphicons to MANIFEST

0.6.0 (2013-09-12)

 * Implemented LogHistory to track recent history
 * New system for adding new views to ModelAdmin2 object
 * Fixed missing enctype="multipart/form-data" functionality
 * Implemented "app verbose name"
 * Apps can have customized names
 * List Actions can be set so they don't require selecting a model
 * Implemented ModelAdmin2.ordering
 * To maintain API consistency, renamed views.AdminView's "url" argument to "regex" 
 * Implemented ModelAdmin2.date_hierarchy
 * Changed theming system to make default theme follow the same rules as third-party themes.
 * Inlines now separated into stacked and tabular formats
 * Code coverage now displaying in README
 * User list page now showing all default columns and filters
 * Vast documentation improvements
 * Converted to ``django.utils.encoding.force_str`` instead ``unicode`` in order to type edge cases
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
 
.. _`internationalized`: https://django-admin2.readthedocs.io/en/latest/contributing.html#internationalize
.. _`Documentation on built-in views`: https://django-admin2.readthedocs.io/en/latest/ref/built-in-views.html
.. _faq: https://django-admin2.readthedocs.io/en/latest/faq.html

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
