from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.test import TestCase


class UserAPITest(TestCase):
    def test_list_response_ok(self):
        response = self.client.get(reverse('admin2:auth_user_api-list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_response_ok(self):
        user = User.objects.create_user(
            username='Foo',
            password='bar')
        response = self.client.get(
            reverse('admin2:auth_user_api-detail', args=(user.pk,)))
        self.assertEqual(response.status_code, 200)


class GroupAPITest(TestCase):
    def test_list_response_ok(self):
        response = self.client.get(reverse('admin2:auth_group_api-list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_response_ok(self):
        group = Group.objects.create(name='group')
        response = self.client.get(
            reverse('admin2:auth_group_api-detail', args=(group.pk,)))
        self.assertEqual(response.status_code, 200)
