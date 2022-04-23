from django.test import TestCase
from django_hosts import reverse
from django.utils import timezone

from core.User.factories import SuperuserFactory
from core.About.factories import AboutFactory
from core.Contacts.factories import ContactsFactory
from core.Posts.factories import PostsFactory


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.user = SuperuserFactory.create()

        self.post = PostsFactory.create(author=self.user)

        self.old_created_post = PostsFactory.create(author=self.user)
        self.old_created_post.created_stamp = timezone.localdate() - timezone.timedelta(days=30 * 6)
        self.old_created_post.save()

        self.old_modified_post = PostsFactory.create(author=self.user)
        self.old_modified_post.modified_stamp = timezone.localdate() - timezone.timedelta(days=30 * 6)
        self.old_modified_post.save()

        self.post_inactive = PostsFactory.create(author=self.user)
        self.post_inactive.archived_stamp = timezone.localdate()
        self.post_inactive.save()

    def test_posts_view_get_success(self):
        response = self.client.get(reverse('home-posts', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)
        self.assertContains(response, self.old_created_post)
        self.assertContains(response, self.old_modified_post)
        self.assertNotContains(response, self.post_inactive)

    def test_posts_view_recently_changed_get_success(self):
        response = self.client.get(reverse('home-recently-changed-posts', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)
        self.assertContains(response, self.old_created_post)
        self.assertContains(response, self.old_modified_post)
        self.assertNotContains(response, self.post_inactive)

    def test_posts_view_this_month_get_success(self):
        response = self.client.get(reverse('home-this-month-posts', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)
        self.assertNotContains(response, self.old_created_post)
        self.assertContains(response, self.old_modified_post)
        self.assertNotContains(response, self.post_inactive)

    def test_post_view_get_success(self):
        response = self.client.get(reverse('home-post-view', args=[self.post.slug], host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)

    def test_about_view_get_success(self):
        about = AboutFactory.create()
        about_inactive = AboutFactory.create()
        about_inactive.archived_stamp = timezone.now()
        about_inactive.save()

        contact = ContactsFactory.create()
        contact_inactive = ContactsFactory.create()
        contact_inactive.archived_stamp = timezone.now()
        contact_inactive.save()

        response = self.client.get(reverse('home-about', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, str(contact)[:35])
        self.assertNotContains(response, contact_inactive)

        self.assertContains(response, about)
        self.assertNotContains(response, about_inactive)

    def test_about_view_no_contacts_get_success(self):
        AboutFactory.create()
        response = self.client.get(reverse('home-about', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No "Contact" info added by superuser')

    def test_about_view_no_about_get_success(self):
        ContactsFactory.create()
        response = self.client.get(reverse('home-about', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No about info added yet')

    def test_about_view_empty_get_success(self):
        response = self.client.get(reverse('home-about', host='blog'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contacts and about info not added yet')
