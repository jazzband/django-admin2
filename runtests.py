#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'
exampleproject_dir = os.path.join(os.path.dirname(__file__), 'example')
sys.path.insert(0, exampleproject_dir)

from django.test.utils import get_runner
from django.conf import settings


def runtests(tests=('blog', 'djadmin2',)):
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
