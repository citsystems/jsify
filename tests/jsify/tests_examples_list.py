import unittest
from jsify import jsify, Iterator, Undefined


class TestJsifyList(unittest.TestCase):
    def setUp(self):
        self.data = [{"a": 1}, {"b": 2}, 3]
        self.js_list = jsify(self.data)

    def test_type_and_access(self):
        self.assertEqual(type(self.js_list).__name__, "List")
        self.assertEqual(self.js_list[0]["a"], 1)
        self.assertEqual(self.js_list[1]["b"], 2)
        self.assertEqual(self.js_list[2], 3)

    def test_modification_reflection(self):
        self.js_list[1]["b"] = 20
        self.assertEqual(self.data[1]["b"], 20)

        self.js_list[0]["a"] = 10
        self.assertEqual(self.data[0]["a"], 10)

    def test_append_and_access(self):
        self.js_list.append({"c": 3})
        self.assertEqual(self.js_list[-1]["c"], 3)
        self.assertEqual(self.data[-1]["c"], 3)

    def test_slicing_returns_jsified_list(self):
        sublist = self.js_list[:2]
        self.assertEqual(type(sublist).__name__, "List")
        self.assertEqual(sublist[1]["b"], 2)

    def test_iteration_and_len(self):
        collected = []
        for item in self.js_list:
            collected.append(item)
        self.assertEqual(len(collected), len(self.js_list))
        self.assertEqual(len(self.js_list), len(self.data))

    def test_iteration_returns_iterator(self):
        it = iter(self.js_list)
        self.assertEqual(type(it).__name__, "Iterator")
        items = list(it)
        self.assertEqual(len(items), len(self.js_list))
        self.assertEqual(items[0]["a"], 1)

    def test_equality_with_native(self):
        self.assertTrue(self.js_list[2] == 3)
        # jsified dict and native dict compare equal on content:
        self.assertTrue(self.js_list[0] == {"a": 1})

    def test_remove_and_len(self):
        self.js_list.remove(3)
        self.assertEqual(len(self.js_list), 2)
        self.assertEqual(len(self.data), 2)
        with self.assertRaises(ValueError):
            self.js_list.remove(999)  # not in list

    def test_index_and_pop(self):
        idx = self.js_list.index(self.js_list[0])
        self.assertEqual(idx, 0)
        popped = self.js_list.pop()
        self.assertEqual(popped, 3)
        self.assertEqual(len(self.js_list), len(self.data))

        with self.assertRaises(IndexError):
            empty_list = jsify([])
            empty_list.pop(0)

    def test_clear(self):
        self.js_list.clear()
        self.assertEqual(len(self.js_list), 0)
        self.assertEqual(len(self.data), 0)

    def test_missing_attribute_returns_undefined(self):
        # dot access on List elements is not supported, but attribute on list itself returns Undefined
        self.assertIs(getattr(self.js_list, "nope", Undefined), Undefined)

    def test_index_out_of_range_returns_undefined(self):
        val = self.js_list[1000]
        self.assertIs(val, Undefined)

    def test_dot_access_on_list_elements_illegal(self):
        # dot access on list elements is not supported, should raise AttributeError
        with self.assertRaises(AttributeError):
            _ = self.js_list.nope.foo


if __name__ == "__main__":
    unittest.main()
