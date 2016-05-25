from django.test import TestCase

from .. import views
from ..types import ModelAdmin2, immutable_admin_factory
from ..core import Admin2
from .models import BigThing


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


class ModelAdminTest(TestCase):

    def setUp(self):
        class MyModelAdmin(ModelAdmin2):
            my_view = views.AdminView(r'^$', views.ModelListView)

        self.model_admin = MyModelAdmin

    def test_views(self):
        views = [self.model_admin.my_view] + ModelAdmin2.views
        self.assertListEqual(self.model_admin.views, views)

    def test_views_not_same(self):
        self.assertIsNot(self.model_admin.views, ModelAdmin2.views)

    def test_get_index_kwargs(self):
        admin_instance = ModelAdmin2(BigThing, Admin2)
        self.assertIn(
            'paginate_by',
            admin_instance.get_index_kwargs().keys()
        )

    def test_get_urls(self):
        admin_instance = ModelAdmin2(BigThing, Admin2)
        self.assertEqual(6, len(admin_instance.get_urls()))

    def test_get_urls_throws_type_error(self):
        with self.assertRaises(TypeError):
            try:
                admin_instance = ModelAdmin2(BigThing, Admin2)
                admin_instance.views = [views.AdminView(None, None, None)]
                admin_instance.get_urls()

            except TypeError as e:
                message = u"Cannot instantiate admin view " \
                    '"ModelAdmin2.None". The error that got raised was: ' \
                    "'NoneType' object has no attribute 'as_view'"
                self.assertEqual(e.args[0], message)
                raise
