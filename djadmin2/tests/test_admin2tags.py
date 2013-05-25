from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from django.test import TestCase

from ..templatetags import admin2_tags
from ..views import IndexView


class TagsTestsModel(models.Model):

    class Meta:
        verbose_name = "Tags Test Model"
        verbose_name_plural = "Tags Test Models"


class TagsTestForm(forms.Form):
    visible_1 = forms.CharField()
    visible_2 = forms.CharField()
    invisible_1 = forms.HiddenInput()


TagsTestFormSet = formset_factory(TagsTestForm)


class TagsTests(TestCase):

    def setUp(self):
        self.instance = TagsTestsModel()

    def test_admin2_urlname(self):
        self.assertEquals(
            "admin2:None_None_index",
            admin2_tags.admin2_urlname(IndexView, "index")
        )

    def test_model_verbose_name_as_model_class(self):
        self.assertEquals(
            TagsTestsModel._meta.verbose_name,
            admin2_tags.model_verbose_name(TagsTestsModel)
        )

    def test_model_verbose_name_as_model_instance(self):
        self.assertEquals(
            self.instance._meta.verbose_name,
            admin2_tags.model_verbose_name(self.instance)
        )

    def test_model_verbose_name_plural_as_model_class(self):
        self.assertEquals(
            TagsTestsModel._meta.verbose_name_plural,
            admin2_tags.model_verbose_name_plural(TagsTestsModel)
        )

    def test_model_verbose_name_plural_as_model_instance(self):
        self.assertEquals(
            self.instance._meta.verbose_name_plural,
            admin2_tags.model_verbose_name_plural(self.instance)
        )

    def test_formset_visible_fieldlist(self):
        formset = TagsTestFormSet()
        self.assertEquals(
            admin2_tags.formset_visible_fieldlist(formset),
            [u'Visible 1', u'Visible 2']
        ) 
