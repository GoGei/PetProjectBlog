from django.test import TestCase

from ..models import TODOModel
from ..factories import TODOFactory


class TODOTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = TODOFactory.create()
        qs = TODOModel.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = TODOFactory.create()
        obj.delete()

        qs = TODOModel.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
