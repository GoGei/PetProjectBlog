import uuid

from django.test import TestCase
from django_hosts import reverse

from core.User.factories import SuperuserFactory


class AboutViewTestCase(TestCase):
    def setUp(self):
        self.password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(self.password)
        self.user.save()

        self.data = {
            'email': self.user.email,
            'password': self.password
        }

    def test_login_get_success(self):
        response = self.client.get(reverse('admin-login', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('admin-login', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('admin-index', host='admin'))

    def test_login_post_password_not_success(self):
        data = self.data.copy()
        data['password'] = 'password'

        response = self.client.post(reverse('admin-login', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct email and password')

    def test_login_post_user_is_not_staff_and_superuser(self):
        data = self.data.copy()
        self.user.is_staff = False
        self.user.save()

        response = self.client.post(reverse('admin-login', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 200)

    def test_login_post_user_is_not_staff_and_not_superuser(self):
        data = self.data.copy()
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        response = self.client.post(reverse('admin-login', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User is not staff')

    def test_login_post_user_is_not_active(self):
        data = self.data.copy()
        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse('admin-login', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct email and password')
