Built-In Views
===============

Each of these views contains the list of context variables that are included in
their templates.

.. note:: TODO: Fix the capitalization of context variables!

View Constants
---------------

The following are available in every view:

    :next: The page to redirect the user to after login
    :MEDIA_URL: Specify a directory where file uploads for users who use your site go
    :STATIC_URL: Specify a directory for JavaScript, CSS and image files.
    :user: Currently logged in user

View Descriptions
------------------

.. autoclass:: djadmin2.views.IndexView
    :members:


.. autoclass:: djadmin2.views.AppIndexView
    :members:

.. autoclass:: djadmin2.views.ModelListView
    :members:


.. autoclass:: djadmin2.views.ModelDetailView
    :members:

.. autoclass:: djadmin2.views.ModelEditFormView
    :members:

.. autoclass:: djadmin2.views.ModelAddFormView
    :members:

.. autoclass:: djadmin2.views.ModelDeleteView
    :members:

.. autoclass:: djadmin2.views.PasswordChangeView
    :members:

.. autoclass:: djadmin2.views.PasswordChangeDoneView
    :members:


.. autoclass:: djadmin2.views.LoginView
    :members:

.. autoclass:: djadmin2.views.LogoutView
    :members:

