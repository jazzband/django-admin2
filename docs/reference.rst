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

Permissions
===========

Permissions are handled on a per view basis. So basically each admin view can
hold its own permission handling. That way you are very flexible in defining
who is allowed to access your edit view without limitting yourself to simple
model based permissions (like ``user.has_perm('blog.change_post')``.

You can attach a permission backend to a view by assigning a list of those to
the ``permission_classes`` attribute:

.. code-block:: python

    from django.views import generic
    from djadmin2.viewmixins import Admin2Mixin
    from djadmin2 import permissions

    
    class MyView(Admin2Mixin, generic.TemplateView):
        permission_classes = (
            permissions.IsStaffPermission,
            permissions.ModelViewPermission)

See the following sections on which permission classes ship with
django-admin2, ready to use and how you can roll your own.

Builtin permission backends
---------------------------

.. autoclass:: djadmin2.permissions.IsStaffPermission

.. autoclass:: djadmin2.permissions.ModelViewPermission

.. autoclass:: djadmin2.permissions.ModelAddPermission

.. autoclass:: djadmin2.permissions.ModelChangePermission

.. autoclass:: djadmin2.permissions.ModelDeletePermission

Writing your own permission backend
-----------------------------------

Internally a permission class uses so called *permission checks* to implement
the real logic of verifying that a user has the correct permissions. A
permission check has the real simple interface of accepting two position
arguments and an optional third one.  The first is the current ``request``,
the second the ``view`` on which the permission check is performed against.
The third and optional one is an arbitrary that can be passed into the
permission checking machinery to implement object level permissions. Based on
these arguments should the permission check than return either ``True`` if the
permission shall be granted. A returned ``False`` means that the permission
check failed and access to the user shall be denied.

Here is an example implementation of a custom permission check:

.. code-block:: python

    def secret_information_check(request, view, obj=None):
        '''
        Only allow superusers access to secret information.
        '''
        if 'secret' in obj.title.lower() and not request.user.is_superuser:
            return False
        return True

You can use the following predefined permission checks or built your own:

.. autofunction:: djadmin2.permissions.is_authenticated

.. autofunction:: djadmin2.permissions.is_staff

.. autofunction:: djadmin2.permissions.is_superuser

.. autofunction:: djadmin2.permissions.model_permission

You can now build your own permission class by subclassing
``djadmin2.permissions.BasePermission`` and assigning a list of those
permission checks to the ``permissions`` attribute:

.. code-block:: python

    class SecretContentPermission(permissions.BasePermission):
        permissions = (
            permissions.is_staff,
            secret_information_check)

Permissions in templates
------------------------

There is a ``{{ permissions }}`` variable available in the admin templates to
provide easy checking if the user has valid permission for a specific view.

You can check for either view, add, change and delete permissions. To do so you
use the provided ``permissions`` variable as seen below:

.. code-block:: html+django

    {% if permissions.has_change_permission %}
        <a href="... link to change form ...">Edit {{ object }}</a>
    {% endif %}

This will check for the particular model that the current view is working with,
if the user has the permission to access the change view. You can also use some
    object level permissions if you want to. For this just use the
``for_object`` filter implemented in the ``admin2_tags`` templatetag library:

.. code-block:: html+django

    {% load admin2_tags %} 

    {% if permissions.has_change_permission|for_object:object %}
        <a href="... link to change form ...">Edit {{ object }}</a>
    {% endif %}

.. note::
   Please be aware, that the :class:`django.contrib.auth.backends.ModelBackend`
   backend that ships with django and is used by default doesn't support object
   level permission. So unless you have implemented your own permission backend
   that supports it, the
   ``{{ permissions.has_change_permission|for_object:object }}`` will always
   return ``False`` and though will be useless.
   

The following permission checks are currently supported:

``has_view_permission``
    Checks if the user has the permission to access the ``detail_view`` view
    from the current ``ModelAdmin2`` object.
    
``has_add_permission``
    Checks if the user has the permission to access the ``create_view`` view
    from the current ``ModelAdmin2`` object.

``has_change_permission``
    Checks if the user has the permission to access the ``update_view`` view
    from the current ``ModelAdmin2`` object.

``has_delete_permission``
    Checks if the user has the permission to access the ``delete_view`` view
    from the current ``ModelAdmin2`` object.

Checking for permissions on other models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you just need to check the permissions for that particular model. In
that case, you can access its permissions like this:

.. code-block:: html+django

    {% if permissions.blog_post.has_view_permission %}
        <a href="...">View {{ post }}</a>
    {% endif %}

So what we actually did here is that we just put the name of the
``ModelAdmin2`` that is used for the model you want to access between the
``permissions`` variable and the ``has_view_permission`` permission check. This
name will be the app label followed by the model name in lowercase with an
underscore in between for ordinary django models.
