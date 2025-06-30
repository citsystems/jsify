import unittest
from jsify import jsify, unjsify, Undefined, Tuple, Iterator


class TestJsifyTuple(unittest.TestCase):
    def setUp(self):
        self.original = ({"x": 1}, {"y": 2}, 3)
        self.obj = jsify(self.original)

    def test_type_of_jsified_tuple(self):
        self.assertIsInstance(self.obj, Tuple)

    def test_index_access(self):
        self.assertEqual(self.obj[0].x, 1)
        self.assertEqual(self.obj[1].y, 2)
        self.assertEqual(self.obj[2], 3)

    def test_slice_returns_jsified_tuple(self):
        sub = self.obj[:2]
        self.assertIsInstance(sub, Tuple)
        self.assertEqual(sub[1].y, 2)

    def test_iteration_returns_iterator(self):
        it = iter(self.obj)
        self.assertIsInstance(it, Iterator)

        # Collect items via iterator
        items = list(it)
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].x, 1)
        self.assertEqual(items[1].y, 2)
        self.assertEqual(items[2], 3)

    def test_count_and_index_methods(self):
        self.assertEqual(self.obj.count({"x": 1}), 1)
        self.assertEqual(self.obj.index({"y": 2}), 1)

    def test_len(self):
        self.assertEqual(len(self.obj), 3)

    def test_str_and_repr(self):
        s = str(self.obj)
        r = repr(self.obj)
        self.assertIsInstance(s, str)
        self.assertIsInstance(r, str)

    def test_reference_behavior(self):
        original = ({"a": 1},)
        t = jsify(original)
        t[0].a = 42
        self.assertEqual(original[0]["a"], 42)

    def test_assignment_to_tuple_element_raises(self):
        with self.assertRaises(TypeError):
            self.obj[0] = 100

    def test_index_out_of_range_returns_undefined(self):
        val = self.obj[1000]
        self.assertIs(val, Undefined)

    def test_missing_attribute_returns_undefined(self):
        self.assertIs(self.obj[0].missing_attr, Undefined)

    def test_dot_access_on_tuple_itself_not_supported(self):
        with self.assertRaises(AttributeError):
            _ = self.obj.some_method

    def test_conversion_back_to_native(self):
        back = unjsify(self.obj)
        self.assertEqual(back, self.original)


if __name__ == "__main__":
    unittest.main()
