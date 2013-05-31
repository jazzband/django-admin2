from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ..models import Post, Comment


class BaseIntegrationTest(TestCase):
    """
    Base TestCase for integration tests.
    """
    def setUp(self):
        self.client = Client()
        self.user = get_user_model()(username='user', is_staff=True,
                                     is_superuser=True)
        self.user.set_password("password")
        self.user.save()
        self.client.login(username='user', password='password')


class AdminIndexTest(BaseIntegrationTest):
    def test_view_ok(self):
        response = self.client.get(reverse("admin2:dashboard"))
        self.assertContains(response, reverse("admin2:blog_post_index"))


class PostListTest(BaseIntegrationTest):
    def test_view_ok(self):
        post = Post.objects.create(title="a_post_title", body="body")
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertContains(response, post.title)

    def test_actions_displayed(self):
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertInHTML('<option value="delete_selected">Delete selected items</option>', response.content)

    def test_delete_selected_post(self):
        post = Post.objects.create(title="a_post_title", body="body")
        params = {'action': 'delete_selected', 'selected_model_pk': str(post.pk)}
        response = self.client.post(reverse("admin2:blog_post_index"), params)
        self.assertInHTML('<p>Are you sure you want to delete the selected post? All of the following items will be deleted:</p>', response.content)

    def test_delete_selected_post_confirmation(self):
        post = Post.objects.create(title="a_post_title", body="body")
        params = {'action': 'delete_selected', 'selected_model_pk': str(post.pk), 'confirmed': 'yes'}
        response = self.client.post(reverse("admin2:blog_post_index"), params)
        self.assertRedirects(response, reverse("admin2:blog_post_index"))


class PostDetailViewTest(BaseIntegrationTest):
    def test_view_ok(self):
        post = Post.objects.create(title="a_post_title", body="body")
        response = self.client.get(reverse("admin2:blog_post_detail",
                                           args=(post.pk, )))
        self.assertContains(response, post.title)


class PostCreateViewTest(BaseIntegrationTest):
    def test_view_ok(self):
        response = self.client.get(reverse("admin2:blog_post_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        post_data = {
            "comment_set-TOTAL_FORMS": u'2',
            "comment_set-INITIAL_FORMS": u'0',
            "comment_set-MAX_NUM_FORMS": u'',
            "comment_set-0-body": u'Comment Body',
            "title": "a_post_title",
            "body": "a_post_body",
        }

        response = self.client.post(reverse("admin2:blog_post_create"),
                                    post_data,
                                    follow=True)
        self.assertTrue(Post.objects.filter(title="a_post_title").exists())
        Post.objects.get(title="a_post_title")
        Comment.objects.get(body="Comment Body")
        self.assertRedirects(response, reverse("admin2:blog_post_index"))

    def test_save_and_add_another_redirects_to_create(self):
        """
        Tests that choosing 'Save and add another' from the model create
        page redirects the user to the model create page.
        """
        post_data = {
            "comment_set-TOTAL_FORMS": u'2',
            "comment_set-INITIAL_FORMS": u'0',
            "comment_set-MAX_NUM_FORMS": u'',
            "title": "a_post_title",
            "body": "a_post_body",
            "_addanother": ""
        }
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse("admin2:blog_post_create"),
                                    post_data)
        Post.objects.get(title='a_post_title')
        self.assertRedirects(response, reverse("admin2:blog_post_create"))

    def test_save_and_continue_editing_redirects_to_update(self):
        """
        Tests that choosing "Save and continue editing" redirects
        the user to the model update form.
        """
        post_data = {
            "comment_set-TOTAL_FORMS": u'2',
            "comment_set-INITIAL_FORMS": u'0',
            "comment_set-MAX_NUM_FORMS": u'',
            "title": "Unique",
            "body": "a_post_body",
            "_continue": ""
        }
        response = self.client.post(reverse("admin2:blog_post_create"),
                                    post_data)
        post = Post.objects.get(title="Unique")
        self.assertRedirects(response, reverse("admin2:blog_post_update",
                                               args=(post.pk, )))


class PostDeleteViewTest(BaseIntegrationTest):
    def test_view_ok(self):
        post = Post.objects.create(title="a_post_title", body="body")
        response = self.client.get(reverse("admin2:blog_post_delete",
                                           args=(post.pk, )))
        self.assertContains(response, post.title)

    def test_delete_post(self):
        post = Post.objects.create(title="a_post_title", body="body")
        response = self.client.post(reverse("admin2:blog_post_delete",
                                            args=(post.pk, )))
        self.assertRedirects(response, reverse("admin2:blog_post_index"))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())


class PostDeleteActionTest(BaseIntegrationTest):
    """
    Tests the behaviour of the 'Delete selected items' action.
    """
    def test_confirmation_page(self):
        p1 = Post.objects.create(title="A Post Title", body="body")
        p2 = Post.objects.create(title="A Post Title", body="body")
        post_data = {
            'action': 'delete_selected',
            'selected_model_pk': [p1.pk, p2.pk]
        }
        response = self.client.post(reverse("admin2:blog_post_index"),
                                    post_data)
        self.assertContains(response, p1.title)
        self.assertContains(response, p2.title)

    def test_results_page(self):
        p1 = Post.objects.create(title="A Post Title", body="body")
        p2 = Post.objects.create(title="A Post Title", body="body")
        post_data = {
            'action': 'delete_selected',
            'selected_model_pk': [p1.pk, p2.pk],
            'confirmed': 'yes'
        }
        response = self.client.post(reverse("admin2:blog_post_index"),
                                    post_data, follow=True)
        self.assertContains(response, "Successfully deleted 2 posts")


class TestAuthViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model()(username='user', is_staff=True,
                                     is_superuser=True)
        self.user.set_password("password")
        self.user.save()

    def test_login_required_redirect_to_index(self):
        index_path = reverse('admin2:dashboard') + '?next=/admin2/blog/post/'
        target_path = reverse('admin2:blog_post_index')
        self.assertRedirects(self.client.get(target_path), index_path)

    def test_login_required_logined_successful(self):
        index_path = reverse('admin2:dashboard')
        self.client.login(username=self.user.username,
                          password='password')
        self.assertContains(self.client.get(index_path),
                            reverse('admin2:blog_post_index'))

    def test_change_password_for_myself(self):
        self.client.login(username=self.user.username,
                          password='password')
        request = self.client.post(reverse('admin2:password_change',
                                           kwargs={'pk': self.user.pk}),
                                   {'old_password': 'password',
                                    'new_password1': 'user',
                                    'new_password2': 'user'})
        self.assertRedirects(request, reverse('admin2:password_change_done'))
        self.client.logout()

        self.assertFalse(self.client.login(username=self.user.username,
                                           password='password'))
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='user'))

    def test_change_password(self):
        self.client.login(username=self.user.username,
                          password='password')

        new_user = get_user_model()(username='new_user')
        new_user.set_password("new_user")
        new_user.save()

        request = self.client.post(reverse('admin2:password_change',
                                           kwargs={'pk': new_user.pk}),
                                   {'old_password': 'new_user',
                                    'password1': 'new_user_password',
                                    'password2': 'new_user_password'})
        self.assertRedirects(request, reverse('admin2:password_change_done'))
        self.client.logout()

        self.assertFalse(self.client.login(username=new_user.username,
                                           password='new_user'))
        self.assertTrue(self.client.login(username=new_user.username,
                                          password='new_user_password'))

    def test_logout(self):
        self.client.login(username=self.user.username,
                          password='password')
        logout_path = reverse('admin2:logout')
        request = self.client.get(logout_path)
        self.assertContains(request, 'Log in again')

        index_path = reverse('admin2:dashboard') + '?next=/admin2/blog/post/'
        target_path = reverse('admin2:blog_post_index')
        self.assertRedirects(self.client.get(target_path), index_path)
