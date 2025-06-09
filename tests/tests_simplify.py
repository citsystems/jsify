import time
from json import loads
from types import SimpleNamespace
from unittest import TestCase

from jsify.simplify import SimplifiedObject, simplified_dumps


class TestSimplify(TestCase):
    def setUp(self):
        self.sample_json_string = """{"a": 1, "b": 2, "c": [1, 2, 3, 4, {"a": 1, "b": 2}]}"""
        self.sample_json = loads(self.sample_json_string)
        self.sample_simplified = SimplifiedObject(a=1, b=2, c=[1, 2, 3, 4, SimplifiedObject(a=1, b=2)])
        self.sample_sn = SimpleNamespace(a=1, b=2, c=[1, 2, 3, 4, SimpleNamespace(a=1, b=2)])

    def test_json_loads(self):
        from jsify.simplify import loads_simplified
        self.assertEqual(loads_simplified(self.sample_json_string), self.sample_simplified)

    def test_json_dumps(self):
        json_str = simplified_dumps(self.sample_simplified)
        self.assertEqual(json_str, self.sample_json_string)

    def test_benchmark(self):
        start = time.time()
        n = 1000000
        for _ in range(n):
            a = self.sample_simplified.a
            b = self.sample_simplified.f
        print(f"Simplified {n} operations: {time.time() - start}")
        start = time.time()
        n = 1000000
        for _ in range(n):
            a = self.sample_sn.a
            b = self.sample_sn.b
        print(f"SimpleNamespace {n} operations: {time.time() - start}")