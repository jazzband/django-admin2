from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text

from ..models import Poll


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
        self.assertContains(response, reverse("admin2:polls_poll_index"))


class PollListTest(BaseIntegrationTest):

    def test_view_ok(self):
        poll = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        response = self.client.get(reverse("admin2:polls_poll_index"))
        self.assertContains(response, poll.question)

    def test_actions_displayed(self):
        response = self.client.get(reverse("admin2:polls_poll_index"))
        self.assertInHTML(
            '<a tabindex="-1" href="#" data-name="action" data-value="DeleteSelectedAction">Delete selected items</a>', force_text(response.content))

    def test_delete_selected_poll(self):
        poll = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        params = {'action': 'DeleteSelectedAction',
                  'selected_model_pk': str(poll.pk)}
        response = self.client.post(reverse("admin2:polls_poll_index"), params)
        self.assertInHTML(
            '<p>Are you sure you want to delete the selected poll? The following item will be deleted:</p>', force_text(response.content))

    def test_delete_selected_poll_confirmation(self):
        poll = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        params = {'action': 'DeleteSelectedAction',
                  'selected_model_pk': str(poll.pk), 'confirmed': 'yes'}
        response = self.client.post(reverse("admin2:polls_poll_index"), params)
        self.assertRedirects(response, reverse("admin2:polls_poll_index"))

    def test_delete_selected_poll_none_selected(self):
        Poll.objects.create(question="some question", pub_date=timezone.now())
        params = {'action': 'DeleteSelectedAction'}
        response = self.client.post(
            reverse("admin2:polls_poll_index"), params, follow=True)
        self.assertContains(
            response, "Items must be selected in order to perform actions on them. No items have been changed.")


class PollDetailViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        poll = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        response = self.client.get(
            reverse("admin2:polls_poll_detail", args=(poll.pk, )))
        self.assertContains(response, poll.question)


class PollCreateViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        response = self.client.get(reverse("admin2:polls_poll_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_poll(self):
        params = {
            "question": "some question",
            "pub_date": "2012-01-01",
            "choice_set-TOTAL_FORMS": u'0',
            "choice_set-INITIAL_FORMS": u'0',
            "choice_set-MAX_NUM_FORMS": u'',
        }
        response = self.client.post(reverse("admin2:polls_poll_create"),
                                    params,
                                    follow=True)
        self.assertTrue(Poll.objects.filter(question="some question").exists())
        self.assertRedirects(response, reverse("admin2:polls_poll_index"))

    def test_save_and_add_another_redirects_to_create(self):
        """
        Tests that choosing 'Save and add another' from the model create
        page redirects the user to the model create page.
        """
        params = {
            "question": "some question",
            "pub_date": "2012-01-01",
            "choice_set-TOTAL_FORMS": u'0',
            "choice_set-INITIAL_FORMS": u'0',
            "choice_set-MAX_NUM_FORMS": u'',
            "_addanother": ""
        }
        response = self.client.post(reverse("admin2:polls_poll_create"),
                                    params)
        self.assertTrue(Poll.objects.filter(question="some question").exists())
        self.assertRedirects(response, reverse("admin2:polls_poll_create"))

    def test_save_and_continue_editing_redirects_to_update(self):
        """
        Tests that choosing "Save and continue editing" redirects
        the user to the model update form.
        """
        params = {
            "question": "some question",
            "pub_date": "2012-01-01",
            "choice_set-TOTAL_FORMS": u'0',
            "choice_set-INITIAL_FORMS": u'0',
            "choice_set-MAX_NUM_FORMS": u'',
            "_continue": ""
        }
        response = self.client.post(reverse("admin2:polls_poll_create"),
                                    params)
        poll = Poll.objects.get(question="some question")
        self.assertRedirects(response, reverse("admin2:polls_poll_update",
                                               args=(poll.pk, )))


class PollDeleteViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        poll = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        response = self.client.get(reverse("admin2:polls_poll_delete",
                                           args=(poll.pk, )))
        self.assertContains(response, poll.question)

    def test_delete_poll(self):
        poll = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        response = self.client.post(reverse("admin2:polls_poll_delete",
                                            args=(poll.pk, )))
        self.assertRedirects(response, reverse("admin2:polls_poll_index"))
        self.assertFalse(Poll.objects.filter(pk=poll.pk).exists())


class PollDeleteActionTest(BaseIntegrationTest):

    """
    Tests the behaviour of the 'Delete selected items' action.
    """

    def test_confirmation_page(self):
        p1 = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        p2 = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        params = {
            'action': 'DeleteSelectedAction',
            'selected_model_pk': [p1.pk, p2.pk]
        }
        response = self.client.post(reverse("admin2:polls_poll_index"),
                                    params)
        self.assertContains(response, p1.question)
        self.assertContains(response, p2.question)

    def test_results_page(self):
        p1 = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        p2 = Poll.objects.create(
            question="some question", pub_date=timezone.now())
        params = {
            'action': 'DeleteSelectedAction',
            'selected_model_pk': [p1.pk, p2.pk],
            'confirmed': 'yes'
        }
        response = self.client.post(reverse("admin2:polls_poll_index"),
                                    params, follow=True)
        self.assertContains(response, "Successfully deleted 2 polls")
