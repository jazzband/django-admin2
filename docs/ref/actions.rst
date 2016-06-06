=======
Actions
=======

.. index:: Actions

Actions are defined to work on a single view type. Currently, actions are only implemented against the ``ModelListView``. This view contains the default ``DeleteSelectedAction`` method, which in end functionality mirrors ``django.contrib.admin.delete_selected``.

However, under the hood, django-admin2's  actions work very differently. Instead of functions with assigned attributes, they can either be functions or full fledged objects. Which means you can more easily extend them to suit your needs.

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

.. index:: 
    single: Actions; Writing List Actions

The basic workflow of Django’s admin is, in a nutshell, “select an object, then change it.” This works well for a majority of use cases. However, if you need to make the same change to many objects at once, this workflow can be quite tedious.

In these cases, Django’s admin lets you write and register “actions” – simple functions that get called with a list of objects selected on the change list page.

If you look at any change list in the admin, you’ll see this feature in action; Django ships with a “delete selected objects” action available to all models.  Using our sample models, let's pretend we wrote a blog article about Django and our mother put in a whole bunch of embarressing comments. Rather than cherry-pick the comments, we want to delete the whole batch.

In our blog/admin.py module we write:

.. code-block:: python

    from djadmin2.actions import BaseListAction
    from djadmin2.site import djadmin2_site
    from djadmin2.types import ModelAdmin2

    from .models import Post, Comment

    class DeleteAllComments(BaseListAction):

        description = 'Delete selected items'
        default_template_name = 'actions/delete_all_comments_confirmation.html'
        success_message = 'Successfully deleted %d %s' # first argument - items count, second - verbose_name[_plural]

        def process_queryset(self):
            """Every action must provide this method"""
            self.get_queryset().delete()


    def custom_function_action(request, queryset):
        print(queryset.count())

    custom_function_action.description = 'Do other action'

    class PostAdmin(ModelAdmin2):
        actions = [DeleteAllComments, custom_function_action]

    djadmin2_site.register(Post, PostAdmin)
    djadmin2_site.register(Comment)


.. warning::

    The “delete selected objects” action uses `QuerySet.delete()`_ for efficiency reasons, which has an important caveat: your model’s delete() method will not be called.

    If you wish to override this behavior, simply write a custom action which accomplishes deletion in your preferred manner – for example, by calling ``Model.delete()`` for each of the selected items.

    For more background on bulk deletion, see the documentation on `object deletion`_.

.. _`QuerySet.delete()`: https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.delete
.. _`Object deletion`: https://docs.djangoproject.com/en/dev/topics/db/queries/#topics-db-queries-delete

Read on to find out how to add your own actions to this list.
