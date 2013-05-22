===============
Reference
===============

This is where the developer API is in the process of being documented. 

.. note:: For developers of django-admin2 

    All functionality listed here must not only be listed, but also demonstrated with simple but functional code examples. 

Baseline Model
=================

The documentation works off a simple set of models, as listed below.

.. code-block:: python

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=255)
        body = models.TextField()

        def __unicode__(self):
            return self.title


    class Comment(models.Model):
        post = models.ForeignKey(Post)
        body = models.TextField()

        def __unicode__(self):
            return self.body


    