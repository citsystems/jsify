import io
import json
import unittest
from jsify import jsify, Undefined
from jsify.json import jsified_dumps, jsified_dump, ObjectEncoder


class TestJsifyJson(unittest.TestCase):
    def setUp(self):
        self.obj = jsify({"a": 1, "b": Undefined, "c": [1, {"x": Undefined}]})

    def test_jsified_dumps_omit_undefined_true(self):
        # Default omit_undefined=True: fields with Undefined omitted
        result = jsified_dumps(self.obj)
        expected = '{"a": 1, "c": [1, {}]}'
        self.assertEqual(result, expected)

    def test_jsified_dumps_omit_undefined_false(self):
        # Serialize Undefined as null
        result = jsified_dumps(self.obj, omit_undefined=False)
        expected = '{"a": 1, "b": null, "c": [1, {"x": null}]}'
        self.assertEqual(result, expected)

    def test_jsified_dumps_with_indent(self):
        # Indented output, omit_undefined default (True)
        result = jsified_dumps(self.obj, indent=2)
        # Load back to check correctness ignoring whitespace
        loaded = json.loads(result)
        expected = {"a": 1, "c": [1, {}]}
        self.assertEqual(loaded, expected)

    def test_jsified_dump_to_file_like(self):
        # Write to file-like object and check content
        f = io.StringIO()
        jsified_dump(self.obj, f, indent=2)
        f.seek(0)
        loaded = json.load(f)
        expected = {"a": 1, "c": [1, {}]}
        self.assertEqual(loaded, expected)

    def test_jsify_dot_access_after_loading(self):
        # Test loading json and wrapping with jsify enables dot access
        json_str = '{"a": 1, "b": {"c": 2}}'
        data = json.loads(json_str)
        obj = jsify(data)
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b.c, 2)
        # Access missing attribute returns Undefined
        self.assertIs(obj.b.x, Undefined)

    def test_standard_json_dumps_without_encoder_raises(self):
        # Using json.dumps directly on jsified object should raise TypeError
        with self.assertRaises(TypeError):
            json.dumps(self.obj)

    def test_standard_json_dumps_with_encoder_succeeds(self):
        # Using json.dumps with cls=ObjectEncoder should succeed
        result = json.dumps(self.obj, cls=ObjectEncoder)
        loaded = json.loads(result)
        expected = {"a": 1, "c": [1, {}]}
        self.assertEqual(loaded, expected)


if __name__ == "__main__":
    unittest.main()
