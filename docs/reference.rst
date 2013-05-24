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

TODO ...
