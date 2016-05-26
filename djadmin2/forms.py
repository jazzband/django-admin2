# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy

from django.utils.translation import ugettext_lazy as _


# Translators : %(username)s will be replaced by the username_field name
# (default : username, but could be email, or something else)
ERROR_MESSAGE = _(
    "Please enter the correct %(username)s and password "
    "for a staff account. Note that both fields may be case-sensitive."
)


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    Liberally copied from django.contrib.admin.forms.AdminAuthenticationForm

    """
    error_messages = {
        'required': _("Please log in again, because your session has expired."),
    }
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=1,
        error_messages=error_messages
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise ValidationError(message % {
                    'username': self.username_field.verbose_name
                })
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise ValidationError(message % {
                    'username': self.username_field.verbose_name
                })
        return self.cleaned_data


class Admin2UserCreationForm(UserCreationForm):
    pass


class Admin2UserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(Admin2UserChangeForm, self).__init__(*args, **kwargs)
        print(self.fields['password'].help_text)
        self.fields['password'].help_text = _("Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using <a href=\"%s\">this form</a>." % self.get_update_password_url())

    def get_update_password_url(self):
        if self.instance and self.instance.pk:
            return reverse_lazy('admin2:password_change', args=[self.instance.pk])
        return 'password/'
