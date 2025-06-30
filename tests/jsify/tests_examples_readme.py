import unittest
from jsify.simplify import loads_simplified, SimplifiedObject, simplified_dumps, Undefined
from jsify import (
    jsify, jsified_get, jsified_pop, jsified_setdefault, jsified_update,
    jsified_items, jsified_keys, jsified_values, jsified_copy, jsified_deepcopy,
    unjsify, unjsify_deepcopy, Dict, List, Tuple, Iterator, Object
)
from jsify.json import jsified_dumps

class TestJsifyExamples(unittest.TestCase):
    # 1. Safe, Shallow Dot Access (SimplifiedObject)
    def test_simplifiedobject_loads_simplified(self):
        obj = loads_simplified('{"user": {"profile": null}}')
        self.assertIsInstance(obj, SimplifiedObject)
        self.assertIsInstance(obj.user, SimplifiedObject)
        self.assertIsNone(obj.user.profile)
        self.assertIs(obj.not_found, Undefined)
        self.assertIs(obj.user.missing, Undefined)

    def test_simplifiedobject_manual_wrap(self):
        plain_dict = {"profile": None}
        top = SimplifiedObject(**plain_dict)
        self.assertIsInstance(top, SimplifiedObject)
        self.assertIsNone(top.profile)
        self.assertIs(top.missing, Undefined)
        obj2 = SimplifiedObject(user={"profile": None})
        self.assertIsInstance(obj2.user, dict)
        with self.assertRaises(AttributeError):
            _ = obj2.user.profile
        nested = SimplifiedObject(**obj2.user)
        self.assertIsNone(nested.profile)
        self.assertIs(nested.missing, Undefined)

    def test_simplifiedobject_serialization_includes_undefined_as_null(self):
        obj = SimplifiedObject(a=1, b=None, c=Undefined)
        json_str = simplified_dumps(obj)
        self.assertIn('"a": 1', json_str)
        self.assertIn('"b": null', json_str)
        self.assertIn('"c": null', json_str)  # <-- This is correct

    # 2. Deep Jsified Wrapping
    def test_jsify_recursive_dot(self):
        data = {'user': {'name': 'Alice', 'profile': {'age': 30}}}
        obj = jsify(data)
        self.assertEqual(obj.user.name, 'Alice')
        self.assertEqual(obj.user.profile.age, 30)
        lst = {'numbers': [10, 20, 30], 'coords': (1, 2, 3)}
        w = jsify(lst)
        self.assertEqual(w.numbers[1], 20)
        self.assertEqual(w.coords[2], 3)
        it = jsify(iter([100, 200, 300]))
        self.assertEqual(next(it), 100)
        self.assertEqual(next(it), 200)
        self.assertEqual(next(it), 300)
        with self.assertRaises(StopIteration):
            next(it)

    # 3. Handling Missing Properties with Undefined
    def test_missing_returns_undefined(self):
        obj = jsify({'user': {}})
        self.assertIs(obj.user.profile.name.something.deep, Undefined)
        self.assertIs(obj.user.profile, Undefined)
        self.assertFalse(Undefined)
        self.assertEqual(Undefined, None)
        self.assertEqual(Undefined, Undefined)

    # 4. Safe Deep Chaining
    def test_safe_chaining(self):
        deep_obj = jsify({'a': {}})
        self.assertIs(deep_obj.a.b.c.d.e.f.g, Undefined)
        self.assertFalse(deep_obj.a.b.c.d.e)

    # 5. Reference-Based Mutation
    def test_reference_mutation(self):
        data = {'config': {'value': 10}}
        obj = jsify(data)
        self.assertEqual(obj.config.value, 10)
        data['config']['value'] = 42
        self.assertEqual(obj.config.value, 42)
        obj.config.value = 100
        self.assertEqual(data['config']['value'], 100)

    # 6. Full Tooling API
    def test_tooling_api(self):
        obj = jsify({'a': 1, 'b': 2})
        self.assertEqual(jsified_get(obj, 'a'), 1)
        self.assertEqual(jsified_pop(obj, 'a'), 1)
        self.assertNotIn('a', [k for k in jsified_keys(obj)])
        self.assertEqual(jsified_setdefault(obj, 'c', 99), 99)
        jsified_update(obj, {'d': 4})
        keys = [k for k in jsified_keys(obj)]
        self.assertIn('b', keys)
        self.assertIn('c', keys)
        self.assertIn('d', keys)
        values = [v for v in jsified_values(obj)]
        self.assertIn(2, values)
        self.assertIn(99, values)
        self.assertIn(4, values)
        items = [pair for pair in jsified_items(obj)]
        self.assertIn(('b', 2), items)
        self.assertIn(('c', 99), items)
        self.assertIn(('d', 4), items)

    # 7. Shallow and Deep Copy
    def test_shallow_and_deep_copy(self):
        obj = jsify({'x': [1, 2]})
        shallow = jsified_copy(obj)
        deep = jsified_deepcopy(obj)
        self.assertIsNot(shallow, obj)
        self.assertIsNot(deep, obj)
        # Mutating shallow copy should affect original nested object
        shallow.x.append(3)
        self.assertIn(3, obj.x)
        # Mutating deep copy should not affect original
        deep.x.append(4)
        self.assertNotIn(4, obj.x)

    # 8. Bidirectional Conversion
    def test_bidirectional_conversion(self):
        obj = jsify({'hello': 123, 'nested': {'x': 1}})
        raw = unjsify(obj)
        self.assertIsInstance(raw, dict)
        self.assertEqual(raw['hello'], 123)
        deep_raw = unjsify_deepcopy(obj)
        self.assertIsInstance(deep_raw, dict)
        self.assertEqual(deep_raw['nested']['x'], 1)
        # Deep copy is not same reference as original
        self.assertIsNot(deep_raw, raw)

    # 9. Custom JSON Serialization
    def test_custom_json_serialization(self):
        data = {'name': 'Alice', 'details': {'age': 30, 'nickname': Undefined}}
        obj = jsify(data)
        s1 = jsified_dumps(obj)
        self.assertIn('"name": "Alice"', s1)
        self.assertIn('"age": 30', s1)
        self.assertNotIn('nickname', s1)
        s2 = jsified_dumps(obj, omit_undefined=False)
        self.assertIn('"nickname": null', s2)

    # 10. Explicit Wrappers
    def test_explicit_wrappers(self):
        d = Dict({'x': 1, 'y': 2})
        l = List([1, 2, 3])
        t = Tuple((1, 2, 3))
        it = Iterator(iter([1, 2, 3]))
        self.assertEqual(d.x, 1)
        self.assertEqual(l[1], 2)
        self.assertEqual(t[2], 3)
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 3)
        with self.assertRaises(StopIteration):
            next(it)

if __name__ == "__main__":
    unittest.main()
