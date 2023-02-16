from django.test import TestCase
from mptt.models import TreeForeignKey
from tree.models import TreeNode


class TreeNodeTestCase(TestCase):
    def setUp(self):
        self.a = TreeNode.objects.create(name='A')
        self.b = TreeNode.objects.create(name='B', parent=self.a)
        self.c = TreeNode.objects.create(name='C', parent=self.a)
        self.d = TreeNode.objects.create(name='D', parent=self.b)
        self.e = TreeNode.objects.create(name='E', parent=self.b)

    def test_tree_structure(self):
        self.assertEqual(self.a.get_descendant_count(), 4)
        self.assertEqual(self.b.get_descendant_count(), 2)
        self.assertEqual(self.c.get_descendant_count(), 0)
        self.assertEqual(self.d.get_descendant_count(), 0)
        self.assertEqual(self.e.get_descendant_count(), 0)
        self.assertEqual(self.a.children.count(), 2)
        self.assertEqual(self.b.children.count(), 2)
        self.assertIsNone(self.a.parent)
        self.assertEqual(self.b.parent, self.a)
        self.assertEqual(self.c.parent, self.a)
        self.assertEqual(self.d.parent, self.b)
        self.assertEqual(self.e.parent, self.b)

    def test_model_fields(self):
        self.assertIsInstance(TreeNode._meta.get_field('parent'), TreeForeignKey)
        self.assertEqual(TreeNode._meta.get_field('parent').null, True)
        self.assertEqual(TreeNode._meta.get_field('parent').blank, True)
