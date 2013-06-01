from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse

from .test_apiviews import APITestCase


class UserAPITest(APITestCase):
    def test_list_response_ok(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin2:auth_user_api_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_permission(self):
        response = self.client.get(reverse('admin2:auth_user_api_list'))
        self.assertEqual(response.status_code, 403)

    def test_detail_response_ok(self):
        self.client.login(username='admin', password='admin')
        user = User.objects.create_user(
            username='Foo',
            password='bar')
        response = self.client.get(
            reverse('admin2:auth_user_api_detail', args=(user.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_permission(self):
        user = User.objects.create_user(
            username='Foo',
            password='bar')
        response = self.client.get(
            reverse('admin2:auth_user_api_detail', args=(user.pk,)))
        self.assertEqual(response.status_code, 403)


class GroupAPITest(APITestCase):
    def test_list_response_ok(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin2:auth_group_api_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_permission(self):
        response = self.client.get(reverse('admin2:auth_group_api_list'))
        self.assertEqual(response.status_code, 403)

    def test_detail_response_ok(self):
        self.client.login(username='admin', password='admin')
        group = Group.objects.create(name='group')
        response = self.client.get(
            reverse('admin2:auth_group_api_detail', args=(group.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_permission(self):
        group = Group.objects.create(name='group')
        response = self.client.get(
            reverse('admin2:auth_group_api_detail', args=(group.pk,)))
        self.assertEqual(response.status_code, 403)
