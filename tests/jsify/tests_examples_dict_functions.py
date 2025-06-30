import unittest
from jsify import jsify, jsified_items, jsified_keys, jsified_values
from jsify import jsified_update, jsified_get, jsified_setdefault, jsified_pop, jsified_popitem

class TestJsifiedDictHelpers(unittest.TestCase):

    def setUp(self):
        # Reset for each test
        self.obj = jsify({"a": 1, "b": 2})

    def test_jsified_items(self):
        pairs = list(jsified_items(self.obj))
        self.assertIn(("a", 1), pairs)
        self.assertIn(("b", 2), pairs)
        self.assertIsInstance(jsified_items(self.obj), list)

    def test_jsified_keys(self):
        keys = list(jsified_keys(self.obj))
        self.assertCountEqual(keys, ["a", "b"])
        self.assertIsInstance(jsified_keys(self.obj), list)

    def test_jsified_values(self):
        values = list(jsified_values(self.obj))
        self.assertCountEqual(values, [1, 2])
        self.assertIsInstance(jsified_values(self.obj), list)

    def test_jsified_update(self):
        jsified_update(self.obj, {"c": 3})
        self.assertEqual(self.obj.c, 3)
        self.assertIn("c", list(jsified_keys(self.obj)))

    def test_jsified_get(self):
        self.assertEqual(jsified_get(self.obj, "a"), 1)
        self.assertEqual(jsified_get(self.obj, "z", default=123), 123)

    def test_jsified_setdefault(self):
        result = jsified_setdefault(self.obj, "q", 42)
        self.assertEqual(result, 42)
        self.assertEqual(self.obj.q, 42)
        # Second call returns value, not default
        result2 = jsified_setdefault(self.obj, "q", 99)
        self.assertEqual(result2, 42)

    def test_jsified_pop(self):
        self.obj.q = 77
        val = jsified_pop(self.obj, "q", default=None)
        self.assertEqual(val, 77)
        # Should now be gone
        self.assertNotIn("q", list(jsified_keys(self.obj)))
        # Popping missing with default
        val2 = jsified_pop(self.obj, "q", default=888)
        self.assertEqual(val2, 888)

    def test_jsified_popitem(self):
        # Prepare object with single item
        d = jsify({"x": 9})
        k, v = jsified_popitem(d)
        self.assertEqual((k, v), ("x", 9))
        # Now empty, should raise
        with self.assertRaises(KeyError):
            jsified_popitem(d)

if __name__ == "__main__":
    unittest.main()
