from django.test import TestCase
from ..fieldsets import Fieldsets, Fieldset


class FieldsetsTest(TestCase):
    def test_contains(self):
        fieldsets = Fieldsets()
        self.assertFalse('name' in fieldsets)

        fieldsets = Fieldsets(Fieldset())
        self.assertFalse('name' in fieldsets)

        fieldsets = Fieldsets(Fieldset('not_name'))
        self.assertFalse('name' in fieldsets)

        fieldsets = Fieldsets(Fieldset('name'))
        self.assertTrue('name' in fieldsets)

        fieldsets = Fieldsets(Fieldset('not_name', 'name'))
        self.assertTrue('name' in fieldsets)

    def test_empty(self):
        fieldsets = Fieldsets()
        self.assertFalse(fieldsets)

        fieldsets = Fieldsets(Fieldset())
        self.assertTrue(fieldsets)

    def test_indexing(self):
        fs = Fieldsets()
        self.assertEqual(len(fs), 0)

        foo = Fieldset('foo')
        bar = Fieldset('bar')
        spam = Fieldset('spam')
        eggs = Fieldset('eggs')
        fs = Fieldsets(foo, bar, spam, eggs)
        self.assertEqual(len(fs), 4)
        self.assertEqual(fs[0], foo)
        self.assertEqual(fs[1], bar)
        self.assertEqual(fs[2], spam)
        self.assertEqual(fs[3], eggs)
        self.assertEqual(fs[-1], eggs)

    def test_slicing(self):
        foo = Fieldset('foo')
        bar = Fieldset('bar')
        spam = Fieldset('spam')
        eggs = Fieldset('eggs')
        fs = Fieldsets(foo, bar, spam, eggs)

        self.assertEqual(fs[0:2], [foo, bar])
        self.assertEqual(fs[::-2], [eggs, bar])

    def test_append(self):
        fs = Fieldsets()
        foo = Fieldset('foo')
        bar = Fieldset('bar')
        fs.append(foo)
        fs.append(bar)
        self.assertEqual(fs.fields, ['foo', 'bar'])

    def test_copy(self):
        foo = Fieldset('foo')
        bar = Fieldset('bar')
        f1 = Fieldsets(foo, bar)
        f2 = f1.copy()
        self.assertEqual(f1, f2)
        self.assertFalse(f1 is f2)

        f2 = f2.remove_fieldset(0)
        self.assertNotEqual(f1, f2)
        self.assertFalse(f1 is f2)

    def test_remove_fieldset(self):
        foo = Fieldset('foo', id='foo1')
        bar = Fieldset('bar', id='foo2')
        fs = Fieldsets(foo, bar)
        fs.remove_fieldset('foo1')
        self.assertEqual(fs.fields, ['foo', 'bar'])

        fs = fs.remove_fieldset('foo1')
        self.assertEqual(fs.fields, ['bar'])

        self.assertRaises(ValueError, fs.remove_fieldset, 'foo1')


class FieldsetTest(TestCase):
    def test_id(self):
        f = Fieldset(id='my_id')
        self.assertEqual(f.id, 'my_id')

    def test_name(self):
        f = Fieldset(name='A beautiful, descriptive name')
        self.assertEqual(f.name, 'A beautiful, descriptive name')

    def test_contains(self):
        fieldset = Fieldset()
        self.assertFalse('name' in fieldset)

        fieldset = Fieldset('not_name')
        self.assertFalse('name' in fieldset)

        fieldset = Fieldset('name')
        self.assertTrue('name' in fieldset)

        fieldset = Fieldset('not_name', 'name')
        self.assertTrue('name' in fieldset)

    def test_empty(self):
        fieldset = Fieldset()
        self.assertFalse(fieldset)

        fieldset = Fieldset('field_one')
        self.assertTrue(fieldset)

    def test_index(self):
        f = Fieldset('foo', 'bar')
        self.assertEqual(f.index('foo'), 0)
        self.assertEqual(f.index('bar'), 1)
        self.assertRaises(ValueError, f.index, None)
        self.assertRaises(ValueError, f.index, 'non_existent')

    def test_copy(self):
        f1 = Fieldset('foo', 'bar')
        f2 = f1.copy()
        self.assertEqual(f1, f2)
        self.assertFalse(f1 is f2)

        f1.move_field('bar', after='foo')
        self.assertNotEqual(f1, f2)

    def test_add_field_before(self):
        f1 = Fieldset('foo', 'bar')
        f1 = f1.add_field('spam', before='bar')
        self.assertEqual(f1.fields, ['foo', 'spam', 'bar'])
        f1 = f1.add_field('eggs', before='foo')
        self.assertEqual(f1.fields, ['eggs', 'foo', 'spam', 'bar'])

    def test_add_field_after(self):
        f1 = Fieldset('foo', 'bar')
        f1 = f1.add_field('spam', after='foo')
        self.assertEqual(f1.fields, ['foo', 'spam', 'bar'])
        f1 = f1.add_field('eggs', after='bar')
        self.assertEqual(f1.fields, ['foo', 'spam', 'bar', 'eggs'])

    def test_move_field_errors(self):
        f1 = Fieldset('foo', 'bar')

        self.assertRaises(ValueError, f1.move_field, 'foo', after='bar', before='bar')
        self.assertRaises(ValueError, f1.move_field, 'foo', 'bar', 'bar')

    def test_move_field_before(self):
        f1 = Fieldset('foo', 'bar', 'spam', 'eggs')
        f1 = f1.move_field('foo', before='eggs')
        self.assertEqual(f1.fields, ['bar', 'spam', 'foo', 'eggs'])

        f1 = f1.move_field('spam', before='bar')
        self.assertEqual(f1.fields, ['spam', 'bar', 'foo', 'eggs'])

    def test_move_field_after(self):
        f1 = Fieldset('foo', 'bar', 'spam', 'eggs')
        f1 = f1.move_field('foo', after='bar')
        self.assertEqual(f1.fields, ['bar', 'foo', 'spam', 'eggs'])

        f1 = f1.move_field('foo', after='eggs')
        self.assertEqual(f1.fields, ['bar', 'spam', 'eggs', 'foo'])

    def test_remove_field(self):
        f1 = Fieldset('foo', 'bar', 'spam', 'eggs')
        f1 = f1.remove_field('foo')
        self.assertEqual(f1.fields, ['bar', 'spam', 'eggs'])
        self.assertRaises(ValueError, f1.remove_field, 'foo')
