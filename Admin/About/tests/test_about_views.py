import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.About.models import About
from core.User.factories import SuperuserFactory
from core.About.factories import AboutFactory

from .test_about_data import about_data


class AboutViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.about = AboutFactory.create()

    def test_about_list_get_success(self):
        response = self.client.get(reverse('about-list', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.about)

    def test_about_add_get_success(self):
        response = self.client.get(reverse('about-add', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)

    def test_about_add_post_success(self):
        About.objects.all().delete()
        data = about_data.copy()
        response = self.client.post(reverse('about-add', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(About.objects.exists())

    def test_about_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('about-add', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('about-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_about_edit_get_success(self):
        response = self.client.get(reverse('about-edit', host='admin', args=[self.about.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.about)

    def test_about_edit_post_success(self):
        data = about_data.copy()
        response = self.client.post(reverse('about-edit', host='admin', args=[self.about.id]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

    def test_about_edit_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('about-edit', host='admin', args=[self.about.id]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('about-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_about_view_get_200(self):
        response = self.client.post(reverse('about-view', host='admin', args=[self.about.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.about)

    def test_about_archive_success(self):
        response = self.client.post(reverse('about-archive', host='admin', args=[self.about.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.about.refresh_from_db()
        self.assertTrue(self.about.archived_stamp)

    def test_about_restore_success(self):
        response = self.client.post(reverse('about-restore', host='admin', args=[self.about.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.about.refresh_from_db()
        self.assertFalse(self.about.archived_stamp)

    def test_about_delete_success(self):
        response = self.client.post(reverse('about-delete', host='admin', args=[self.about.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(About.objects.all().exists())
