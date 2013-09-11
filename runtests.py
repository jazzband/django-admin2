#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'
exampleproject_dir = os.path.join(os.path.dirname(__file__), 'example')
sys.path.insert(0, exampleproject_dir)

from django.test.utils import get_runner
from django.conf import settings


def runtests(tests=('blog', 'files', 'djadmin2')):
    '''
    Takes a list as first argument, enumerating the apps and specific testcases
    that should be executed. The syntax is the same as for what you would pass
    to the ``django-admin.py test`` command.

    Examples::

        # run the default test suite
        runtests()

        # only run the tests from application ``blog``
        runtests(['blog'])

        # only run testcase class ``Admin2Test`` from app ``djadmin2``
        runtests(['djadmin2.Admin2Test'])

        # run all tests from application ``blog`` and the test named
        # ``test_register`` on the ``djadmin2.Admin2Test`` testcase.
        runtests(['djadmin2.Admin2Test.test_register', 'blog'])
    '''
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(tests)
    sys.exit(bool(failures))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        tests = sys.argv[1:]
        runtests(tests)
    else:
        runtests()
