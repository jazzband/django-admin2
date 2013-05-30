from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

import floppyforms

import djadmin2
from blog.admin2 import UserAdmin2


class UserAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(
            username='admin',
            is_staff=True,
            is_superuser=True)
        self.user.set_password('admin')
        self.user.save()

    def test_create_form_uses_floppyform_widgets(self):
        form = UserAdmin2.create_form_class()
        self.assertTrue(
            isinstance(form.fields['username'].widget,
                       floppyforms.TextInput))

        request = self.factory.get(reverse('admin2:auth_user_create'))
        request.user = self.user
        model_admin = UserAdmin2(User, djadmin2.default)
        view = model_admin.create_view.as_view(
            **model_admin.get_create_kwargs())
        response = view(request)
        form = response.context_data['form']
        self.assertTrue(
            isinstance(form.fields['username'].widget,
                       floppyforms.TextInput))

    def test_update_form_uses_floppyform_widgets(self):
        form = UserAdmin2.update_form_class()
        self.assertTrue(
            isinstance(form.fields['username'].widget,
                       floppyforms.TextInput))
        self.assertTrue(
            isinstance(form.fields['date_joined'].widget,
                       floppyforms.DateTimeInput))

        request = self.factory.get(
            reverse('admin2:auth_user_update', args=(self.user.pk,)))
        request.user = self.user
        model_admin = UserAdmin2(User, djadmin2.default)
        view = model_admin.update_view.as_view(
            **model_admin.get_update_kwargs())
        response = view(request, pk=self.user.pk)
        form = response.context_data['form']
        self.assertTrue(
            isinstance(form.fields['username'].widget,
                       floppyforms.TextInput))
        self.assertTrue(
            isinstance(form.fields['date_joined'].widget,
                       floppyforms.DateTimeInput))
