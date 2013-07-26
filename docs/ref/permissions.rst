Permissions
===========

.. index:: Permissions

Permissions are handled on a per view basis. So basically each admin view can
hold its own permissions. That way you are very flexible in defining
who is allowed to access which view. For example, the edit view might need some
totally different permission checks then the delete view. However the add view
has nearly the same requirements as the edit view, you just also need to have
on extra permission. All those scenarios can be handled very easily in **django-admin2**.

Since the permission handling is centered around the specific views, this is
the place where you attach the permission checking logic to. You can assign one
or more permission backends to a view by setting the ``permission_classes``
attribute:

.. code-block:: python

    from django.views import generic
    from djadmin2.viewmixins import Admin2Mixin
    from djadmin2 import permissions

    
    class MyView(Admin2Mixin, generic.TemplateView):
        permission_classes = (
            permissions.IsStaffPermission,
            permissions.ModelViewPermission)

See the following sections on which permission classes ship with
**django-admin2**, ready to use and how you can roll your own.

Built-in permission classes
---------------------------

.. index::
    single: Permissions; Built-In Permission Classes

You can use the following permission classes directly in you views.

.. autoclass:: djadmin2.permissions.IsStaffPermission

.. autoclass:: djadmin2.permissions.IsSuperuserPermission

.. autoclass:: djadmin2.permissions.ModelViewPermission

.. autoclass:: djadmin2.permissions.ModelAddPermission

.. autoclass:: djadmin2.permissions.ModelChangePermission

.. autoclass:: djadmin2.permissions.ModelDeletePermission

Writing your own permission class
---------------------------------

.. index::
    single: Permissions; Custom Permission Classes

If you need it, writing your own permission class is really easy. You just need
to subclass the :class:`djadmin2.permissions.BasePermission` class and
overwrite the :meth:`~djadmin2.permissions.BasePermission.has_permission`
method that implements the desired permission checking. The arguments that the
method takes are pretty self explanatory:

``request``
    That is the request object that was sent to the server to access the
    current page. This will usually have the ``request.user`` attribute which
    you can use to check for user based permissions.

``view``
    The ``view`` argument is the instance of the class based view that the user wants
    to access.

``obj``
    This argument is optional and will only be given if an object-level
    permission check is performed. Take this into account if you want to
    support object-level permissions, or ignore it otherwise.

Based on these arguments should the ``has_permission`` method than return
either ``True`` if the permission shall be granted or ``False`` if the access
to the user shall be diened.

Here is an example implementation of a custom permission class:

.. code-block:: python

    from djadmin2.permissions import BasePermission

    class HasAccessToSecretInformationPermission(BasePermission):
        '''
        Only allow superusers access to secret information.
        '''

        def has_permission(self, request, view, obj=None):
            if obj is not None:
                if 'secret' in obj.title.lower() and not request.user.is_superuser:
                    return False
            return True

Permissions in Templates
------------------------

.. index::
    single: Permissions; Permissions in Templates

Since the permission handling is designed around views, the permission checks
in the template will also always access a view and return either ``True`` or
``False`` if the user has access to the given view. There is a ``{{ permissions
}}`` variable available in the admin templates to perform these tests against a
specific view.

At the moment you can check for view, add, change and delete permissions. To do
so you use the provided ``permissions`` variable as seen below:

.. code-block:: html+django

    {% if permissions.has_change_permission %}
        <a href="... link to change form ...">Edit {{ object }}</a>
    {% endif %}

This permission check will use the ``ModelAdmin2`` instance of the current view
that was used to render the above template to find the view it should perform
the permission check against. Since we test the change permission, it will use
the ``update_view`` to check if the user has the permission to access the
change page or not. If that's the case, we can safely display the link to
the change page.

At the moment we can check for the following four basic permissions:

``has_view_permission``
    This will check the permissions against the current admin's ``detail_view``.

``has_add_permission``
    This will check the permissions against the current admin's ``create_view``.

``has_change_permission``
    This will check the permissions against the current admin's ``update_view``.

``has_delete_permission``
    This will check the permissions against the current admin's ``delete_view``.

Object-Level Permissions
~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
    single: Permissions; Object-Level Permissions

The permission handling in templates also support checking for object-level
permissions. To do so, you can use the ``for_object`` filter implemented in the
``admin2_tags`` templatetag library:

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

Sometimes you have the need to perform all the permission checks in a block of
template code to use one object. In that case you can *bind* an object to the
permissions variable for easier handling:

.. code-block:: html+django

    {% load admin2_tags %}

    {% with permissions|for_object:object as object_permissions %}
        {% if object_permissions.has_change_permission %}
            <a href="... link to change form ...">Edit {{ object }}</a>
        {% endif %}
        {% if object_permissions.has_delete_permission %}
            <a href="... link to delete page ...">Delete {{ object }}</a>
        {% endif %}
    {% endwith %}

That also comes in handy if you have a rather generic template that performs
some permission checks and you want it to use object-level
permissions as well:

.. code-block:: html+django

    {% load admin2_tags %}

    {% with permissions|for_object:object as object_permissions %}
        {% include "list_of_model_actions.html" with permissions=object_permissions %}
    {% endwith %}

Checking for Permissions on Other Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
    single: Permissions; Checking for Permissions on Other Models

Sometimes you just need to check the permissions for that particular model. In
that case, you can access its permissions like this:

.. code-block:: html+django

    {% if permissions.blog_post.has_view_permission %}
        <a href="...">View {{ post }}</a>
    {% endif %}

So what we actually did here is that we just put the name of the
``ModelAdmin2`` that is used for the model you want to access between the
``permissions`` variable and the ``has_view_permission``. This name will be the
app label followed by the model name in lowercase with an underscore in between
for ordinary django models. That way you can break free of beeing limitted to
permission checks for the current ``ModelAdmin2``. But that doesn't help you
either if you don't know from the beginning on which model admin you want to
check the permissions. Imagine the admin's index page that should show a list
of all the available admin pages. To dynamically bind the permissions variable
to a model admin, you can use the ``for_admin`` filter:

.. code-block:: html+django

    {% load admin2_tags %}

    {% for admin in list_of_model_admins %}
        {% with permissions|for_admin:admin as permissions %}
            {% if permissions.has_add_permission %}Add another {{ admin.model_name }}{% endif %}
        {% endwith %}
    {% endfor %}

Dynamically Check for a Specific Permission Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
    single: Permissions; Dynamically Check for a Specific Permission Name

Just like you can bind a permission dynamically to a model admin, you can also
specify the actual permission name on the fly. There is the ``for_view`` filter
to do so.

.. code-block:: html+django

    {% load admin2_tags %}

    {% with "add" as view_name %}
        {% if permissions|for_view:view_name %}
            <a href="...">{{ view_name|capfirst }} model</a>
        {% endif %}
    {% endwith %}

That way you can avoid hardcoding the ``has_add_permission`` check and make the
checking depended on a given template variable. The argument for the
``for_view`` filter must be one of the four strings: ``view``, ``add``,
``change`` or ``delete``.
