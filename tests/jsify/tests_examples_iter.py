import unittest
from jsify import jsify, Undefined
from jsify.cjsify import Iterator as JsifyIterator

class TestJsifiedIterator(unittest.TestCase):
    def test_jsified_iterator_type(self):
        it = iter([{"a": 1}, {"b": 2}, 3])
        obj = jsify(it)
        self.assertIsInstance(obj, JsifyIterator)

    def test_jsified_iterator_basic_dot_and_index_access(self):
        it = iter([{"a": 1}, {"b": 2}, 3])
        obj = jsify(it)
        items = list(obj)
        self.assertEqual(items[0].a, 1)
        self.assertEqual(items[1].b, 2)
        self.assertEqual(items[2], 3)

    def test_jsified_iterator_hasattr_and_dot_access(self):
        it = iter([{"a": 1}, 2])
        obj = jsify(it)
        item = next(obj)
        self.assertTrue(hasattr(item, "a"))
        self.assertEqual(item.a, 1)
        item2 = next(obj)
        self.assertTrue(item2.a == Undefined)

    def test_jsified_iterator_nested_jsification(self):
        it = iter([{"x": {"y": 5}}])
        obj = jsify(it)
        item = next(obj)
        self.assertEqual(item.x.y, 5)

    def test_jsified_iterator_attribute_error_on_nonjsified_item(self):
        it = iter([1])
        obj = jsify(it)
        item = next(obj)
        self.assertEqual(item.foo, Undefined)

    def test_jsified_iterator_exhaustion_and_reuse(self):
        obj = jsify(iter([1, 2]))
        items1 = list(obj)
        self.assertEqual(items1, [1, 2])
        items2 = list(obj)
        self.assertEqual(items2, [])

    def test_jsified_iterator_no_random_access(self):
        obj = jsify(iter([{"a": 1}, {"b": 2}]))
        with self.assertRaises(TypeError):
            _ = obj[0]

    def test_jsified_iterator_stop_iteration(self):
        obj = jsify(iter([]))
        with self.assertRaises(StopIteration):
            next(obj)

    def test_jsified_iterator_safe_chaining(self):
        it = iter([{"a": 1}])
        obj = jsify(it)
        item = next(obj)
        self.assertIs(item.b, Undefined)

    def test_jsified_iterator_jsified_values_are_reference_not_copy(self):
        l = [{"a": 1}]
        it = iter(l)
        obj = jsify(it)
        item = next(obj)
        item.a = 42
        self.assertEqual(l[0]["a"], 42)

if __name__ == "__main__":
    unittest.main()
