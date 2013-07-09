# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from fabric.api import local, lcd
from fabric.contrib.console import confirm


DIRS = ['djadmin2', 'example/blog', 'example2/polls']


def _run(command, directory):
    with lcd(directory):
        print('\n### Processing %s...' % directory)
        local(command)


def makemessages():
    command = 'django-admin.py makemessages -a'
    for d in DIRS:
        _run(command, d)


def compilemessages():
    command = 'django-admin.py compilemessages'
    for d in DIRS:
        _run(command, d)


def checkmessages():
    command = 'ls -1 locale/*/LC_MESSAGES/django.po | xargs -I {} msgfmt -c {}'
    for d in DIRS:
        _run(command, d)


def pulltx():
    print('\n### Pulling new translations from Transifex...')
    local('tx pull -a')


def pushtx():
    print('\n### Pushing translations and sources to Transifex...')
    print('Warning: This might destroy existing translations. Probably you should pull first.')
    if confirm('Continue anyways?', default=False):
        local('tx push -s -t')
    else:
        print('Aborting.')
