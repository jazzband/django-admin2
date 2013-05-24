from django.db import models
from django.test import TestCase

from .. import utils
from ..views import IndexView


class UtilsTestModel(models.Model):

    class Meta:
        verbose_name = "Utils Test Model"
        verbose_name_plural = "Utils Test Models"


class UtilsTest(TestCase):

    def setUp(self):
        self.instance = UtilsTestModel()

    def test_as_model_class(self):
        self.assertEquals(
            UtilsTestModel._meta,
            utils.model_options(UtilsTestModel)
        )

    def test_as_model_instance(self):
        self.assertEquals(
            self.instance._meta,
            utils.model_options(self.instance)
        )

    def test_admin2_urlname(self):
        self.assertEquals(
            "admin2:None_None_index",
            utils.admin2_urlname(IndexView, "index")
        )

    def test_model_verbose_name_as_model_class(self):
        self.assertEquals(
            UtilsTestModel._meta.verbose_name,
            utils.model_verbose_name(UtilsTestModel)
        )

    def test_model_verbose_name_as_model_instance(self):
        self.assertEquals(
            self.instance._meta.verbose_name,
            utils.model_verbose_name(self.instance)
        )

    def test_model_verbose_name_plural_as_model_class(self):
        self.assertEquals(
            UtilsTestModel._meta.verbose_name_plural,
            utils.model_verbose_name_plural(UtilsTestModel)
        )

    def test_model_verbose_name_plural_as_model_instance(self):
        self.assertEquals(
            self.instance._meta.verbose_name_plural,
            utils.model_verbose_name_plural(self.instance)
        )
