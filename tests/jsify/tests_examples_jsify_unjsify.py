import unittest
from jsify import (
    jsify,
    jsified_deepcopy,
    unjsify,
    unjsify_deepcopy,
    Dict,
    List,
    Tuple,
    Iterator,
    Undefined
)


class TestJsifyDocExamples(unittest.TestCase):
    def test_jsify_types(self):
        self.assertIsInstance(jsify({"a": 1}), Dict)
        self.assertIsInstance(jsify([1, 2, 3]), List)
        self.assertIsInstance(jsify((1, 2, 3)), Tuple)
        self.assertIsInstance(jsify(iter([1, 2])), Iterator)
        self.assertIsInstance(jsify((x for x in range(2))), Iterator)
        self.assertEqual(jsify(123), 123)
        self.assertIsNone(jsify(None))

    def test_jsify_nested_types(self):
        obj = jsify({"foo": [1, {"bar": 2}]})
        self.assertIsInstance(obj.foo, List)
        self.assertIsInstance(obj.foo[1], Dict)
        # Reference mutation
        obj.foo[1].bar = 99
        self.assertEqual(obj.foo[1].bar, 99)
        self.assertEqual(obj["foo"][1]["bar"], 99)

    def test_jsify_scalars_unchanged(self):
        self.assertEqual(jsify(42), 42)
        self.assertEqual(jsify("abc"), "abc")
        self.assertTrue(jsify(True))
        self.assertIs(jsify(Undefined), Undefined)

    def test_jsify_missing_key_attribute(self):
        obj = jsify({"foo": [1, {"bar": 2}]})
        # attribute
        self.assertIs(obj.not_present, Undefined)
        # out-of-bounds on list
        self.assertIs(obj.foo[99], Undefined)
        # nested missing
        self.assertIs(obj.foo[1].not_here, Undefined)

    def test_jsified_deepcopy(self):
        original = {"x": {"y": [1, 2, {"z": 3}]}}
        obj = jsify(original)
        obj2 = jsified_deepcopy(obj)
        # Mutate original via jsified
        obj.x.y[2].z = 99
        self.assertEqual(original["x"]["y"][2]["z"], 99)
        # Mutate deep copy does not affect original
        obj2.x.y[2].z = 100
        self.assertEqual(original["x"]["y"][2]["z"], 99)
        self.assertEqual(obj2.x.y[2].z, 100)

    def test_unjsify_shallow(self):
        d = {"foo": {"bar": 1}}
        obj = jsify(d)
        orig = unjsify(obj)
        self.assertIs(orig, d)
        self.assertIsInstance(unjsify(obj.foo), dict)

    def test_unjsify_deepcopy(self):
        profile = jsify({"name": "Alice"})
        data = {"profile": profile, "type": "admin"}
        user = jsify(data)
        # .profile is still jsified
        self.assertIsInstance(user.profile, Dict)
        # Shallow unjsify
        shallow = unjsify(user)
        self.assertIsInstance(shallow["profile"], Dict)
        # Deep unjsify
        deep = unjsify_deepcopy(user)
        self.assertIsInstance(deep["profile"], dict)
        self.assertEqual(deep["profile"]["name"], "Alice")
        self.assertEqual(deep["type"], "admin")

    def test_unjsify_deepcopy_for_nested_jsified(self):
        # Test if deeply nested jsified objects are unwrapped
        profile = jsify({"person": {"name": "Bob"}})
        data = {"profile": profile, "type": "admin"}
        user = jsify(data)
        result = unjsify_deepcopy(user)
        self.assertIsInstance(result["profile"], dict)
        self.assertEqual(result["profile"]["person"]["name"], "Bob")


if __name__ == "__main__":
    unittest.main()
