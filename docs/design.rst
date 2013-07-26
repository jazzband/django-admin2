======
Design
======

.. index:: Design
    single: Design; Constraints

Constraints
------------

This section outlines the design constraints that django-admin2 follows:

1. There will be nothing imported from ``django.contrib.admin``.
2. The original bootstrap/ theme shall contain no UI enhancements beyond the original ``django.contrib.admin`` UI. (However, future themes can and should be experimental.)
3. External package dependencies are allowed but should be very limited.
4. Building a django-admin2 theme cannot involve learning Python, which explains why we are not using tools like django-crispy-forms. (One of our goals is to make it easier for designers to explore theming django-admin2).

.. index::
    single: Design; Backend Goals

Backend Goals
---------------

Rather than creating yet another project that skins ``django.contrib.admin``, our goal is to rewrite ``django.contrib.admin`` from the ground up using Class-Based Views, better state management, and attention to all the lessons learned from difficult admin customizations over the years. 

While the internal API for the backend may be drastically different, the end goal is to achieve relative parity with existing functionality in an extendable way:

* Relative functional parity with ``django.contrib.admin``. This is our desire to replicate much of the existing functionality, but not have to worry too much about coding ourselves into an overly-architected corner.
* Ability handle well under high load situations with many concurrent users. This is diametrically opposite from `django.contrib.admin` which doesn't work well in this regard.
* Extensible presentation and data views in such a way that it does not violate Constraint #4. To cover many cases, we will provide instructions on how to use the REST API to fetch data rather than create overly complex backend code.
* Create an architecture that follows the "*Principle of least surprise*". Things should behave as you expect them to, and you should be blocked from making dangerous mistakes. This is the reason for the ImmutableAdmin type.

Clean code with substantial documentation is also a goal:

1. Create a clearly understandable/testable code base.
2. All classes/methods/functions documented.
3. Provide a wealth of in-line code documentation.

.. index::
    single: Design; REST API Goals

REST API Goals
----------------

There are a lot of various cases that are hard to handle with pure HTML projects, but are trivial to resolve if a REST API is available. For example, using unmodified ``django.contrib.admin`` on projects with millions of database records combined with foreign key lookups. In order to handle these cases, rather than explore each edge case, ``django-admin2`` provides a RESTFUL API as of version 0.2.0.

Goals:

1. Provide a extendable self-documenting API (django-rest-framework).
2. Reuse components from the HTML view.
3. Backwards compatibility: Use a easily understood API versioning system so we can expand functionality of the API without breaking existing themes.

.. index::
    single: Design; UI Goals

UI Goals
---------

1. Replicate the old admin UI as closely as possible in the bootstrap/ theme. This helps us ensure that admin2/ functionality has parity with admin/.

2. Once (1) is complete and we have a stable underlying API, experiment with more interesting UI variations.
