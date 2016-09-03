from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.utils.encoding import force_text

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


@override_settings(ROOT_URLCONF='djadmin2.tests.urls')
class CustomLoginViewTest(TestCase):

    def test_view_ok(self):
        response = self.client.get(reverse("admin2:dashboard"))
        self.assertInHTML('<h3 class="panel-title">Custom login view</h3>', force_text(response.content))
