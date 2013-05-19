from django.test import TestCase
from django.contrib.auth.models import User

from django.contrib.admin.sites import LOGIN_FORM_KEY
from django.contrib.auth import REDIRECT_FIELD_NAME


class Admin2AuthViewsIntegrationTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@example.com', 'password'
        )

        self.admin_login = {
            'username': self.admin_user.username,
            'password': 'password',
            LOGIN_FORM_KEY: 1,
            REDIRECT_FIELD_NAME: '/admin2/'
        }

    def test_login(self):
        response = self.client.get('/admin2/')
        self.assertEqual(response.status_code, 200)
        login = self.client.post('/admin2/', self.admin_login)
        # assert client is logged in
        self.assertEqual(self.client.session['_auth_user_id'],
                         self.admin_user.pk)
        # response is a redirect to the dashboard
        self.assertRedirects(login, '/admin2/')

    def test_logout(self):
        self.client.login(username=self.admin_user.username,
                          password='password')
        self.client.get('/admin2/')
        # assert client is logged in
        self.assertEqual(self.client.session['_auth_user_id'],
                         self.admin_user.pk)
        logout = self.client.get('/admin2/logout/')
        self.assertEqual(logout.status_code, 200)
        # assert client is not logged in
        self.assertFalse('_auth_user_id' in self.client.session.keys())
