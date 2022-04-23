from django.test import TestCase

from ..models import About
from ..factories import AboutFactory


class AboutTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = AboutFactory.create()
        qs = About.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = AboutFactory.create()
        obj.delete()

        qs = About.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
