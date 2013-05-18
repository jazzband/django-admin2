from django.utils import unittest
from django.test.client import RequestFactory

from djadmin2 import views

class ViewTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class IndexViewTest(ViewTest):
    def test_response_ok(self):
        request = self.factory.get('/admin/blog/post/')
        response = views.IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class ModelListViewTest(ViewTest):
    pass


class ModelDetailViewTest(ViewTest):
    pass


class ModelEditFormViewTest(ViewTest):
    pass


class ModelAddFormViewTest(ViewTest):
    pass


class ModelDeleteViewTest(ViewTest):
    pass

