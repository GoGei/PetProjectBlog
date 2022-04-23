import uuid
import json
from django.test import TestCase
from core.User.factories import UserFactory

from ..forms import LoginForm


class LoginFormTestCase(TestCase):
    def setUp(self):
        self.form = LoginForm
        self.user = UserFactory.create()
        self.data = {
            'email': self.user.email,
            'password': uuid.uuid4()
        }

    def test_login_form_valid(self):
        form = self.form(self.data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_email(self):
        data = self.data.copy()
        data['email'] = 'unknown.email@email.com'
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        self.assertIn('email', errors)
