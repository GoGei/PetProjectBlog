import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.Posts.models import Posts
from core.User.factories import SuperuserFactory
from core.Posts.factories import PostsFactory

from .test_posts_data import posts_data


class PostsViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.post = PostsFactory.create()

    def test_posts_list_get_success(self):
        response = self.client.get(reverse('posts-list', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)

    def test_posts_add_get_success(self):
        response = self.client.get(reverse('posts-add', host='admin'), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)

    def test_posts_add_post_success(self):
        Posts.objects.all().delete()
        data = posts_data.copy()
        response = self.client.post(reverse('posts-add', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Posts.objects.exists())

    def test_posts_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('posts-add', host='admin'), HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('posts-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_posts_edit_get_success(self):
        response = self.client.get(reverse('posts-edit', host='admin', args=[self.post.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)

    def test_posts_edit_post_success(self):
        data = posts_data.copy()
        response = self.client.post(reverse('posts-edit', host='admin', args=[self.post.id]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

    def test_posts_edit_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('posts-edit', host='admin', args=[self.post.id]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('posts-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_posts_view_get_200(self):
        response = self.client.post(reverse('posts-view', host='admin', args=[self.post.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)

    def test_posts_archive_success(self):
        response = self.client.post(reverse('posts-archive', host='admin', args=[self.post.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertTrue(self.post.archived_stamp)

    def test_posts_restore_success(self):
        response = self.client.post(reverse('posts-restore', host='admin', args=[self.post.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertFalse(self.post.archived_stamp)

    def test_posts_delete_success(self):
        response = self.client.post(reverse('posts-delete', host='admin', args=[self.post.id]), HTTP_HOST='admin')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Posts.objects.all().exists())
