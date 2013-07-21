Frequently Asked Questions
===========================

Is this intended to go into Django contrib?
----------------------------------------------

No.

Reasons why it won't be going into Django core:

1. We want to rely on external dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We think certain packages can do a lot of the heavy lifting for us, and rewriting them is more time taken away from fixing bugs and implementing features. Since the Django core team isn't likely to accept external dependencies, especially ones that rely on Django itself, this alone is reason enough for django-admin2 to never make it into Django contrib.

2. We want increased Speed of Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django is a huge project with a lot of people relying on it. The conservative pace at which any change or enhancement is accepted is usually boon to the community of developers who work with it. Also, the committee-based management system means everyone gets a voice. This means things often happen at a slow and steady pace.

However, there are times when it's good to be outside of core, especially for experimental replacements for core functionality. Working outside of Django core means we can do what we want, when we want it.

What's wrong with the Django Admin?
-----------------------------------

The existing Django Admin is a powerful tool with pretty extensive extension capabilities. That said, it does have several significant issues.

Doesn't handle a million-record foreign key relation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say you have a million users and a model with a foreign key relation to them. You go the model detail field in the admin and you know what happens? The Django admin tries to serve out a million option links to your browser. Django doesn't handle this well, and neither does your browser. You can fix this yourself, find a third-party package to do it for you, or use django-admin2.

Yes, before release 1.0  of django-admin2 it will handle this problem for you.

Uses an early version of Class-Based Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

Very Challenging to Theme
~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO