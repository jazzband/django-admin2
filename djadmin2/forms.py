import floppyforms
from copy import deepcopy

import django.forms
import django.forms.models
import django.forms.extras.widgets


_WIDGET_COMMON_ATTRIBUTES = (
    'is_hidden',
    'needs_multipart_form',
    'is_localized',
    'is_required')

_WIDGET_COMMON_ARGUMENTS = ('attrs',)


def _copy_attributes(original, new_widget, attributes):
        for attr in attributes:
            original_value = getattr(original, attr)
            original_value = deepcopy(original_value)
            setattr(new_widget, attr, original_value)


def _create_widget(widget_class, copy_attributes=(), init_arguments=()):
    # attach defaults that apply for all widgets
    copy_attributes = tuple(copy_attributes) + _WIDGET_COMMON_ATTRIBUTES
    init_arguments = tuple(init_arguments) + _WIDGET_COMMON_ARGUMENTS

    def create_new_widget(original):
        kwargs = {}
        for argname in init_arguments:
            kwargs[argname] = getattr(original, argname)
        new_widget = widget_class(**kwargs)
        _copy_attributes(
            original,
            new_widget,
            copy_attributes)
        return new_widget
    return create_new_widget


def _create_radioselect(original):
    # return original widget if the renderer is something else than what
    # django ships with by default. This means if this condition evaluates to
    # true, then a custom renderer was specified. We cannot emulate its
    # behaviour so we shouldn't guess and just return the original widget
    if original.renderer is not django.forms.widgets.RadioFieldRenderer:
        return original
    create_new_widget = _create_widget(
        floppyforms.widgets.RadioSelect,
        ('allow_multiple_selected',))
    return create_new_widget(original)


def _create_splitdatetimewidget(widget_class):
    def create_new_widget(original):
        new_widget = widget_class(
            attrs=original.attrs,
            date_format=original.widgets[0].format,
            time_format=original.widgets[1].format)
        _copy_attributes(original, new_widget, _WIDGET_COMMON_ARGUMENTS)
        return new_widget
    return create_new_widget


def _create_multiwidget(widget_class, copy_attributes=(), init_arguments=()):
    create_new_widget = _create_widget(widget_class, copy_attributes,
                                       init_arguments)

    def create_new_multiwidget(original):
        multiwidget = create_new_widget(original)
        multiwidget.widgets = [
            get_floppyform_widget(widget)
            for widget in multiwidget.widgets]
        return multiwidget
    return create_new_multiwidget


# this dictionary keeps a mapping from django's widget classes to a callable
# that will accept an instance of this class. It will return a new instance of
# a corresponding floppyforms widget, with the same semantics -- all relevant
# attributes will be copied to the new widget.
_django_to_floppyforms_widget = {
    django.forms.widgets.Input:
        _create_widget(floppyforms.widgets.Input, ('input_type',)),
    django.forms.widgets.TextInput:
        _create_widget(floppyforms.widgets.TextInput, ('input_type',)),
    django.forms.widgets.PasswordInput:
        _create_widget(floppyforms.widgets.PasswordInput, ('input_type',)),
    django.forms.widgets.HiddenInput:
        _create_widget(floppyforms.widgets.HiddenInput, ('input_type',)),
    django.forms.widgets.MultipleHiddenInput:
        _create_widget(
            floppyforms.widgets.MultipleHiddenInput,
            ('input_type',),
            init_arguments=('choices',)),
    django.forms.widgets.FileInput:
        _create_widget(floppyforms.widgets.FileInput, ('input_type',)),
    django.forms.widgets.ClearableFileInput:
        _create_widget(
            floppyforms.widgets.ClearableFileInput,
            (
                'input_type', 'initial_text', 'input_text',
                'clear_checkbox_label', 'template_with_initial',
                'template_with_clear')),
    django.forms.widgets.Textarea:
        _create_widget(floppyforms.widgets.Textarea),
    django.forms.widgets.DateInput:
        _create_widget(
            floppyforms.widgets.DateInput,
            ('input_type',),
            init_arguments=('format',)),
    django.forms.widgets.DateTimeInput:
        _create_widget(
            floppyforms.widgets.DateTimeInput,
            ('input_type',),
            init_arguments=('format',)),
    django.forms.widgets.TimeInput:
        _create_widget(
            floppyforms.widgets.TimeInput,
            ('input_type',),
            init_arguments=('format',)),
    django.forms.widgets.CheckboxInput:
        _create_widget(floppyforms.widgets.CheckboxInput, ('check_test',)),
    django.forms.widgets.Select:
        _create_widget(
            floppyforms.widgets.Select,
            ('allow_multiple_selected',)),
    django.forms.widgets.NullBooleanSelect:
        _create_widget(
            floppyforms.widgets.NullBooleanSelect,
            ('allow_multiple_selected',)),
    django.forms.widgets.SelectMultiple:
        _create_widget(
            floppyforms.widgets.SelectMultiple,
            ('allow_multiple_selected',)),
    django.forms.widgets.RadioSelect:
        _create_radioselect,
    django.forms.widgets.CheckboxSelectMultiple:
        _create_widget(floppyforms.widgets.CheckboxSelectMultiple),
    django.forms.widgets.MultiWidget:
        _create_widget(
            floppyforms.widgets.MultiWidget,
            init_arguments=('widgets',)),
    django.forms.widgets.SplitDateTimeWidget:
        _create_splitdatetimewidget(
            floppyforms.widgets.SplitDateTimeWidget),
    django.forms.widgets.SplitHiddenDateTimeWidget:
        _create_splitdatetimewidget(
            floppyforms.widgets.SplitHiddenDateTimeWidget),
    django.forms.extras.widgets.SelectDateWidget:
        _create_widget(
            floppyforms.widgets.SelectDateWidget,
            init_arguments=('years', 'required')),
}


def get_floppyform_widget(widget):
    '''
    Get an instance of django.forms.widgets.Widget and return a new widget
    instance but using the corresponding floppyforms widget class.

    Only original django widgets will be replaced with a floppyforms version.
    The widget will be returned unaltered if it is not known, e.g. if it's a
    custom widget from a third-party app.
    '''
    create_widget_class = _django_to_floppyforms_widget.get(
        widget.__class__, None)
    if create_widget_class is not None:
        return create_widget_class(widget)
    return widget


def modelform_factory(model, form=django.forms.models.ModelForm, fields=None,
                      exclude=None, formfield_callback=None,  widgets=None):
    form_class = django.forms.models.modelform_factory(
        model=model,
        form=form,
        fields=fields,
        exclude=exclude,
        formfield_callback=formfield_callback,
        widgets=widgets)
    for field in form_class.base_fields.values():
        field.widget = get_floppyform_widget(field.widget)
    return form_class
