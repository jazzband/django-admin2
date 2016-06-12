============
Contributing
============

.. index:: Contributing

.. warning:: Before you begin working on your contribution, please read and become familiar with the design_ of ``django-admin2``. The design_ document should hopefully make it clear what our constraints and goals are for the project.

.. _design: https://django-admin2.readthedocs.io/en/latest/design.html

.. index::
    single: Contributing; Setup

Setup
=====

Fork on GitHub
--------------

Before you do anything else, login/signup on GitHub and fork **django-admin2** from the `GitHub project`_.

Clone your fork locally
-----------------------

If you have git-scm installed, you now clone your git repo using the following command-line argument where <my-github-name> is your account name on GitHub::

    git clone git@github.com:<my-github-name>/django-admin2.git

Local Installation
-------------------------

1. Create a virtualenv_ (or use virtualenvwrapper_). Activate it.
2. cd into django-admin2
3. type ``$ pip install -r requirements.txt``
4. type ``$ python setup.py develop``

Try the example projects
--------------------------

1. cd into example/
2. create the database: ``$ python manage.py migrate``
3. run the dev server: ``$ python manage.py runserver``

.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/

.. index::
    single: Contributing; Issues

Issues!
=======

The list of outstanding **django-admin2** feature requests and bugs can be found on our on our GitHub `issue tracker`_. Pick an unassigned issue that you think you can accomplish, add a comment that you are attempting to do it, and shortly your own personal label matching your GitHub ID will be assigned to that issue.

Feel free to propose issues that aren't described!

Tips
----

#. **starter** labeled issues are deemed to be good low-hanging fruit for newcomers to the project, Django, or even Python.
#. **doc** labeled issues must only touch content in the docs folder.
#. Since this project will live on inheritance, all views are Class-Based.
#. Familiarize yourself with the project design_ document.

.. index:: 
    single: Contributing; Topic Branches
    single: Contributing; Pull Requests

Setting up topic branches and generating pull requests
======================================================

.. note:: This is our way of describing our version of git-flow.

While it's handy to provide useful code snippets in an issue, it is better for
you as a developer to submit pull requests. By submitting pull request your
contribution to django-admin2 will be recorded by Github.

In git it is best to isolate each topic or feature into a "topic branch".  While
individual commits allow you control over how small individual changes are made
to the code, branches are a great way to group a set of commits all related to
one feature together, or to isolate different efforts when you might be working
on multiple topics at the same time.

While it takes some experience to get the right feel about how to break up
commits, a topic branch should be limited in scope to a single ``issue`` as
submitted to an issue tracker.

Also since GitHub pegs and syncs a pull request to a specific branch, it is the
**ONLY** way that you can submit more than one fix at a time.  If you submit
a pull from your master branch, you can't make any more commits to your master
without those getting added to the pull.

To create a topic branch, its easiest to use the convenient ``-b`` argument to ``git checkout``::

    git checkout -b fix-broken-thing
    Switched to a new branch 'fix-broken-thing'

You should use a verbose enough name for your branch so it is clear what it is
about.  Now you can commit your changes and regularly merge in the upstream
develop as described below.

When you are ready to generate a pull request, either for preliminary review,
or for consideration of merging into the project you must first push your local
topic branch back up to GitHub::

    git push origin fix-broken-thing

Now when you go to your fork on GitHub, you will see this branch listed under
the "Source" tab where it says "Switch Branches".  Go ahead and select your
topic branch from this list, and then click the "Pull request" button.

Your pull request should be applied to the **develop** branch of django-admin2.
Be sure to change from the default of ``master`` to ``develop``.

Next, you can add a comment about your branch.  If this in response to
a submitted issue, it is good to put a link to that issue in this initial
comment.  The repo managers will be notified of your pull request and it will
be reviewed (see below for best practices).  Note that you can continue to add
commits to your topic branch (and push them up to GitHub) either if you see
something that needs changing, or in response to a reviewer's comments.  If
a reviewer asks for changes, you do not need to close the pull and reissue it
after making changes. Just make the changes locally, push them to GitHub, then
add a comment to the discussion section of the pull request.

.. index::
    single: Contributing; Pulling Upstream Changes

Pull upstream changes into your fork regularly
==================================================

**django-admin2** is advancing quickly. It is therefore critical that you pull upstream changes from master into your fork on a regular basis. Nothing is worse than putting in a day of hard work into a pull request only to have it rejected because it has diverged too far from master.

To pull in upstream changes::

    git remote add upstream https://github.com/twoscoops/django-admin2.git
    git pull upstream develop

For more info, see http://help.github.com/fork-a-repo/

.. index::
    single: Contributing; Pulling with Rebase

Advanced git users: Pull with rebase
------------------------------------

This will pull and then reapply your work on top of the upcoming changes::

    git pull --rebase upstream develop

It saves you from an extra merge, keeping the history cleaner, but it's potentially dangerous because you're rewriting history. For more info, see http://gitready.com/advanced/2009/02/11/pull-with-rebase.html

.. index::
    single: Contributing; Getting your Pull Requests Accepted

.. index:: Getting your Pull Request Accepting

How to get your pull request accepted
=====================================

We want your submission. But we also want to provide a stable experience for our users and the community. Follow these rules and you should succeed without a problem!

.. index:: 
    single: Getting your Pull Request Accepting; Run the tests!

Run the tests!
--------------

Before you submit a pull request, please run the entire django-admin2 test suite via::

    python runtests.py

The first thing the core committers will do is run this command. Any pull request that fails this test suite will be **immediately rejected**.

.. index:: 
    single: Getting your Pull Request Accepting; Don't reduce test coverage!


If you add code/views you need to add tests!
--------------------------------------------

We've learned the hard way that code without tests is undependable. If your pull request reduces our test coverage because it lacks tests then it will be **rejected**.

For now, we use the Django Test framework (based on unittest).

Also, keep your tests as simple as possible. Complex tests end up requiring their own tests. We would rather see duplicated assertions across test methods then cunning utility methods that magically determine which assertions are needed at a particular stage. Remember: `Explicit is better than implicit`.

You don't need to run the whole test suite during development in order to make
the test cycles a bit faster. Just pass in the specific tests you want to run
to ``runtests.py`` as you would do with the ``django-admin.py test`` command.
Examples::

    # only run the tests from application ``blog``
    python runtests.py blog

    # only run testcase class ``Admin2Test`` from app ``djadmin2``
    python runtests.py djadmin2.Admin2Test

    # run all tests from application ``blog`` and the test named
    # ``test_register`` on the ``djadmin2.Admin2Test`` testcase.
    python runtests.py djadmin2.Admin2Test.test_register blog
    
.. index:: 
    single: Getting your Pull Request Accepting; Don't mix code changes with whitespace cleanup

Don't mix code changes with whitespace cleanup
----------------------------------------------

If you change two lines of code and correct 200 lines of whitespace issues in a file the diff on that pull request is functionally unreadable and will be **immediately rejected**. Whitespace cleanups need to be in their own pull request.

.. index:: 
    single: Getting your Pull Request Accepting; Keep your pull requests limited to single issues

Keep your pull requests limited to a single issue
--------------------------------------------------

django-admin2 pull requests should be as small/atomic as possible. Large, wide-sweeping changes in a pull request will be **rejected**, with comments to isolate the specific code in your pull request. Some examples:

#. If you are making spelling corrections in the docs, don't modify the settings.py file (pydanny_ is guilty of this mistake).
#. If you are fixing a view don't '*cleanup*' unrelated views. That cleanup belongs in another pull request.
#. Changing permissions on a file should be in its own pull request with explicit reasons why.

Best Practices
--------------

As much as possible, we follow the advice of the `Two Scoops of Django`_ book. Periodically the book will be referenced either for best practices or as a blunt object by the project lead in order to end bike-shedding.

.. _`Two Scoops of Django`: https://2scoops.org

Python
~~~~~~

Follow PEP-0008 and memorize the Zen of Python::

    >>> import this

Please keep your code as clean and straightforward as possible. When we see more than one or two functions/methods starting with `_my_special_function` or things like `__builtins__.object = str` we start to get worried. Rather than try and figure out your brilliant work we'll just **reject** it and send along a request for simplification.

Furthermore, the pixel shortage is over. We want to see:

* `options` instead of `opts`
* `model_name` instead of `model`
* `my_function_that_does_things` instead of `mftdt`

Templates
~~~~~~~~~

Follow bootstrap's coding standards for HTML_ and CSS_.  Use two spaces for indentation, and write so the templates are readable (not for the generated html).

.. _HTML: https://github.com/twitter/bootstrap/blob/master/CONTRIBUTING.md#coding-standards-html
.. _CSS: https://github.com/twitter/bootstrap/blob/master/CONTRIBUTING.md#coding-standards-css

Internationalize
~~~~~~~~~~~~~~~~

Any new text visible to the user must be internationalized_.

.. _internationalized: https://django-admin2.readthedocs.io/en/latest/internationalization.html


How pull requests are checked, tested, and done
===============================================

First we pull the code into a local branch::

    git checkout develop
    git checkout -b <submitter-github-name>-<submitter-branch> develop
    git pull git://github.com/<submitter-github-name>/django-admin2.git <submitter-branch> <branch-name>

Then we run the tests::

    coverage run runtests.py
    coverage report

We do the following:

1. Any test failures or the code coverage drops and the pull request is rejected.
2. We open up a browser and make sure it looks okay.
3. We check the commit's code changes and make sure that they follow our rules.

We finish with a merge and push to GitHub::

    git checkout develop
    git merge <branch-name>
    git push origin develop

.. _installation: install.html
.. _GitHub project: https://github.com/twoscoops/django-admin2
.. _issue tracker: https://github.com/twoscoops/django-admin2/issues
.. _pydanny: http://pydanny.com
