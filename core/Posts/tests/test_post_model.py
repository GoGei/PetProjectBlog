from django.test import TestCase

from ..models import Posts
from ..factories import PostsFactory


class PostsTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = PostsFactory.create()
        qs = Posts.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = PostsFactory.create()
        obj.delete()

        qs = Posts.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
