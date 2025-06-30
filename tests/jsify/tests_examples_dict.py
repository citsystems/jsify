import unittest
from jsify import (
    jsify, unjsify,
    jsified_items, jsified_keys, jsified_values,
    jsified_update, jsified_get, jsified_setdefault,
    jsified_pop, jsified_popitem, Undefined, Iterator
)


class TestJsifyDictDocs(unittest.TestCase):

    def setUp(self):
        self.d = {"a": 1, "b": {"c": 2}, "arr": [1, 2]}
        self.obj = jsify(self.d)

    def test_type_jsified(self):
        self.assertEqual(type(self.obj).__name__, 'Dict')
        self.assertEqual(type(self.obj.b).__name__, 'Dict')
        self.assertEqual(type(self.obj.arr).__name__, 'List')

    def test_dot_and_item_access(self):
        self.assertEqual(self.obj.a, 1)
        self.assertEqual(self.obj["a"], 1)
        self.assertEqual(self.obj.b.c, 2)
        self.assertEqual(self.obj["b"]["c"], 2)

    def test_nested_list_jsified(self):
        self.assertEqual(self.obj.arr[1], 2)
        self.assertEqual(type(self.obj.arr).__name__, 'List')

    def test_missing_keys(self):
        self.assertIs(self.obj.nope, Undefined)
        self.assertIs(self.obj["nope"], Undefined)

    def test_safe_chaining(self):
        self.assertIs(self.obj.nope.foo.bar, Undefined)

    def test_key_shadowing(self):
        o = jsify({'items': 123})
        self.assertEqual(o.items, 123)
        # There is no method o.items() if shadowed by key 'items'
        with self.assertRaises(TypeError):
            _ = o.items()

    def test_jsified_helpers(self):
        o = jsify({"x": 1, "y": 2})
        self.assertEqual(set(jsified_keys(o)), {"x", "y"})
        self.assertEqual(set(jsified_values(o)), {1, 2})
        self.assertEqual(set(tuple(pair) for pair in jsified_items(o)), {("x", 1), ("y", 2)})

        jsified_update(o, {"z": 3})
        self.assertEqual(o.z, 3)

        self.assertEqual(jsified_get(o, "x"), 1)
        jsified_pop(o, "x")
        self.assertIs(o.x, Undefined)

        jsified_setdefault(o, "w", 99)
        self.assertEqual(o.w, 99)

        # Popitem removes one item; remaining items should be only two now
        k, v = jsified_popitem(o)
        self.assertIn((k, v), [("y", 2), ("z", 3), ("w", 99)])
        keys_left = set(jsified_keys(o))
        self.assertEqual(len(keys_left), 2)

    def test_reference_behavior(self):
        orig = {"foo": {"bar": [1, 2]}}
        o = jsify(orig)
        o.foo.bar[0] = 42
        self.assertEqual(orig["foo"]["bar"][0], 42)
        o.foo.bar.append(99)
        self.assertIn(99, orig["foo"]["bar"])

    def test_unjsify_roundtrip(self):
        out = unjsify(self.obj)
        self.assertIsInstance(out, dict)
        self.assertEqual(out, self.d)

    def test_type_checks(self):
        self.assertNotIsInstance(self.obj, dict)
        self.assertNotEqual(type(self.obj), dict)
        self.assertIsInstance(unjsify(self.obj), dict)

    def test_iteration_returns_iterator(self):
        it = iter(self.obj)
        self.assertEqual(type(it).__name__, 'Iterator')

        keys = list(it)
        self.assertCountEqual(keys, self.d.keys())

    def test_iterated_values_access(self):
        it = iter(self.obj)
        keys = list(it)
        for k in keys:
            self.assertIn(k, self.obj)
            # Access value by key
            self.assertIsNot(self.obj[k], Undefined)


if __name__ == "__main__":
    unittest.main()
