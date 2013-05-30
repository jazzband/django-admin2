from django.test import TestCase

from ..types import immutable_admin_factory


class ModelAdmin(object):
    model_admin_attributes = ['a', 'b', 'c']
    a = 1  # covered
    b = 2  # covered
    c = 3  # covered
    d = 4  # not covered


class ImmutableAdminFactoryTests(TestCase):

    def setUp(self):
        self.immutable_admin = immutable_admin_factory(ModelAdmin)

    def test_immutability(self):
        with self.assertRaises(AttributeError):
            # can't set attribute
            self.immutable_admin.a = 10
        with self.assertRaises(AttributeError):
            # 'ImmutableAdmin' object has no attribute 'e'
            self.immutable_admin.e = 5
        with self.assertRaises(AttributeError):
            # can't delete attribute
            del self.immutable_admin.a

    def test_attributes(self):
        self.assertEquals(self.immutable_admin.a, 1)
        self.assertEquals(self.immutable_admin.b, 2)
        self.assertEquals(self.immutable_admin.c, 3)
        with self.assertRaises(AttributeError):
            # 'ImmutableAdmin' object has no attribute 'd'
            self.immutable_admin.d
