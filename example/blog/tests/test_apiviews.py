from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import simplejson as json


from djadmin2 import apiviews
from djadmin2 import default
from djadmin2 import ModelAdmin2
from ..models import Post


class APITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(
            username='admin',
            is_staff=True)
        self.user.set_password('admin')
        self.user.save()

    def get_model_admin(self, model):
        return ModelAdmin2(model, default)


class IndexAPIViewTest(APITestCase):
    def test_response_ok(self):
        request = self.factory.get(reverse('admin2:api_index'))
        request.user = self.user
        view = apiviews.IndexAPIView.as_view(**default.get_api_index_kwargs())
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_view_permission(self):
        request = self.factory.get(reverse('admin2:api_index'))
        request.user = AnonymousUser()
        view = apiviews.IndexAPIView.as_view(**default.get_api_index_kwargs())
        self.assertRaises(PermissionDenied, view, request)


class ListCreateAPIViewTest(APITestCase):
    def test_response_ok(self):
        request = self.factory.get(reverse('admin2:blog_post_api_list'))
        request.user = self.user
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_view_permission(self):
        request = self.factory.get(reverse('admin2:blog_post_api_list'))
        request.user = AnonymousUser()
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        self.assertRaises(PermissionDenied, view, request)

    def test_list_includes_unicode_field(self):
        Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(reverse('admin2:blog_post_api_list'))
        request.user = self.user
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        response = view(request)
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertIn('"__str__": "Foo"', response.content)

    def test_pagination(self):
        request = self.factory.get(reverse('admin2:blog_post_api_list'))
        request.user = self.user
        model_admin = self.get_model_admin(Post)
        view = apiviews.ListCreateAPIView.as_view(
            **model_admin.get_api_list_kwargs())
        response = view(request)
        response.render()

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)
        # next and previous fields exist, but are null because we have no
        # content
        self.assertTrue('next' in data)
        self.assertEqual(data['next'], None)
        self.assertTrue('previous' in data)
        self.assertEqual(data['previous'], None)


class RetrieveUpdateDestroyAPIViewTest(APITestCase):
    def test_response_ok(self):
        post = Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(
            reverse('admin2:blog_post_api_detail',
            kwargs={'pk': post.pk}))
        request.user = self.user
        model_admin = self.get_model_admin(Post)
        view = apiviews.RetrieveUpdateDestroyAPIView.as_view(
            **model_admin.get_api_detail_kwargs())
        response = view(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)

    def test_view_permission(self):
        post = Post.objects.create(title='Foo', body='Bar')
        request = self.factory.get(
            reverse('admin2:blog_post_api_detail',
            kwargs={'pk': post.pk}))
        request.user = AnonymousUser()
        model_admin = self.get_model_admin(Post)
        view = apiviews.RetrieveUpdateDestroyAPIView.as_view(
            **model_admin.get_api_detail_kwargs())
        self.assertRaises(PermissionDenied, view, request, pk=post.pk)
