from django.test import TestCase

from ..models import Contacts
from ..factories import ContactsFactory


class ContactsTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = ContactsFactory.create()
        qs = Contacts.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = ContactsFactory.create()
        obj.delete()

        qs = Contacts.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
