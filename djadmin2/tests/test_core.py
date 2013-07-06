from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from ..types import ModelAdmin2
from ..core import Admin2
from ..actions import get_description


class Thing(models.Model):
    pass


class TestAction(object):
    description = "Test Action Class"


def test_function():
    pass


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

    def test_get_urls(self):
        self.admin2.register(Thing)
        self.assertEquals(8, len(self.admin2.get_urls()))

    def test_action_description(self):
        self.admin2.register(Thing)
        self.admin2.registry[Thing].list_actions.extend([
            TestAction,
            test_function
            ])
        self.assertEquals(
            get_description(
                self.admin2.registry[Thing].list_actions[0]
                ),
            'Delete selected items'
            )
        self.assertEquals(
            get_description(
                self.admin2.registry[Thing].list_actions[1]
                ),
            'Test Action Class'
            )
        self.assertEquals(
            get_description(
                self.admin2.registry[Thing].list_actions[2]
                ),
            'Test function'
            )
