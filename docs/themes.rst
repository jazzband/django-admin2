======
Themes
======

How To Create a Theme
---------------------

A theme consists of 3 parts. Here's how you set those up:

1. Static files: create a directory in djadmin2/static/themes/ called your-theme-name/. Put your static files in there.

2. Templates: create a directory in djadmin2/templates/admin2/bootstrap/ called your-theme-name/. Copy the template files from the bootstrap theme into there and then modify them as you'd like.

3. Your settings file should point to your theme directory::

    ADMIN2_THEME_DIRECTORY = "admin2/bootstrap/"

Look at the "bootstrap" theme as an example. If you run into any problems, please file an issue.

Available Themes
----------------

Currently, only the "bootstrap" theme exists. The goal of this theme is to replicate the original Django admin UI functionality as closely as possible. This helps us ensure that we are not forgetting any functionality that Django users might be dependent on.

If you'd like to experiment with UI design that differs from the original Django admin UI, please create a new theme. It would be great to have at least 1 experimental theme!

Future
------

Keep in mind that this project is an experiment just to get our ideas down. We are looking at other similar projects to see if we can merge or borrow things.