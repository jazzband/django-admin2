from os import path

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client
from django.utils.encoding import force_str

from ..models import CaptionedFile

fixture_dir = path.join(path.abspath(path.dirname(__file__)), 'fixtures')
fixture_file = path.join(fixture_dir, 'pubtest.txt')


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
        self.assertContains(
            response, reverse("admin2:files_captionedfile_index"))


class CaptionedFileListTest(BaseIntegrationTest):

    def test_view_ok(self):
        captioned_file = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        response = self.client.get(reverse("admin2:files_captionedfile_index"))
        self.assertContains(response, captioned_file.caption)

    def test_actions_displayed(self):
        response = self.client.get(reverse("admin2:files_captionedfile_index"))
        self.assertInHTML(
            '<a tabindex="-1" href="#" data-name="action" data-value="DeleteSelectedAction">Delete selected items</a>', force_str(response.content))

    def test_delete_selected_captioned_file(self):
        captioned_file = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        params = {'action': 'DeleteSelectedAction',
                  'selected_model_pk': str(captioned_file.pk)}
        response = self.client.post(
            reverse("admin2:files_captionedfile_index"), params)
        self.assertInHTML(
            '<p>Are you sure you want to delete the selected Captioned File? The following item will be deleted:</p>', force_str(response.content))

    def test_delete_selected_captioned_file_confirmation(self):
        captioned_file = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        params = {'action': 'DeleteSelectedAction', 'selected_model_pk': str(
            captioned_file.pk), 'confirmed': 'yes'}
        response = self.client.post(
            reverse("admin2:files_captionedfile_index"), params)
        self.assertRedirects(
            response, reverse("admin2:files_captionedfile_index"))

    def test_delete_selected_captioned_file_none_selected(self):
        CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        params = {'action': 'DeleteSelectedAction'}
        response = self.client.post(
            reverse("admin2:files_captionedfile_index"), params, follow=True)
        self.assertContains(
            response, "Items must be selected in order to perform actions on them. No items have been changed.")


class CaptionedFileDetailViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        captioned_file = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        response = self.client.get(
            reverse("admin2:files_captionedfile_detail", args=(captioned_file.pk, )))
        self.assertContains(response, captioned_file.caption)


class CaptionedFileCreateViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        response = self.client.get(
            reverse("admin2:files_captionedfile_create"))
        self.assertIn(
            'enctype="multipart/form-data"', force_str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_create_captioned_file(self):
        with open(fixture_file, 'rb') as fp:
            params = {
                "caption": "some file",
                "publication": fp,
            }
            response = self.client.post(reverse("admin2:files_captionedfile_create"),
                                        params,
                                        follow=True)
        self.assertTrue(
            CaptionedFile.objects.filter(caption="some file").exists())
        self.assertRedirects(
            response, reverse("admin2:files_captionedfile_index"))

    def test_save_and_add_another_redirects_to_create(self):
        """
        Tests that choosing 'Save and add another' from the model create
        page redirects the user to the model create page.
        """
        with open(fixture_file, 'rb') as fp:
            params = {
                "caption": "some file",
                "publication": fp,
                "_addanother": ""
            }
            response = self.client.post(reverse("admin2:files_captionedfile_create"),
                                        params)
        self.assertTrue(
            CaptionedFile.objects.filter(caption="some file").exists())
        self.assertRedirects(
            response, reverse("admin2:files_captionedfile_create"))

    def test_save_and_continue_editing_redirects_to_update(self):
        """
        Tests that choosing "Save and continue editing" redirects
        the user to the model update form.
        """
        with open(fixture_file, 'rb') as fp:
            params = {
                "caption": "some file",
                "publication": fp,
                "_continue": ""
            }
            response = self.client.post(reverse("admin2:files_captionedfile_create"),
                                        params)
        captioned_file = CaptionedFile.objects.get(caption="some file")
        self.assertRedirects(response, reverse("admin2:files_captionedfile_update",
                                               args=(captioned_file.pk, )))


class CaptionedFileDeleteViewTest(BaseIntegrationTest):

    def test_view_ok(self):
        captioned_file = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        response = self.client.get(reverse("admin2:files_captionedfile_delete",
                                           args=(captioned_file.pk, )))
        self.assertContains(response, captioned_file.caption)

    def test_delete_captioned_file(self):
        captioned_file = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        response = self.client.post(reverse("admin2:files_captionedfile_delete",
                                            args=(captioned_file.pk, )))
        self.assertRedirects(
            response, reverse("admin2:files_captionedfile_index"))
        self.assertFalse(
            CaptionedFile.objects.filter(pk=captioned_file.pk).exists())


class FileDeleteActionTest(BaseIntegrationTest):

    """
    Tests the behaviour of the 'Delete selected items' action.
    """

    def test_confirmation_page(self):
        cf1 = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        cf2 = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        params = {
            'action': 'DeleteSelectedAction',
            'selected_model_pk': [cf1.pk, cf2.pk]
        }
        response = self.client.post(reverse("admin2:files_captionedfile_index"),
                                    params)
        self.assertContains(response, cf1.caption)
        self.assertContains(response, cf2.caption)

    def test_results_page(self):
        cf1 = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        cf2 = CaptionedFile.objects.create(
            caption="some file", publication=fixture_file)
        params = {
            'action': 'DeleteSelectedAction',
            'selected_model_pk': [cf1.pk, cf2.pk],
            'confirmed': 'yes'
        }
        response = self.client.post(reverse("admin2:files_captionedfile_index"),
                                    params, follow=True)
        self.assertContains(response, "Successfully deleted 2 Captioned Files")
