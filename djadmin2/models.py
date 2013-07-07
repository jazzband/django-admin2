# -*- coding: utf-8 -*-
""" Boilerplate for now, will serve a purpose soon! """
from __future__ import division, absolute_import, unicode_literals

from django.db.models import signals

from . import permissions


# setup signal handlers here, since ``models.py`` will be imported by django
# for sure if ``djadmin2`` is listed in the ``INSTALLED_APPS``.

signals.post_syncdb.connect(permissions.create_view_permissions,
    dispatch_uid="django-admin2.djadmin2.permissions.create_view_permissions")
