import json
import datetime
from django.test import TestCase
from core.About.models import About
from core.About.factories import AboutFactory

from ..forms import AboutForm, AboutFilter
from .test_about_data import about_data, about_error_data, about_empty_data, \
    about_filter_form_data


class AboutFormTestCase(TestCase):
    def setUp(self):
        self.form = AboutForm

    def test_about_form_valid(self):
        data = about_data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_about_form_invalid_errors(self):
        data = about_error_data.copy()
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_about_form_invalid_empty(self):
        data = about_empty_data.copy()
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class AboutFilterTestCase(TestCase):
    def setUp(self):
        self.form = AboutFilter

    def test_about_filter_valid(self):
        data = about_filter_form_data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_about_filter_obj_found(self):
        about = AboutFactory.create()
        data = {
            'search': about.title[:10],
            'from_date': about.from_date - datetime.timedelta(days=2),
            'to_date': about.to_date + datetime.timedelta(days=2),
        }
        form = self.form(data, queryset=About.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(about, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(about, form.qs)

    def test_about_filter_obj_not_found(self):
        about = AboutFactory.create()
        data = {
            'search': about.title[:10:-1],
            'from_date': about.from_date + datetime.timedelta(days=2),
            'to_date': about.to_date - datetime.timedelta(days=2),
        }
        form = self.form(data, queryset=About.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(about, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertNotIn(about, form.qs)
