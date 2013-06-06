from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone

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
        poll = Poll.objects.create(question="some question", pub_date=timezone.now())
        response = self.client.get(reverse("admin2:polls_poll_index"))
        self.assertContains(response, poll.question)

    def test_actions_displayed(self):
        response = self.client.get(reverse("admin2:polls_poll_index"))
        self.assertInHTML('<a tabindex="-1" href="#" data-name="action" data-value="DeleteSelectedAction">Delete selected items</a>', response.content)

    def test_delete_selected_poll(self):
        poll = Poll.objects.create(question="some question", pub_date=timezone.now())
        params = {'action': 'DeleteSelectedAction', 'selected_model_pk': str(poll.pk)}
        response = self.client.post(reverse("admin2:polls_poll_index"), params)
        self.assertInHTML('<p>Are you sure you want to delete the selected poll? All of the following items will be deleted:</p>', response.content)

    def test_delete_selected_poll_confirmation(self):
        poll = Poll.objects.create(question="some question", pub_date=timezone.now())
        params = {'action': 'DeleteSelectedAction', 'selected_model_pk': str(poll.pk), 'confirmed': 'yes'}
        response = self.client.post(reverse("admin2:polls_poll_index"), params)
        self.assertRedirects(response, reverse("admin2:polls_poll_index"))

    def test_delete_selected_poll_none_selected(self):
        Poll.objects.create(question="some question", pub_date=timezone.now())
        params = {'action': 'DeleteSelectedAction'}
        response = self.client.post(reverse("admin2:polls_poll_index"), params, follow=True)
        self.assertContains(response, "Items must be selected in order to perform actions on them. No items have been changed.")
