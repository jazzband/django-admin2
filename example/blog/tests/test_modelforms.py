import floppyforms
from django import forms
from django.test import TestCase
from djadmin2.forms import get_floppyform_widget, modelform_factory
from ..models import Post


class ModelFormFactoryTest(TestCase):
    def test_modelform_factory(self):
        form_class = modelform_factory(Post)
        self.assertTrue(form_class)
        field = form_class.base_fields['title']
        self.assertTrue(isinstance(field.widget, floppyforms.TextInput))


class GetFloppyformWidgetTest(TestCase):
    def assertExpectWidget(self, instance, new_class_,
        equal_attributes=None):
        new_instance = get_floppyform_widget(instance)
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

    def test_created_widget_doesnt_leak_attributes_into_original_widget(self):
        widget = forms.TextInput()
        widget.is_required = True
        widget.attrs = {'placeholder': 'Search ...'}
        new_widget = get_floppyform_widget(widget)
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
            floppyforms.widgets.TextInput)

    def test_passwordinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.PasswordInput(),
            floppyforms.widgets.PasswordInput)

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
            ['format'])

    def test_datetimeinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.DateTimeInput(),
            floppyforms.widgets.DateTimeInput)

        widget = forms.widgets.DateTimeInput(format='DATETIME_FORMAT')
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.DateTimeInput,
            ['format'])

    def test_timeinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.TimeInput(),
            floppyforms.widgets.TimeInput)

        widget = forms.widgets.TimeInput(format='TIME_FORMAT')
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.TimeInput,
            ['format'])

    def test_checkboxinput_widget(self):
        self.assertExpectWidget(
            forms.widgets.CheckboxInput(),
            floppyforms.widgets.CheckboxInput)

        check_test = lambda v: False
        widget = forms.widgets.CheckboxInput(check_test=check_test)
        new_widget = get_floppyform_widget(widget)
        self.assertEqual(widget.check_test, new_widget.check_test)
        self.assertTrue(new_widget.check_test is check_test)

    def test_select_widget(self):
        self.assertExpectWidget(
            forms.widgets.Select(),
            floppyforms.widgets.Select)

        widget = forms.widgets.Select()
        widget.allow_multiple_selected = True
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.Select,
            ('allow_multiple_selected',))

    def test_nullbooleanselect_widget(self):
        self.assertExpectWidget(
            forms.widgets.NullBooleanSelect(),
            floppyforms.widgets.NullBooleanSelect)

    def test_selectmultiple_widget(self):
        self.assertExpectWidget(
            forms.widgets.SelectMultiple(),
            floppyforms.widgets.SelectMultiple)

        widget = forms.widgets.SelectMultiple()
        widget.allow_multiple_selected = False
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.SelectMultiple,
            ('allow_multiple_selected',))

    def test_radioselect_widget(self):
        self.assertExpectWidget(
            forms.widgets.RadioSelect(),
            floppyforms.widgets.RadioSelect)

        widget = forms.widgets.RadioSelect(renderer='custom renderer')
        # don't overwrite widget with floppyform widget if a custom renderer
        # was used. We cannot copy this over since floppyform doesn't use the
        # renderer.
        self.assertExpectWidget(
            widget,
            forms.widgets.RadioSelect)

    def test_checkboxselectmultiple_widget(self):
        self.assertExpectWidget(
            forms.widgets.CheckboxSelectMultiple(),
            floppyforms.widgets.CheckboxSelectMultiple)

    def test_multi_widget(self):
        self.assertExpectWidget(
            forms.widgets.MultiWidget([]),
            floppyforms.widgets.MultiWidget)

        text_input = forms.widgets.TextInput()
        widget = forms.widgets.MultiWidget([text_input])
        new_widget = get_floppyform_widget(widget)
        self.assertEqual(widget.widgets, new_widget.widgets)
        self.assertTrue(new_widget.widgets[0] is text_input)

    def test_splitdatetime_widget(self):
        widget = forms.widgets.SplitDateTimeWidget()
        self.assertExpectWidget(
            widget,
            floppyforms.widgets.SplitDateTimeWidget)

        widget = forms.widgets.SplitDateTimeWidget(
            date_format='DATE_FORMAT', time_format='TIME_FORMAT')
        new_widget = get_floppyform_widget(widget)
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
        new_widget = get_floppyform_widget(widget)
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
