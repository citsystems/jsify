import unittest
from jsify import jsify, jsified_items, jsified_update, unjsify
from jsify.json import jsified_dumps, Undefined
from jsify.simplify import loads_simplified

class TestJsifyDocExamples(unittest.TestCase):
    def test_simplifiedobject_simple_access(self):
        data = '{"user": {"profile": null}}'
        obj = loads_simplified(data)
        self.assertTrue(hasattr(obj, "user"))
        # user is SimplifiedObject, profile is None
        self.assertIsNone(obj.user.profile)
        # missing top-level attribute returns Undefined
        self.assertIs(obj.no_such_field, Undefined)

    def test_simplifiedobject_missing_nested(self):
        data = '{"a": 1, "b": 2}'
        obj = loads_simplified(data)
        self.assertEqual(obj.a, 1)
        self.assertIs(obj.z, Undefined)
        # if obj.b is a dict, would need to wrap it for dot access
        # not applicable here since b is int

    def test_jsify_dot_and_item_access(self):
        data = {"settings": {"theme": "dark"}, "items": [1, 2, 3]}
        obj = jsify(data)
        self.assertEqual(obj.settings.theme, "dark")
        self.assertEqual(obj.items[1], 2)
        # reflect changes
        data["settings"]["theme"] = "light"
        self.assertEqual(obj.settings.theme, "light")

    def test_jsify_nested_mutation(self):
        orig = {"foo": {"bar": 1}}
        o = jsify(orig)
        self.assertEqual(o.foo.bar, 1)
        orig["foo"]["bar"] = 2
        self.assertEqual(o.foo.bar, 2)

    def test_undefined_deep_access(self):
        wrapped = jsify({"user": {}})
        self.assertIsInstance(wrapped.user.profile.email, type(Undefined))
        self.assertIs(wrapped.user.profile.email, Undefined)
        # boolean check
        if not wrapped.user.notexisting.anything:
            executed = True
        else:
            executed = False
        self.assertTrue(executed)

    def test_serialization(self):
        obj = jsify({"a": 1, "b": None, "c": Undefined})
        s1 = jsified_dumps(obj)
        self.assertIn('"a": 1', s1)
        self.assertIn('"b": null', s1)
        self.assertNotIn('"c"', s1)
        s2 = jsified_dumps(obj, omit_undefined=False)
        self.assertIn('"c": null', s2)

    def test_no_key_conflicts(self):
        data = {"items": "DATA"}
        obj = jsify(data)
        self.assertEqual(obj.items, "DATA")
        self.assertEqual(list(jsified_items(obj)), [("items", "DATA")])
        orig = unjsify(obj)
        self.assertEqual(list(orig.items()), [("items", "DATA")])

    def test_key_masking_builtins(self):
        data = {"update": "NOT_A_METHOD"}
        obj = jsify(data)
        self.assertEqual(obj.update, "NOT_A_METHOD")
        jsified_update(obj, {"x": 5})
        self.assertEqual(obj.x, 5)

if __name__ == "__main__":
    unittest.main()
