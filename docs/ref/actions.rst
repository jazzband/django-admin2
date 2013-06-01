=======
Actions
=======

.. warning:: Incomplete and innaccurate! In the process of revising. -- pydanny

Actions are defined to work on a single view type. Currently, actions are only implemented against the ``ModelListView``. This view contains the default ``DeleteSelectedAction`` method, which in end functionality mirrors ``django.contrib.admin.delete_selected``.

However, under the hood, django-admin2's  actions work very differently. Instead of functions with assigned attributes, they are full fledged objects. Which means you can more easily extend them to suit your needs.

The documentation works off a simple set of models, as listed below:

.. code-block:: python

    # blog/models.py
    from django.db import models

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )


    class Post(models.Model):
        title = models.CharField(max_length=255)
        body = models.TextField()
        status = models.CharField(max_length=1, choices=STATUS_CHOICES)

        def __unicode__(self):
            return self.title


    class Comment(models.Model):
        post = models.ForeignKey(Post)
        body = models.TextField()

        def __unicode__(self):
            return self.body

Writing List Actions
-----------------------

Using our sample models, let's pretend we wrote a blog article about Django and our mother put in a whole bunch of embarressing comments. Rather than cherry-pick the comments, we want to delete the whole batch. 

In our blog/admin.py module we write:

.. code-block:: python

    import djadmin2

    from .models import Post, Comment

    class DeleteAllComments(djadmin2.actions.BaseListAction):
        description = "Delete selected items"
        template = "blog/actions/delete_all_comments_confirmation.html

    class PostAdmin(djadmin2.ModelAdmin2):
        actions = [DeleteAllComments]

    djadmin2.default.register(Post, PostAdmin)
    djadmin2.default.register(Comment)

