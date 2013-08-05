from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

import djadmin2
from ..types import ModelAdmin2
from ..core import Admin2


class Thing(models.Model):
    pass


APP_LABEL, APP_VERBOSE_NAME = 'app_one_label', 'App One Verbose Name'


class Admin2Test(TestCase):
    def setUp(self):
        self.admin2 = Admin2()

    def test_register(self):
        self.admin2.register(Thing)
        self.assertTrue(isinstance(self.admin2.registry[Thing], ModelAdmin2))

    def test_register_error(self):
        self.admin2.register(Thing)
        self.assertRaises(ImproperlyConfigured, self.admin2.register, Thing)

    def test_deregister(self):
        self.admin2.register(Thing)
        self.admin2.deregister(Thing)
        self.assertTrue(Thing not in self.admin2.registry)

    def test_deregister_error(self):
        self.assertRaises(ImproperlyConfigured, self.admin2.deregister, Thing)

    def test_register_app_verbose_name(self):
        self.admin2.register_app_verbose_name(APP_LABEL, APP_VERBOSE_NAME)
        self.assertEquals(
            self.admin2.app_verbose_names[APP_LABEL],
            APP_VERBOSE_NAME
        )

    def test_register_app_verbose_name_error(self):
        self.admin2.register_app_verbose_name(APP_LABEL, APP_VERBOSE_NAME)
        self.assertRaises(
            ImproperlyConfigured,
            self.admin2.register_app_verbose_name,
            APP_LABEL,
            APP_VERBOSE_NAME
        )

    def test_deregister_app_verbose_name(self):
        self.admin2.register_app_verbose_name(APP_LABEL, APP_VERBOSE_NAME)
        self.admin2.deregister_app_verbose_name(APP_LABEL)
        self.assertTrue(APP_LABEL not in self.admin2.app_verbose_names)

    def test_deregister_app_verbose_name_error(self):
        self.assertRaises(
            ImproperlyConfigured,
            self.admin2.deregister_app_verbose_name,
            APP_LABEL
        )

    def test_get_urls(self):
        self.admin2.register(Thing)
        self.assertEquals(8, len(self.admin2.get_urls()))

    def test_default_entries(self):
        expected_default_models = (User, Group, Site)
        for model in expected_default_models:
            self.assertTrue(isinstance(djadmin2.default.registry[model], ModelAdmin2))
