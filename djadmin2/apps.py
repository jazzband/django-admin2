from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from djadmin2.permissions import create_view_permissions


class Djadmin2Config(AppConfig):
    name = 'djadmin2'
    verbose_name = _("Django Admin2")

    def ready(self):
        post_migrate.connect(create_view_permissions,
                             dispatch_uid="django-admin2.djadmin2.permissions.create_view_permissions")
