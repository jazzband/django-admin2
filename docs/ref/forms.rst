=====
Forms
=====

Replicating `django.contrib.admin`'s user management
======================================================

If you have users, it's assumed you will have a Django app to manage them, called something like `accounts`, `users`, or `profiles`. For this exercise, we'll assume the app is called `accounts`. 

Step 1 - The admin2.py module
-----------------------------

In the `accounts` app, create an ``admin2.py`` module.

Step 2 - Web Integration
------------------------

Enter the following code in ``accounts/admin2.py``:

.. code-block:: python

    # Import the User and Group model from django.contrib.auth
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    from djadmin2.site import djadmin2_site
    from djadmin2.forms import UserCreationForm, UserChangeForm
    from djadmin2.types import ModelAdmin2

    # fetch the User model
    User = get_user_model()

    # Incorporate the 
    class UserAdmin2(ModelAdmin2):
        create_form_class = UserCreationForm
        update_form_class = UserChangeForm

    djadmin2_site.register(User, UserAdmin2)
    djadmin2_site.register(Group)

Done! The User and Group controls will appear in your django-admin2 dashboard.

Well... almost. We still need to incorporate the API components.

Step 3 - API Integration
------------------------

Change ``accounts/admin2.py`` to the following:

.. code-block:: python

    # Import the User and Group model from django.contrib.auth
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    from rest_framework.relations import PrimaryKeyRelatedField

    import djadmin2

    # fetch the User model
    User = get_user_model()


    # Serialize the groups
    class GroupSerializer(Admin2APISerializer):
        permissions = PrimaryKeyRelatedField(many=True)

        class Meta:
            model = Group

    # The GroupAdmin2 object is synonymous with GroupAdmin
    class GroupAdmin2(djadmin2.ModelAdmin2):
        api_serializer_class = GroupSerializer


    # Serialize the users, excluding password data
    class UserSerializer(djadmin2.apiviews.Admin2APISerializer):
        user_permissions = PrimaryKeyRelatedField(many=True)

        class Meta:
            model = User
            exclude = ('passwords',)


    # The UserAdmin2 object is synonymous with UserAdmin
    class UserAdmin2(djadmin2.ModelAdmin2):
        create_form_class = UserCreationForm
        update_form_class = UserChangeForm

        api_serializer_class = UserSerializer

    djadmin2.default.register(User, UserAdmin2)
    djadmin2.default.register(Group, GroupAdmin2)

Things to Do
=================


* Consider breaking the user management reference into more steps
* Create default UserAdmin2 and GroupAdmin2 classes
* Demonstrate how to easy it is to customize and HTML5-ize forms
* Demonstrate how easy it is to customize widgets