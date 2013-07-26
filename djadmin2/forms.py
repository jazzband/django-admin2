# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from copy import deepcopy

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import django.forms
import django.forms.models
import django.forms.extras.widgets
from django.utils.translation import ugettext_lazy

import floppyforms


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
        ('choices', 'allow_multiple_selected',))
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
            floppify_widget(widget)
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
            init_arguments=('format',)),
    django.forms.widgets.DateTimeInput:
        _create_widget(
            floppyforms.widgets.DateTimeInput,
            init_arguments=('format',)),
    django.forms.widgets.TimeInput:
        _create_widget(
            floppyforms.widgets.TimeInput,
            init_arguments=('format',)),
    django.forms.widgets.CheckboxInput:
        _create_widget(floppyforms.widgets.CheckboxInput, ('check_test',)),
    django.forms.widgets.Select:
        _create_widget(
            floppyforms.widgets.Select,
            ('choices', 'allow_multiple_selected',)),
    django.forms.widgets.NullBooleanSelect:
        _create_widget(
            floppyforms.widgets.NullBooleanSelect,
            ('choices', 'allow_multiple_selected',)),
    django.forms.widgets.SelectMultiple:
        _create_widget(
            floppyforms.widgets.SelectMultiple,
            ('choices', 'allow_multiple_selected',)),
    django.forms.widgets.RadioSelect:
        _create_radioselect,
    django.forms.widgets.CheckboxSelectMultiple:
        _create_widget(
            floppyforms.widgets.CheckboxSelectMultiple,
            ('choices', 'allow_multiple_selected',)),
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

_django_field_to_floppyform_widget = {
    django.forms.fields.FloatField:
        _create_widget(floppyforms.widgets.NumberInput),
    django.forms.fields.DecimalField:
        _create_widget(floppyforms.widgets.NumberInput),
    django.forms.fields.IntegerField:
        _create_widget(floppyforms.widgets.NumberInput),
    django.forms.fields.EmailField:
        _create_widget(floppyforms.widgets.EmailInput),
    django.forms.fields.URLField:
        _create_widget(floppyforms.widgets.URLInput),
    django.forms.fields.SlugField:
        _create_widget(floppyforms.widgets.SlugInput),
    django.forms.fields.IPAddressField:
        _create_widget(floppyforms.widgets.IPAddressInput),
    django.forms.fields.SplitDateTimeField:
        _create_splitdatetimewidget(floppyforms.widgets.SplitDateTimeWidget),
}


def floppify_widget(widget, field=None):
    '''
    Get an instance of django.forms.widgets.Widget and return a new widget
    instance but using the corresponding floppyforms widget class.

    Only original django widgets will be replaced with a floppyforms version.
    The widget will be returned unaltered if it is not known, e.g. if it's a
    custom widget from a third-party app.

    The optional parameter ``field`` can be used to influence the widget
    creation further. This is useful since floppyforms supports more widgets
    than django does. For example is django using a ``TextInput`` for a
    ``EmailField``, but floppyforms has a better suiting widget called
    ``EmailInput``. If a widget is found specifically for the passed in
    ``field``, it will take precendence to the first parameter ``widget``
    which will effectively be ignored.
    '''
    if field is not None:
        create_widget = _django_field_to_floppyform_widget.get(
            field.__class__)
        if create_widget is not None:
            # check if the default widget was replaced by a different one, in
            # that case we cannot create the field specific floppyforms
            # widget.
            if field.widget.__class__ is field.__class__.widget:
                return create_widget(widget)
    create_widget = _django_to_floppyforms_widget.get(widget.__class__)
    if create_widget is not None:
        return create_widget(widget)
    return widget


def floppify_form(form_class):
    '''
    Take a normal form and return a subclass of that form that replaces all
    django widgets with the corresponding floppyforms widgets.
    '''
    new_form_class = type(form_class.__name__, (form_class,), {})
    for field in new_form_class.base_fields.values():
        field.widget = floppify_widget(field.widget, field=field)
    return new_form_class


def modelform_factory(model, form=django.forms.models.ModelForm, fields=None,
                      exclude=None, formfield_callback=None, widgets=None):
    form_class = django.forms.models.modelform_factory(
        model=model,
        form=form,
        fields=fields,
        exclude=exclude,
        formfield_callback=formfield_callback,
        widgets=widgets)
    return floppify_form(form_class)


# Translators : %(username)s will be replaced by the username_field name
# (default : username, but could be email, or something else)
ERROR_MESSAGE = ugettext_lazy("Please enter the correct %(username)s and password "
        "for a staff account. Note that both fields may be case-sensitive.")


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    Liberally copied from django.contrib.admin.forms.AdminAuthenticationForm

    """
    error_messages = {
        'required': ugettext_lazy("Please log in again, because your session has expired."),
    }
    this_is_the_login_form = django.forms.BooleanField(widget=floppyforms.HiddenInput,
            initial=1, error_messages=error_messages)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise floppyforms.ValidationError(message % {
                    'username': self.username_field.verbose_name
                })
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise floppyforms.ValidationError(message % {
                    'username': self.username_field.verbose_name
                })
        return self.cleaned_data


UserCreationForm = floppify_form(UserCreationForm)
UserChangeForm = floppify_form(UserChangeForm)
