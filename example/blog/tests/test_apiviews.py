from django.utils import unittest
from django.test.client import RequestFactory


from djadmin2 import apiviews
from ..models import Post


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class IndexViewModelListCreateAPIViewTest(ViewTest):

    def test_response_ok(self):
        request = self.factory.get('/admin/api/blog/post/')
        response = apiviews.ModelListCreateAPIView.as_view(model=Post)(request)
        self.assertEqual(response.status_code, 200)

    def test_list_includes_unicode_field(self):
        Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get('/admin/api/blog/post/')
        response = apiviews.ModelListCreateAPIView.as_view(model=Post)(request)
        response.render()

        self.assertIn('"unicode": "Foo"', response.content)
