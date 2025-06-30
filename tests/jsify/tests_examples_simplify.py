import unittest
from jsify.simplify import SimplifiedObject, Undefined, loads_simplified, simplified_dumps, simplified_dump, load_simplified
from jsify.cjsify import jsify
import io


class TestSimplifiedObject(unittest.TestCase):

    def test_direct_creation(self):
        obj = SimplifiedObject(a=1, b=2, c={'x': 5})
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)
        self.assertEqual(obj.c['x'], 5)
        self.assertIs(obj.missing, Undefined)
        self.assertIsInstance(obj.c, dict)
        self.assertNotIsInstance(obj.c, SimplifiedObject)

    def test_loads_simplified_recursive(self):
        s = '{"user": {"profile": {}, "age": 25}}'  # profile is an empty dict now
        obj = loads_simplified(s)
        self.assertEqual(obj.user.age, 25)
        self.assertIsInstance(obj.user.profile, SimplifiedObject)
        self.assertIs(obj.user.profile.foo, Undefined)

    def test_deep_attribute_access(self):
        s = '{"a": {"b": {"c": 123}}}'
        obj = loads_simplified(s)
        self.assertEqual(obj.a.b.c, 123)
        self.assertIs(obj.a.b.missing, Undefined)
        self.assertIs(obj.a.b.missing.deep, Undefined)

    def test_falsy_and_comparison(self):
        obj = SimplifiedObject()
        self.assertFalse(obj.missing)
        self.assertTrue(obj.missing == None)
        self.assertIsNot(obj.missing, None)
        self.assertIs(obj.missing, Undefined)

    def test_serialization_dumps(self):
        obj = SimplifiedObject(a=1, b=None, c=Undefined)
        s = simplified_dumps(obj)
        self.assertIn('"a": 1', s)
        self.assertIn('"b": null', s)
        self.assertIn('"c": null', s)  # Undefined serializes as null

    def test_serialization_dump_and_load(self):
        obj = SimplifiedObject(x=10, y=Undefined)
        f = io.StringIO()
        simplified_dump(obj, f)  # Correct argument order: obj, file
        f.seek(0)
        loaded = load_simplified(f)
        self.assertEqual(loaded.x, 10)
        # Undefined serializes as null and deserializes back as None, not Undefined
        self.assertIsNone(loaded.y)

    def test_manual_nested_simplifiedobject(self):
        inner = SimplifiedObject(x=5)
        outer = SimplifiedObject(a=1, b=inner)
        self.assertEqual(outer.b.x, 5)
        obj = SimplifiedObject(items=[SimplifiedObject(x=1), SimplifiedObject(x=2)])
        self.assertEqual(obj.items[0].x, 1)

    def test_jsify_recursive_wrapping(self):
        d = {'user': {'name': 'Alice', 'age': 30}}
        obj = jsify(d)
        self.assertEqual(obj.user.name, 'Alice')
        self.assertEqual(obj.user.age, 30)
        self.assertTrue(hasattr(obj.user, 'name'))
        self.assertTrue(hasattr(obj.user, 'age'))

    def test_no_item_access_top_level(self):
        obj = SimplifiedObject(a=10)
        with self.assertRaises(TypeError):
            _ = obj['a']
        self.assertEqual(obj.a, 10)

    def test_undefined_import_and_check(self):
        from jsify.simplify import Undefined as Undef
        obj = SimplifiedObject()
        self.assertIs(obj.missing, Undef)
        self.assertTrue(obj.missing == None)
        self.assertFalse(obj.missing is None)


if __name__ == '__main__':
    unittest.main()
