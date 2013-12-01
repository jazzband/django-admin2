from django.test import TestCase
from django.views.generic import View

from .. import views


class AdminViewTest(TestCase):

    def setUp(self):
        self.admin_view = views.AdminView(r'^$', views.ModelListView, name='admin-view')

    def test_url(self):
        self.assertEquals(self.admin_view.url, r'^$')

    def test_view(self):
        self.assertEquals(self.admin_view.view, views.ModelListView)

    def test_name(self):
        self.assertEquals(self.admin_view.name, 'admin-view')
