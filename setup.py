#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand
import re
import os
import sys
import string


def get_author(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__author__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


def remove_screenshots(text):
    """
    Removes the section with screenshots since PyPI doesn't like them.
    """
    outputting = True
    new_text = ""
    for line in text.splitlines():
        if line.startswith("Screenshots"):
            outputting = False
            continue
        if len(line) and line[0] in string.ascii_letters:
            outputting = True
        if outputting:
            new_text += line + '\n'
    return new_text


author = get_author('djadmin2')
version = get_version('djadmin2')


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

LONG_DESCRIPTION = remove_screenshots(open('README.rst').read())
HISTORY = open('HISTORY.rst').read()

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'example'))
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='django-admin2',
    version=version,
    description="An introspective interface for Django's ORM.",
    long_description=LONG_DESCRIPTION + '\n\n' + HISTORY,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='django,admin',
    author=author,
    author_email='pydanny@gmail.com',
    url='http://djangoadmin.org',
    license='MIT',
    packages=get_packages('djadmin2'),
    include_package_data=True,
    #test_suite='runtests.runtests',
    install_requires=[
        'django>=1.8.0',
        'django-extra-views<=0.7.1',
        'django-braces>=1.3.0',
        'djangorestframework<=3.3.3',
        'django-filter>=0.15.3',
        'pytz==2016.4',
        'future>=0.15.2',
        ],
    extras_require={
        'testing': ['pytest', 'pytest-django', 'pytest-ipdb'],
    },
    cmdclass = {'test': PyTest},
    zip_safe=False,
)

# (*) Please direct queries to Github issue list, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
