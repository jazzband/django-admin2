from os import path

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from files.models import CaptionedFile


fixture_dir = path.join(path.abspath(path.dirname(__file__)), 'fixtures')


class CaptionedFileTestCase(TestCase):

    def setUp(self):
        self.captioned_file = CaptionedFile.objects.create(
            caption="this is a file",
            publication=path.join('pubtest.txt')
        )
        self.captioned_file.save()

    def test_creation(self):
        cf = CaptionedFile.objects.create(
            caption="lo lo",
            publication=path.join('pubtest.txt')
        )
        cf.save()
        self.assertEqual(CaptionedFile.objects.count(), 2)
        # Cause setup created one already

    def test_update(self):
        self.captioned_file.caption = "I like text files"
        self.captioned_file.save()

        cf = CaptionedFile.objects.get()
        self.assertEqual(cf.caption, "I like text files")

    def test_delete(self):
        cf = CaptionedFile.objects.get()
        cf.delete()

        self.assertEqual(CaptionedFile.objects.count(), 0)


class MultiEncodedAdminFormTest(TestCase):
    def setUp(self):
        self.user = User(
            username='admin',
            is_staff=True,
            is_superuser=True)
        self.user.set_password('admin')
        self.user.save()
        self.create_url = reverse('admin2:example3_captioned_file_create')
