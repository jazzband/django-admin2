from django.utils import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse


from djadmin2 import apiviews
from djadmin2 import default
from djadmin2.models import ModelAdmin2
from ..models import Post


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def get_model_admin(self, model):
        return ModelAdmin2(model, default)


class ListCreateAPIViewTest(ViewTest):

    def test_response_ok(self):
        request = self.factory.get(reverse('admin2:blog_post_api-list'))
        modeladmin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **modeladmin.get_api_list_kwargs())
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_list_includes_unicode_field(self):
        Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(reverse('admin2:blog_post_api-list'))
        modeladmin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **modeladmin.get_api_list_kwargs())
        response = view(request)
        response.render()

        self.assertIn('"__str__": "Foo"', response.content)


class RetrieveUpdateDestroyAPIViewTest(ViewTest):

    def test_response_ok(self):
        post = Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(
            reverse('admin2:blog_post_api-detail',
            kwargs={'pk': post.pk}))
        modeladmin = self.get_model_admin(Post)
        view = apiviews.RetrieveUpdateDestroyAPIView.as_view(
            **modeladmin.get_api_detail_kwargs())
        response = view(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
