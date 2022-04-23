import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.Contacts.models import Contacts
from core.User.factories import SuperuserFactory
from core.Contacts.factories import ContactsFactory

from .test_contacts_data import contacts_data, related_data


class ContactsViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.contacts = ContactsFactory.create()

        data = contacts_data.copy()
        data.update({data['field_type']: related_data[data['field_type']]})
        self.contact_data = data

    def test_contacts_list_get_success(self):
        response = self.client.get(reverse('contacts-list', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contacts)

    def test_contacts_add_get_success(self):
        response = self.client.get(reverse('contacts-add', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)

    def test_contacts_add_post_success(self):
        Contacts.objects.all().delete()
        response = self.client.post(reverse('contacts-add', host='admin'), HTTP_HOST='admin', data=self.contact_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contacts.objects.exists())

    def test_contacts_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('contacts-add', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('contacts-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_contacts_edit_get_success(self):
        response = self.client.get(reverse('contacts-edit', host='admin', args=[self.contacts.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contacts)

    def test_contacts_edit_post_success(self):
        response = self.client.post(reverse('contacts-edit', host='admin', args=[self.contacts.id]),
                                    HTTP_HOST='admin', data=self.contact_data)
        self.assertEqual(response.status_code, 302)

    def test_contacts_edit_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('contacts-edit', host='admin', args=[self.contacts.id]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('contacts-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_contacts_view_get_200(self):
        response = self.client.post(reverse('contacts-view', host='admin', args=[self.contacts.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contacts)

    def test_contacts_archive_success(self):
        response = self.client.post(reverse('contacts-archive', host='admin', args=[self.contacts.id]),
                                    HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.contacts.refresh_from_db()
        self.assertTrue(self.contacts.archived_stamp)

    def test_contacts_restore_success(self):
        response = self.client.post(reverse('contacts-restore', host='admin', args=[self.contacts.id]),
                                    HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.contacts.refresh_from_db()
        self.assertFalse(self.contacts.archived_stamp)

    def test_contacts_delete_success(self):
        response = self.client.post(reverse('contacts-delete', host='admin', args=[self.contacts.id]),
                                    HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contacts.objects.all().exists())
