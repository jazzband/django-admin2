from django import forms
from django.test import TestCase

import floppyforms

from djadmin2.forms import floppify_widget, floppify_form, modelform_factory
from ..models import Post


class ModelFormFactoryTest(TestCase):
    def test_modelform_factory(self):
        form_class = modelform_factory(Post)
        self.assertTrue(form_class)
        field = form_class.base_fields['title']
        self.assertTrue(isinstance(field.widget, floppyforms.TextInput))


class GetFloppyformWidgetTest(TestCase):
    def assertExpectWidget(self, instance, new_class_,
        equal_attributes=None, new_attributes=None):
        new_instance = floppify_widget(instance)
        self.assertEqual(new_instance.__class__, new_class_)
        if equal_attributes:
            for attribute in equal_attributes:
                self.assertTrue(
                    hasattr(instance, attribute),
                    'Cannot check attribute %r, not available on original '
                    'widget %r' % (attribute, instance))
                self.assertTrue(
                    hasattr(new_instance, attribute),
                    'Cannot check attribute %r, not available on generated '
                    'widget %r' % (attribute, new_instance))
                old_attr = getattr(instance, attribute)
                new_attr = getattr(new_instance, attribute)
                self.assertEqual(old_attr, new_attr,
                    'Original widget\'s attribute was not copied: %r != %r' %
                    (old_attr, new_attr))
        if new_attributes:
            for attribute, value in new_attributes.items():
                self.assertTrue(
                    hasattr(new_instance, attribute),
                    'Cannot check new attribute %r, not available on '
                    'generated widget %r' % (attribute, new_instance))
                new_attr = getattr(new_instance, attribute)
                self.assertEqual(new_attr, value,
                    'Generated widget\'s attribute is not as expected: '
                    '%r != %r' % (new_attr, value))

    def test_created_widget_doesnt_leak_attributes_into_original_widget(self):
        widget = forms.TextInput()
        widget.is_required = True
        widget.attrs = {'placeholder': 'Search ...'}
        new_widget = floppify_widget(widget)
        self.assertFalse(widget.__dict__ is new_widget.__dict__)
        new_widget.is_required = False
        self.assertEqual(widget.is_required, True)
        new_widget.attrs['placeholder'] = 'Enter name'
        self.assertEqual(widget.attrs['placeholder'], 'Search ...')

    def test_copy_attribute_is_required(self):
        widget = forms.TextInput()
        widget.is_required = True
        self.assertExpectWidget(
            widget,
            floppyforms.TextInput,
            equal_attributes=['is_required'])

    # Test individual widgets

    def test_input_widget(self):
        self.assertExpectWidget(
            forms.widgets.Input(),
            floppyforms.widgets.Input)

        widget = forms.widgets.Input()
        widget.input_type = 'email'
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.Input,
            ['input_type'])

    def test_textinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.TextInput(),
            floppyforms.widgets.TextInput,
            ['input_type'],
            {'input_type': 'text'})

    def test_passwordinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.PasswordInput(),
            floppyforms.widgets.PasswordInput,
            ['input_type'],
            {'input_type': 'password'})

    def test_hiddeninput_widget(self):
        self.assertExpectWidget(
            forms.widgets.HiddenInput(),
            floppyforms.widgets.HiddenInput)

        widget = forms.widgets.HiddenInput()
        widget.is_hidden = False
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.HiddenInput,
            ['input_type'])

    def test_multiplehiddeninput_widget(self):
        self.assertExpectWidget(
            forms.widgets.MultipleHiddenInput(),
            floppyforms.widgets.MultipleHiddenInput)

        widget = forms.widgets.MultipleHiddenInput(choices=(
            ('no', 'Please, No!'),
            ('yes', 'Ok, why not.'),
        ))
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.MultipleHiddenInput,
            ['choices'])

    def test_fileinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.FileInput(),
            floppyforms.widgets.FileInput)

        widget = forms.widgets.FileInput()
        widget.needs_multipart_form = False
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.FileInput,
            ['needs_multipart_form'])

    def test_clearablefileinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.ClearableFileInput(),
            floppyforms.widgets.ClearableFileInput)

        widget = forms.widgets.ClearableFileInput()
        widget.initial_text = 'some random text 1'
        widget.input_text = 'some random text 2'
        widget.clear_checkbox_label = 'some random text 3'
        widget.template_with_initial = 'some random text 4'
        widget.template_with_clear = 'some random text 5'
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.ClearableFileInput,
            ['initial_text', 'input_text', 'clear_checkbox_label',
            'template_with_initial', 'template_with_clear'])

    def test_textarea_widget(self):
        self.assertExpectWidget(
            forms.widgets.Textarea(),
            floppyforms.widgets.Textarea)

    def test_dateinput_widget(self):
        self.assertExpectWidget(
            forms.DateInput(),
            floppyforms.DateInput)

        widget = forms.widgets.DateInput(format='DATE_FORMAT')
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.DateInput,
            ['format'],
            {'input_type': 'date'})

    def test_datetimeinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.DateTimeInput(),
            floppyforms.widgets.DateTimeInput)

        widget = forms.widgets.DateTimeInput(format='DATETIME_FORMAT')
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.DateTimeInput,
            ['format'],
            {'input_type': 'datetime'})

    def test_timeinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.TimeInput(),
            floppyforms.widgets.TimeInput)

        widget = forms.widgets.TimeInput(format='TIME_FORMAT')
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.TimeInput,
            ['format'],
            {'input_type': 'time'})

    def test_checkboxinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.CheckboxInput(),
            floppyforms.widgets.CheckboxInput)

        check_test = lambda v: False
        widget = forms.widgets.CheckboxInput(check_test=check_test)
        new_widget = floppify_widget(widget)
        self.assertEqual(widget.check_test, new_widget.check_test)
        self.assertTrue(new_widget.check_test is check_test)

    def test_select_widget(self):
        choices = (
            ('draft', 'Draft'),
            ('public', 'Public'),
        )

        self.assertExpectWidget(
            forms.widgets.Select(),
            floppyforms.widgets.Select)

        widget = forms.widgets.Select(choices=choices)
        widget.allow_multiple_selected = True
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.Select,
            ('choices', 'allow_multiple_selected',))

    def test_nullbooleanselect_widget(self):
        self.assertExpectWidget(
            forms.widgets.NullBooleanSelect(),
            floppyforms.widgets.NullBooleanSelect,
            ('choices', 'allow_multiple_selected',))
        
        widget = forms.widgets.NullBooleanSelect()
        widget.choices = list(widget.choices)

        value, label = widget.choices[0]
        widget.choices[0] = value, 'Maybe'

        self.assertExpectWidget(
            widget,
            floppyforms.widgets.NullBooleanSelect,
            ('choices', 'allow_multiple_selected',))

    def test_selectmultiple_widget(self):
        choices = (
            ('draft', 'Draft'),
            ('public', 'Public'),
        )

        self.assertExpectWidget(
            forms.widgets.SelectMultiple(),
            floppyforms.widgets.SelectMultiple)

        widget = forms.widgets.SelectMultiple(choices=choices)
        widget.allow_multiple_selected = False
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.SelectMultiple,
            ('choices', 'allow_multiple_selected',))

    def test_radioselect_widget(self):
        choices = (
            ('draft', 'Draft'),
            ('public', 'Public'),
        )

        self.assertExpectWidget(
            forms.widgets.RadioSelect(),
            floppyforms.widgets.RadioSelect)

        self.assertExpectWidget(
            forms.widgets.RadioSelect(choices=choices),
            floppyforms.widgets.RadioSelect,
            ('choices', 'allow_multiple_selected',))

        widget = forms.widgets.RadioSelect(renderer='custom renderer')
        # don't overwrite widget with floppyform widget if a custom renderer
        # was used. We cannot copy this over since floppyform doesn't use the
        # renderer.
        self.assertExpectWidget(
            widget,
            forms.widgets.RadioSelect)

    def test_checkboxselectmultiple_widget(self):
        choices = (
            ('draft', 'Draft'),
            ('public', 'Public'),
        )

        self.assertExpectWidget(
            forms.widgets.CheckboxSelectMultiple(),
            floppyforms.widgets.CheckboxSelectMultiple)

        self.assertExpectWidget(
            forms.widgets.CheckboxSelectMultiple(choices=choices),
            floppyforms.widgets.CheckboxSelectMultiple,
            ('choices', 'allow_multiple_selected',))

    def test_multi_widget(self):
        self.assertExpectWidget(
            forms.widgets.MultiWidget([]),
            floppyforms.widgets.MultiWidget)

        text_input = forms.widgets.TextInput()
        widget = forms.widgets.MultiWidget([text_input])
        new_widget = floppify_widget(widget)
        self.assertEqual(widget.widgets, new_widget.widgets)
        self.assertTrue(new_widget.widgets[0] is text_input)

    def test_splitdatetime_widget(self):
        widget = forms.widgets.SplitDateTimeWidget()
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.SplitDateTimeWidget)

        widget = forms.widgets.SplitDateTimeWidget(
            date_format='DATE_FORMAT', time_format='TIME_FORMAT')
        new_widget = floppify_widget(widget)
        self.assertTrue(isinstance(
            new_widget.widgets[0], floppyforms.widgets.DateInput))
        self.assertTrue(isinstance(
            new_widget.widgets[1], floppyforms.widgets.TimeInput))
        self.assertEqual(new_widget.widgets[0].format, 'DATE_FORMAT')
        self.assertEqual(new_widget.widgets[1].format, 'TIME_FORMAT')

    def test_splithiddendatetime_widget(self):
        widget = forms.widgets.SplitHiddenDateTimeWidget()
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.SplitHiddenDateTimeWidget)

        widget = forms.widgets.SplitHiddenDateTimeWidget(
            date_format='DATE_FORMAT', time_format='TIME_FORMAT')
        new_widget = floppify_widget(widget)
        self.assertTrue(isinstance(
            new_widget.widgets[0], floppyforms.widgets.DateInput))
        self.assertTrue(isinstance(
            new_widget.widgets[1], floppyforms.widgets.TimeInput))
        self.assertEqual(new_widget.widgets[0].format, 'DATE_FORMAT')
        self.assertEqual(new_widget.widgets[0].is_hidden, True)
        self.assertEqual(new_widget.widgets[1].format, 'TIME_FORMAT')
        self.assertEqual(new_widget.widgets[1].is_hidden, True)

    def test_selectdate_widget(self):
        self.assertExpectWidget(
            forms.extras.widgets.SelectDateWidget(),
            floppyforms.widgets.SelectDateWidget)

        widget = forms.extras.widgets.SelectDateWidget(
            attrs={'attribute': 'value'},
            years=[2010, 2011, 2012, 2013],
            required=False)
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.SelectDateWidget,
            ('attrs', 'years', 'required'))


class ModelFormTest(TestCase):
    def test_custom_base_form(self):
        class MyForm(forms.ModelForm):
            pass

        form_class = modelform_factory(model=Post, form=MyForm)
        form = form_class()
        self.assertTrue(isinstance(
            form.fields['title'].widget,
            floppyforms.widgets.TextInput))

    def test_declared_fields(self):
        class MyForm(forms.ModelForm):
            subtitle = forms.CharField()

        form_class = modelform_factory(model=Post, form=MyForm)
        self.assertTrue(isinstance(
            form_class.base_fields['subtitle'].widget,
            floppyforms.widgets.TextInput))
        self.assertTrue(isinstance(
            form_class.declared_fields['subtitle'].widget,
            floppyforms.widgets.TextInput))

        self.assertTrue(isinstance(
            form_class.base_fields['title'].widget,
            floppyforms.widgets.TextInput))
        # title is not defined in declared fields

    def test_additional_form_fields(self):
        class MyForm(forms.ModelForm):
            subtitle = forms.CharField()

        form_class = modelform_factory(model=Post, form=MyForm)
        form = form_class()
        self.assertTrue(isinstance(
            form.fields['subtitle'].widget,
            floppyforms.widgets.TextInput))

    def test_subclassing_forms(self):
        class MyForm(forms.ModelForm):
            subtitle = forms.CharField()

            class Meta:
                model = Post

        class ChildForm(MyForm):
            created = forms.DateField()

        form_class = modelform_factory(model=Post, form=ChildForm)
        form = form_class()
        self.assertTrue(isinstance(
            form.fields['title'].widget,
            floppyforms.widgets.TextInput))
        self.assertTrue(isinstance(
            form.fields['subtitle'].widget,
            floppyforms.widgets.TextInput))
        self.assertTrue(isinstance(
            form.fields['created'].widget,
            floppyforms.widgets.DateInput))


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

        form_class = floppify_form(MyForm)
        widget = form_class().fields['email'].widget
        self.assertFalse(isinstance(widget, floppyforms.widgets.EmailInput))
        self.assertTrue(isinstance(widget, floppyforms.widgets.Textarea))

    def test_float_field(self):
        class MyForm(forms.ModelForm):
            float = forms.FloatField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['float'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.NumberInput))
        self.assertEqual(widget.input_type, 'number')

    def test_decimal_field(self):
        class MyForm(forms.ModelForm):
            decimal = forms.DecimalField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['decimal'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.NumberInput))
        self.assertEqual(widget.input_type, 'number')

    def test_integer_field(self):
        class MyForm(forms.ModelForm):
            integer = forms.IntegerField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['integer'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.NumberInput))
        self.assertEqual(widget.input_type, 'number')

    def test_email_field(self):
        class MyForm(forms.ModelForm):
            email = forms.EmailField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['email'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.EmailInput))
        self.assertEqual(widget.input_type, 'email')

    def test_url_field(self):
        class MyForm(forms.ModelForm):
            url = forms.URLField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['url'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.URLInput))
        self.assertEqual(widget.input_type, 'url')

    def test_slug_field(self):
        class MyForm(forms.ModelForm):
            slug = forms.SlugField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['slug'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.SlugInput))
        self.assertEqual(widget.input_type, 'text')

    def test_ipaddress_field(self):
        class MyForm(forms.ModelForm):
            ipaddress = forms.IPAddressField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['ipaddress'].widget
        self.assertTrue(isinstance(widget, floppyforms.widgets.IPAddressInput))
        self.assertEqual(widget.input_type, 'text')

    def test_splitdatetime_field(self):
        class MyForm(forms.ModelForm):
            splitdatetime = forms.SplitDateTimeField()

        form_class = modelform_factory(model=Post, form=MyForm)
        widget = form_class().fields['splitdatetime'].widget
        self.assertTrue(isinstance(
            widget, floppyforms.widgets.SplitDateTimeWidget))
        self.assertTrue(isinstance(
            widget.widgets[0], floppyforms.widgets.DateInput))
        self.assertTrue(isinstance(
            widget.widgets[1], floppyforms.widgets.TimeInput))
