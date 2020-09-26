from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_str

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


class UserListTest(BaseIntegrationTest):

    def test_search_users_m2m_group(self):
        # This test should cause the distinct search path to exectue
        group = Group.objects.create(name="Test Group")
        self.user.groups.add(group)

        params = {"q": "group"}
        response = self.client.get(reverse("admin2:auth_user_index"), params)
        self.assertContains(response, 'user')


class CommentListTest(BaseIntegrationTest):

    def test_search_comments(self):
        # Test search across Foriegn Keys
        post_1 = Post.objects.create(title="post_1_title", body="body")
        post_2 = Post.objects.create(title="post_2_title", body="another body")
        Comment.objects.create(body="comment_post_1_a", post=post_1)
        Comment.objects.create(body="comment_post_1_b", post=post_1)
        Comment.objects.create(body="comment_post_2", post=post_2)

        params = {"q": "post_1_title"}
        response = self.client.get(
            reverse("admin2:blog_comment_index"), params)
        self.assertContains(response, "comment_post_1_a")
        self.assertContains(response, "comment_post_1_b")
        self.assertNotContains(response, "comment_post_2")

    def test_list_selected_hides(self):
        post_1 = Post.objects.create(title="post_1_title", body="body")
        Comment.objects.create(body="comment_post1_body", post=post_1)
        response = self.client.get(reverse("admin2:blog_comment_index"))
        self.assertNotContains(response, "of 1 selected")


class PostListTest(BaseIntegrationTest):

    def _create_posts(self):
        Post.objects.bulk_create([
            Post(
                title="post_1_title",
                body="body",
                published_date=datetime(
                    month=7,
                    day=22,
                    year=2013
                )
            ),
            Post(
                title="post_2_title",
                body="body",
                published_date=datetime(
                    month=5,
                    day=20,
                    year=2012,
                )
            ),
            Post(
                title="post_3_title",
                body="body",
                published_date=datetime(
                    month=5,
                    day=30,
                    year=2012,
                ),
            ),
            Post(
                title="post_4_title",
                body="body",
                published_date=datetime(
                    month=6,
                    day=20,
                    year=2012,
                )
            ),
            Post(
                title="post_5_title",
                body="body",
                published_date=datetime(
                    month=6,
                    day=20,
                    year=2012,
                )
            ),
        ])

    def test_view_ok(self):
        post = Post.objects.create(title="A Post Title", body="body")
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertContains(response, post.title)

    def test_list_filter_presence(self):
        Post.objects.create(title="post_1_title", body="body")
        Post.objects.create(title="post_2_title", body="another body")
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertContains(response, 'id="list_filter_container"')

    def test_list_selected_shows(self):
        Post.objects.create(title="post_1_title", body="body")
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertContains(response, 'class="selected-count"')

    def test_actions_displayed(self):
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertInHTML(
            '<a tabindex="-1" href="#" data-name="action" data-value="DeleteSelectedAction">Delete selected items</a>', force_str(response.content))

    def test_actions_displayed_twice(self):
        # If actions_on_top and actions_on_bottom are both set
        response = self.client.get(reverse("admin2:blog_comment_index"))
        self.assertContains(response, '<div class="navbar actions-top">')
        self.assertContains(response, '<div class="navbar actions-bottom">')

    def test_delete_selected_post(self):
        post = Post.objects.create(title="A Post Title", body="body")
        params = {'action': 'DeleteSelectedAction',
                  'selected_model_pk': str(post.pk)}
        response = self.client.post(reverse("admin2:blog_post_index"), params)
        # caution : uses pluralization
        self.assertInHTML(
            '<p>Are you sure you want to delete the selected post? The following item will be deleted:</p>', force_str(response.content))

    def test_delete_selected_post_confirmation(self):
        post = Post.objects.create(title="A Post Title", body="body")
        params = {'action': 'DeleteSelectedAction',
                  'selected_model_pk': str(post.pk), 'confirmed': 'yes'}
        response = self.client.post(reverse("admin2:blog_post_index"), params)
        self.assertRedirects(response, reverse("admin2:blog_post_index"))

    def test_delete_selected_post_none_selected(self):
        Post.objects.create(title="A Post Title", body="body")
        params = {'action': 'DeleteSelectedAction'}
        response = self.client.post(
            reverse("admin2:blog_post_index"), params, follow=True)
        self.assertContains(
            response, "Items must be selected in order to perform actions on them. No items have been changed.")

    def test_search_posts(self):
        Post.objects.create(title="A Post Title", body="body")
        Post.objects.create(title="Another Post Title", body="body")
        Post.objects.create(
            title="Post With Keyword In Body", body="another post body")
        params = {"q": "another"}
        response = self.client.get(reverse("admin2:blog_post_index"), params)
        self.assertContains(response, "Another Post Title")
        self.assertContains(response, "Post With Keyword In Body")
        self.assertNotContains(response, "A Post Title")

    def test_renderer_title(self):
        Post.objects.create(
            title='a lowercase title', body='body', published=False)
        response = self.client.get(reverse('admin2:blog_post_index'))
        self.assertContains(response, 'A Lowercase Title')

    def test_renderer_body(self):
        Post.objects.create(
            title='title', body='a lowercase body', published=False)
        response = self.client.get(reverse('admin2:blog_post_index'))
        self.assertContains(response, 'a lowercase body')

    def test_renderer_unpublished(self):
        Post.objects.create(title='title', body='body', published=False)
        response = self.client.get(reverse('admin2:blog_post_index'))
        self.assertContains(response, 'fa fa-minus')

    def test_renderer_published(self):
        Post.objects.create(title='title', body='body', published=True)
        response = self.client.get(reverse('admin2:blog_post_index'))
        self.assertContains(response, 'fa fa-check')

    def test_drilldowns(self):
        self._create_posts()

        response = self.client.get(reverse('admin2:blog_post_index'))
        self.assertContains(response, '<a href="?year=2012">2012</a>')
        self.assertContains(response, "<tr>", 5)

        response = self.client.get(
            "%s?%s" % (
                reverse('admin2:blog_post_index'),
                "year=2012",
            )
        )

        self.assertContains(
            response,
            '<a href="?year=2012&month=05">May 2012</a>',
        )
        self.assertContains(
            response,
            'All dates',
        )
        self.assertContains(response, "<tr>", 4)

        response = self.client.get(
            "%s?%s" % (
                reverse('admin2:blog_post_index'),
                "year=2012&month=5",
            )
        )

        self.assertContains(response, "<tr>", 2)
        self.assertContains(
            response,
            '<a href="?year=2012&month=05&day=20">May 20</a>',
        )
        self.assertContains(response, '<a href="?year=2012">')

        response = self.client.get(
            "%s?%s" % (
                reverse('admin2:blog_post_index'),
                "year=2012&month=05&day=20",
            )
        )

        self.assertContains(response, "<tr>", 1)
        self.assertContains(
            response,
            '<a href="?year=2012&month=05&day=20">May 20</a>',
        )
        self.assertContains(
            response,
            '<li class="active">'
        )
        self.assertContains(
            response,
            'May 2012'
        )

    def test_ordering(self):
        self._create_posts()

        response = self.client.get(reverse("admin2:blog_post_index"))

        model_admin = response.context["view"].model_admin
        response_queryset = response.context["object_list"]
        manual_queryset = Post.objects.order_by("-published_date", "title")

        zipped_queryset = zip(
            list(response_queryset),
            list(manual_queryset),
        )

        self.assertTrue(all([
            model1.pk == model2.pk
            for model1, model2 in zipped_queryset
        ]))

        self.assertEqual(
            model_admin.get_ordering(response.request),
            model_admin.ordering,
        )

    def test_all_unselected_action(self):
        self._create_posts()

        response = self.client.get(reverse("admin2:blog_post_index"))

        self.assertTrue(all([
            not post.published
            for post in response.context["object_list"]
        ]))

        response = self.client.post(
            reverse("admin2:blog_post_index"),
            {
                'action': 'PublishAllItemsAction',
            },
            follow=True
        )

        self.assertTrue(all([
            post.published
            for post in response.context["object_list"]
        ]))

        # Test function-based view
        response = self.client.post(
            reverse("admin2:blog_post_index"),
            {
                'action': 'PublishAllItemsAction',
            },
            follow=True,
        )

        self.assertTrue(all([
            post.published
            for post in response.context["object_list"]
        ]))


class PostListTestCustomAction(BaseIntegrationTest):

    def test_publish_action_displayed_in_list(self):
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertInHTML(
            '<a tabindex="-1" href="#" data-name="action" data-value="CustomPublishAction">Publish selected items</a>', force_str(response.content))

    def test_publish_selected_items(self):
        post = Post.objects.create(title="A Post Title",
                                   body="body",
                                   published=False)
        self.assertEqual(Post.objects.filter(published=True).count(), 0)

        params = {'action': 'CustomPublishAction',
                  'selected_model_pk': str(post.pk),
                  'confirmed': 'yes'}
        response = self.client.post(reverse("admin2:blog_post_index"), params)
        self.assertRedirects(response, reverse("admin2:blog_post_index"))

        self.assertEqual(Post.objects.filter(published=True).count(), 1)

    def test_unpublish_action_displayed_in_list(self):
        response = self.client.get(reverse("admin2:blog_post_index"))
        self.assertInHTML(
            '<a tabindex="-1" href="#" data-name="action" data-value="unpublish_items">Unpublish selected items</a>', force_str(response.content))

    def test_unpublish_selected_items(self):
        post = Post.objects.create(title="A Post Title",
                                   body="body",
                                   published=True)
        self.assertEqual(Post.objects.filter(published=True).count(), 1)

        params = {'action': 'unpublish_items',
                  'selected_model_pk': str(post.pk)}
        response = self.client.post(reverse("admin2:blog_post_index"), params)
        self.assertRedirects(response, reverse("admin2:blog_post_index"))

        self.assertEqual(Post.objects.filter(published=True).count(), 0)


class PostDetailViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        post = Post.objects.create(title="A Post Title", body="body")
        response = self.client.get(reverse("admin2:blog_post_detail",
                                           args=(post.pk, )))
        self.assertContains(response, post.title)


class PostCreateViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        response = self.client.get(reverse("admin2:blog_post_create"))
        self.assertNotIn(
            '''enctype="multipart/form-data"''', force_str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        # Generated by inspecting the request with the pdb debugger
        post_data = {
            "comments-TOTAL_FORMS": u'2',
            "comments-INITIAL_FORMS": u'0',
            "comments-MAX_NUM_FORMS": u'',
            "comments-0-body": u'Comment Body',
            'comments-0-post': '',
            'comments-0-id': '',
            "title": "A Post Title",
            "body": "a_post_body",
        }

        response = self.client.post(reverse("admin2:blog_post_create"),
                                    post_data,
                                    follow=True)
        self.assertTrue(Post.objects.filter(title="A Post Title").exists())
        Comment.objects.get(body="Comment Body")
        self.assertRedirects(response, reverse("admin2:blog_post_index"))

    def test_save_and_add_another_redirects_to_create(self):
        """
        Tests that choosing 'Save and add another' from the model create
        page redirects the user to the model create page.
        """
        post_data = {
            "comments-TOTAL_FORMS": u'2',
            "comments-INITIAL_FORMS": u'0',
            "comments-MAX_NUM_FORMS": u'',
            "comments-0-body": u'Comment Body',
            'comments-0-post': '',
            'comments-0-id': '',
            "title": "A Post Title",
            "body": "a_post_body",
            "_addanother": ""
        }
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse("admin2:blog_post_create"),
                                    post_data)
        Post.objects.get(title='A Post Title')
        self.assertRedirects(response, reverse("admin2:blog_post_create"))

    def test_save_and_continue_editing_redirects_to_update(self):
        """
        Tests that choosing "Save and continue editing" redirects
        the user to the model update form.
        """
        post_data = {
            "comments-TOTAL_FORMS": u'2',
            "comments-INITIAL_FORMS": u'0',
            "comments-MAX_NUM_FORMS": u'',
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
        post = Post.objects.create(title="A Post Title", body="body")
        response = self.client.get(reverse("admin2:blog_post_delete",
                                           args=(post.pk, )))
        self.assertContains(response, post.title)

    def test_delete_post(self):
        post = Post.objects.create(title="A Post Title", body="body")
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
            'action': 'DeleteSelectedAction',
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
            'action': 'DeleteSelectedAction',
            'selected_model_pk': [p1.pk, p2.pk],
            'confirmed': 'yes'
        }
        response = self.client.post(reverse("admin2:blog_post_index"),
                                    post_data, follow=True)
        self.assertContains(response, "Successfully deleted 2 post")


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
                                    'new_password1': 'new_password',
                                    'new_password2': 'new_password'})
        self.assertRedirects(request, reverse('admin2:password_change_done'))
        self.client.logout()

        self.assertFalse(self.client.login(username=self.user.username,
                                           password='password'))
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='new_password'))

    def test_change_password(self):
        self.client.login(username=self.user.username,
                          password='password')

        new_user = get_user_model()(username='new_user')
        new_user.set_password("new_user")
        new_user.save()

        request = self.client.post(reverse('admin2:password_change',
                                           kwargs={'pk': new_user.pk}),
                                   {'password1': 'new_user_password',
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
