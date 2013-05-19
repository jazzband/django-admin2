from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.utils import simplejson as json


from djadmin2 import apiviews
from djadmin2 import default
from djadmin2.models import ModelAdmin2
from ..models import Post


class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def get_model_admin(self, model):
        return ModelAdmin2(model, default)


class IndexAPIViewTest(ViewTest):

    def test_response_ok(self):
        request = self.factory.get(reverse('admin2:api-index'))
        view = apiviews.IndexAPIView.as_view(**default.get_api_index_kwargs())
        response = view(request)
        self.assertEqual(response.status_code, 200)


class ListCreateAPIViewTest(ViewTest):

    def test_response_ok(self):
        request = self.factory.get(reverse('admin2:blog_post_api-list'))
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_list_includes_unicode_field(self):
        Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(reverse('admin2:blog_post_api-list'))
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        response = view(request)
        response.render()

        self.assertIn('"__str__": "Foo"', response.content)

    def test_pagination(self):
        request = self.factory.get(reverse('admin2:blog_post_api-list'))
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        response = view(request)
        response.render()
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)
        # next and previous fields exist, but are null because we have no
        # content
        self.assertTrue('next' in data)
        self.assertEqual(data['next'], None)
        self.assertTrue('previous' in data)
        self.assertEqual(data['previous'], None)


class RetrieveUpdateDestroyAPIViewTest(ViewTest):

    def test_response_ok(self):
        post = Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(
            reverse('admin2:blog_post_api-detail',
            kwargs={'pk': post.pk}))
        model_admin = self.get_model_admin(Post)
        view = apiviews.RetrieveUpdateDestroyAPIView.as_view(
            **model_admin.get_api_detail_kwargs())
        response = view(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
