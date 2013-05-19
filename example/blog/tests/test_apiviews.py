from django.utils import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse


from djadmin2 import apiviews
from ..models import Post


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()


class ListCreateAPIViewTest(ViewTest):

    def test_response_ok(self):
        request = self.factory.get(reverse('admin2:blog_post_api-index'))
        response = apiviews.ListCreateAPIView.as_view(model=Post)(request)
        self.assertEqual(response.status_code, 200)

    def test_list_includes_unicode_field(self):
        Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(reverse('admin2:blog_post_api-index'))
        response = apiviews.ListCreateAPIView.as_view(model=Post)(request)
        response.render()

        self.assertIn('"__str__": "Foo"', response.content)


class RetrieveUpdateDestroyAPIViewTest(ViewTest):

    def test_response_ok(self):
        post = Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(reverse('admin2:blog_post_api-detail', kwargs={'pk': post.pk}))
        response = apiviews.RetrieveUpdateDestroyAPIView.as_view(model=Post)(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
