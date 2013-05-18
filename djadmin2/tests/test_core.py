import unittest

from django.db import models
from django.core.exceptions import ImproperlyConfigured

from ..models import ModelAdmin2
from ..core import Admin2

class Thing(models.Model):
    pass

class Admin2Test(unittest.TestCase):
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
        self.assertEquals(2, len(self.admin2.get_urls()))
