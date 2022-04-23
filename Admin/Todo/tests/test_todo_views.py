import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.TODO.models import TODOModel
from core.User.factories import SuperuserFactory
from core.TODO.factories import TODOFactory

from .test_todo_data import todo_data


class TODOModelViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.todo = TODOFactory.create()

        data = todo_data.copy()
        self.todo_data = data

    def test_todo_list_get_success(self):
        response = self.client.get(reverse('todo-list', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo)

    def test_todo_add_get_success(self):
        response = self.client.get(reverse('todo-add', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)

    def test_todo_add_post_success(self):
        TODOModel.objects.all().delete()
        response = self.client.post(reverse('todo-add', host='admin'), HTTP_HOST='admin', data=self.todo_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TODOModel.objects.exists())

    def test_todo_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('todo-add', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('todo-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_todo_edit_get_success(self):
        response = self.client.get(reverse('todo-edit', host='admin', args=[self.todo.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo)

    def test_todo_edit_post_success(self):
        response = self.client.post(reverse('todo-edit', host='admin', args=[self.todo.id]),
                                    HTTP_HOST='admin', data=self.todo_data)
        self.assertEqual(response.status_code, 302)

    def test_todo_edit_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('todo-edit', host='admin', args=[self.todo.id]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('todo-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_todo_view_get_200(self):
        response = self.client.post(reverse('todo-view', host='admin', args=[self.todo.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo)

    def test_todo_archive_success(self):
        response = self.client.post(reverse('todo-archive', host='admin', args=[self.todo.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.archived_stamp)

    def test_todo_restore_success(self):
        response = self.client.post(reverse('todo-restore', host='admin', args=[self.todo.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.archived_stamp)

    def test_todo_clear_success(self):
        self.todo.archive()
        response = self.client.post(reverse('todo-clear', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TODOModel.objects.all().exists())
