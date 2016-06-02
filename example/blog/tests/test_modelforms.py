from __future__ import unicode_literals

from django import forms
from django.forms import modelform_factory
from django.test import TestCase

from ..models import Post


class ModelFormFactoryTest(TestCase):

    def test_modelform_factory(self):
        form_class = modelform_factory(Post, exclude=[])
        self.assertTrue(form_class)
        field = form_class.base_fields['title']
        self.assertTrue(isinstance(field.widget, forms.TextInput))


class ModelFormTest(TestCase):

    def test_custom_base_form(self):
        class MyForm(forms.ModelForm):
            pass

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        form = form_class()
        self.assertTrue(isinstance(
            form.fields['title'].widget,
            forms.TextInput))

    def test_declared_fields(self):
        class MyForm(forms.ModelForm):
            subtitle = forms.CharField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        self.assertTrue(isinstance(
            form_class.base_fields['subtitle'].widget,
            forms.TextInput))
        self.assertTrue(isinstance(
            form_class.declared_fields['subtitle'].widget,
            forms.TextInput))

        self.assertTrue(isinstance(
            form_class.base_fields['title'].widget,
            forms.TextInput))
        # title is not defined in declared fields

    def test_additional_form_fields(self):
        class MyForm(forms.ModelForm):
            subtitle = forms.CharField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        form = form_class()
        self.assertTrue(isinstance(
            form.fields['subtitle'].widget,
            forms.TextInput))

    def test_subclassing_forms(self):
        class MyForm(forms.ModelForm):
            subtitle = forms.CharField()

            class Meta:
                model = Post
                exclude = []

        class ChildForm(MyForm):
            created = forms.DateField()

        form_class = modelform_factory(model=Post, form=ChildForm, exclude=[])
        form = form_class()
        self.assertTrue(isinstance(
            form.fields['title'].widget,
            forms.TextInput))
        self.assertTrue(isinstance(
            form.fields['subtitle'].widget,
            forms.TextInput))
        self.assertTrue(isinstance(
            form.fields['created'].widget,
            forms.DateInput))


class FieldWidgetTest(TestCase):

    def test_dont_overwrite_none_default_widget(self):
        # we don't create the floppyform EmailInput for the email field here
        # since we have overwritten the default widget. However we replace the
        # django textarea with a floppyforms Textarea
        email_input = forms.widgets.Textarea()

        class MyForm(forms.ModelForm):
            email = forms.EmailField(widget=email_input)

            class Meta:
                model = Post
                exclude = []

        widget = MyForm().fields['email'].widget
        self.assertFalse(isinstance(widget, forms.EmailInput))
        self.assertTrue(isinstance(widget, forms.Textarea))

    def test_float_field(self):
        class MyForm(forms.ModelForm):
            float = forms.FloatField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['float'].widget
        self.assertTrue(isinstance(widget, forms.NumberInput))
        self.assertEqual(widget.input_type, 'number')

    def test_decimal_field(self):
        class MyForm(forms.ModelForm):
            decimal = forms.DecimalField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['decimal'].widget
        self.assertTrue(isinstance(widget, forms.NumberInput))
        self.assertEqual(widget.input_type, 'number')

    def test_integer_field(self):
        class MyForm(forms.ModelForm):
            integer = forms.IntegerField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['integer'].widget
        self.assertTrue(isinstance(widget, forms.NumberInput))
        self.assertEqual(widget.input_type, 'number')

    def test_email_field(self):
        class MyForm(forms.ModelForm):
            email = forms.EmailField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['email'].widget
        self.assertTrue(isinstance(widget, forms.EmailInput))
        self.assertEqual(widget.input_type, 'email')

    def test_url_field(self):
        class MyForm(forms.ModelForm):
            url = forms.URLField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['url'].widget
        self.assertTrue(isinstance(widget, forms.URLInput))
        self.assertEqual(widget.input_type, 'url')

    def test_slug_field(self):
        class MyForm(forms.ModelForm):
            slug = forms.SlugField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['slug'].widget
        self.assertTrue(isinstance(widget, forms.TextInput))
        self.assertEqual(widget.input_type, 'text')

    def test_genericipaddress_field(self):
        class MyForm(forms.ModelForm):
            ipaddress = forms.GenericIPAddressField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['ipaddress'].widget
        self.assertTrue(isinstance(widget, forms.TextInput))
        self.assertEqual(widget.input_type, 'text')

    def test_splitdatetime_field(self):
        class MyForm(forms.ModelForm):
            splitdatetime = forms.SplitDateTimeField()

        form_class = modelform_factory(model=Post, form=MyForm, exclude=[])
        widget = form_class().fields['splitdatetime'].widget
        self.assertTrue(isinstance(
            widget, forms.SplitDateTimeWidget))
        self.assertTrue(isinstance(
            widget.widgets[0], forms.DateInput))
        self.assertTrue(isinstance(
            widget.widgets[1], forms.TimeInput))
