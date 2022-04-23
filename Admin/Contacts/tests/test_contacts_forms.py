import json
from django.test import TestCase
from core.Contacts.models import Contacts
from core.Contacts.factories import ContactsFactory

from ..forms import ContactsForm, ContactsFilter
from .test_contacts_data import contacts_data, contacts_error_data, contacts_empty_data, \
    contacts_filter_form_data, related_data


class ContactsFormTestCase(TestCase):
    def setUp(self):
        self.form = ContactsForm

    def test_contacts_form_valid(self):
        data = contacts_data.copy()
        data.update({data['field_type']: related_data[data['field_type']]})

        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_contacts_form_invalid_errors(self):
        data = contacts_error_data.copy()
        data.pop('field_type')

        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_contacts_form_invalid_empty(self):
        data = contacts_empty_data.copy()
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class ContactsFilterTestCase(TestCase):
    def setUp(self):
        self.form = ContactsFilter
        self.contact = ContactsFactory.create()

    def test_contacts_filter_valid(self):
        data = contacts_filter_form_data.copy()
        data.update({data['field_type']: related_data[data['field_type']]})

        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_contacts_filter_obj_found(self):
        contact = self.contact
        data = {
            'search': contact.description[:10],
            contact.field_type: related_data[contact.field_type]
        }

        form = self.form(data, queryset=Contacts.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(contact, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(contact, form.qs)

    def test_contacts_filter_obj_not_found(self):
        contact = self.contact
        data = {
            'search': contact.description[:10:-1],
        }

        form = self.form(data, queryset=Contacts.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(contact, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertNotIn(contact, form.qs)

    def test_contacts_search_success(self):
        contact = self.contact
        search_to = [contact.description[:10],
                     contact.phone or contact.link or contact.email
                     ]
        for search in search_to:
            data = {'search': search}
            form = self.form(data, queryset=Contacts.objects.all())
            self.assertIn(contact, form.qs)
