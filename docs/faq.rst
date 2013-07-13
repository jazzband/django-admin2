Frequently Asked Questions
===========================

Is this intended to go into Django contrib?
----------------------------------------------

No.

Reasons why it won't be going into Django core:

1. We want to rely on external dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We think certain packages can do a lot of the heavy lifting for us, and rewriting them is more time taken away from fixing bugs and implementing features.

2. We want increased Speed of Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django is a huge project with a lot of people relying on it. The conservative pace at which any change or enhancement is accepted is usually boon to the community of developers who work with it. Also, the committee-based management system means everyone gets a voice. This means things often happen at a slow and steady pace.

However, there are times when it's good to be outside of core, especially for experimental replacements for core functionality. We want changes and we want them now! Working outside of Django core means we can do what we want, when we want it.