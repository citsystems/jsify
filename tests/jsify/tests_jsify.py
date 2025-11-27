import gc
import time
from copy import copy
from types import SimpleNamespace
from unittest import TestCase

from box import Box
from jsify import List, Dict, jsify, jsified_copy, jsified_get, jsified_pop, jsified_popitem, jsified_setdefault, \
    jsified_update, \
    jsified_values, jsified_keys, jsified_items, unjsify, Iterator, Object, Undefined, unjsify_deepcopy
from jsify.json import jsified_dumps
from dotmap import DotMap


class TestObject(TestCase):
    test_dict = dict(a=1, b=dict(a=1, b=2, c=3), c=3)
    test_merge = dict(d=1, e=dict(a=1, b=2, c=3), f=3)
    test_list = [1, 2, 3, 4, 5, 6, 7, test_dict, test_merge]
    test_tuple = (1, dict(a=1, b=2, c=3), 3, test_dict)
    test_literal = 2
    test_types_dict = dict(list=test_list, dict=test_dict, tuple=test_tuple, literal=test_literal)
    test_types_list = [test_types_dict['list'], test_types_dict['dict'], test_types_dict['tuple'], test_literal]
    test_types_tuple = (test_types_dict['list'], test_types_dict['dict'], test_types_dict['tuple'], test_literal)
    test_json_string = """{
      "company": "Tech Innovators",
      "location": {
        "country": "USA",
        "state": "California",
        "address": {
          "street": "123 Tech Drive",
          "city": "Silicon Valley",
          "zip": "94043"
        }
      },
      "employees": [
        {
          "name": "Alice",
          "role": "Engineer",
          "projects": [
            {
              "name": "AI Development",
              "duration": "6 months",
              "technologies": ["Python", "TensorFlow", "Keras"]
            },
            {
              "name": "Web Platform",
              "duration": "12 months",
              "technologies": ["JavaScript", "React", "Node.js"]
            }
          ]
        },
        {
          "name": "Bob",
          "role": "Designer",
          "projects": [
            {
              "name": "Mobile App Design",
              "duration": "3 months",
              "tools": ["Sketch", "Figma"]
            }
          ]
        }
      ],
      "departments": [
        {
          "name": "Engineering",
          "head": {
            "name": "Charlie",
            "age": 45,
            "experience": {
              "years": 20,
              "fields": ["Software Development", "AI", "Cloud Computing"]
            }
          },
          "budget": 1500000,
          "teams": [
            {
              "name": "Frontend",
              "members": ["Alice", "David", "Eva"]
            },
            {
              "name": "Backend",
              "members": ["Frank", "George"]
            }
          ]
        },
        {
          "name": "Design",
          "head": {
            "name": "Diana",
            "age": 38,
            "experience": {
              "years": 15,
              "fields": ["UI/UX", "Graphic Design"]
            }
          },
          "budget": 800000,
          "tools": ["Photoshop", "Illustrator", "InDesign"]
        }
      ],
      "initiatives": [
        {
          "year": 2023,
          "goals": [
            "Expand market share",
            "Develop new product line",
            "Increase customer satisfaction"
          ],
          "milestones": {
            "Q1": "Research and Planning",
            "Q2": "Development",
            "Q3": "Testing",
            "Q4": "Launch"
          }
        },
        {
          "year": 2024,
          "goals": [
            "Global Expansion",
            "AI Integration",
            "Sustainability Initiatives"
          ],
          "milestones": {
            "Q1": "Market Analysis",
            "Q2": "Product Design",
            "Q3": "Implementation",
            "Q4": "Evaluation"
          }
        }
      ],
      "miscellaneous": {
        "isPublicCompany": false,
        "established": 2005,
        "stockPrices": [
          {
            "year": 2021,
            "prices": [150.25, 155.5, 160.75, 162.0]
          },
          {
            "year": 2022,
            "prices": [165.0, 170.25, 175.75, 180.5]
          }
        ],
        "recentEvents": [
          {
            "type": "Conference",
            "name": "Tech Summit 2023",
            "attendees": [
              {"name": "Alice", "role": "Speaker"},
              {"name": "Charlie", "role": "Panelist"}
            ]
          },
          {
            "type": "Product Launch",
            "name": "NextGen AI Platform",
            "launchDate": "2023-09-15"
          }
        ]
      }
    }"""

    def test_create_from_literal(self):
        self.assertEqual(jsify(1), 1)
        self.assertEqual(jsify(1.1), 1.1)
        self.assertEqual(jsify("string"), "string")
        self.assertEqual(jsify(None), None)
        self.assertEqual(jsify(True), True)

    def test_create_from_dict(self):
        json_object = jsify(self.test_dict)
        self.assertIsInstance(json_object, Dict)
        self.assertDictEqual(unjsify(json_object), self.test_dict)

    def test_create_from_dict_with_merge(self):
        json_object = jsify(self.test_dict, **self.test_merge)
        self.assertIsInstance(json_object, Dict)
        self.assertDictEqual(unjsify(json_object), self.test_dict | self.test_merge)

    def test_create_from_list(self):
        self.assertListEqual(list(jsify(self.test_list)), self.test_list)

    def test_create_from_tuple(self):
        self.assertTupleEqual(tuple(jsify(self.test_tuple)), self.test_tuple)

    def test_get_from_dict(self):
        json_object = jsify(self.test_types_dict)
        self.assertNotIsInstance(json_object.literal, Object)
        self.assertEqual(json_object.literal, self.test_literal)
        self.assertIsInstance(json_object.dict, Dict)
        self.assertDictEqual(unjsify(json_object.dict), self.test_dict)
        self.assertIsInstance(json_object.list, List)
        self.assertListEqual(unjsify(json_object.list), self.test_list)
        self.assertIsInstance(json_object.tuple, Object)
        self.assertTupleEqual(unjsify(json_object.tuple), self.test_tuple)

        self.assertNotIsInstance(json_object['literal'], Object)
        self.assertEqual(json_object['literal'], self.test_literal)
        self.assertIsInstance(json_object['dict'], Object)
        self.assertDictEqual(unjsify(json_object['dict']), self.test_dict)
        self.assertIsInstance(json_object['list'], Object)
        self.assertListEqual(unjsify(json_object['list']), self.test_list)
        self.assertIsInstance(json_object['tuple'], Object)
        self.assertTupleEqual(unjsify(json_object['tuple']), self.test_tuple)

    def macro_test_get_from_list_or_tuple(self, json_object):
        self.assertIsInstance(json_object[0], Object)
        self.assertListEqual(unjsify(json_object[0]), self.test_list)
        self.assertIsInstance(json_object[1], Object)
        self.assertDictEqual(unjsify(json_object[1]), self.test_dict)
        self.assertIsInstance(json_object[2], Object)
        self.assertTupleEqual(unjsify(json_object[2]), self.test_tuple)
        self.assertNotIsInstance(json_object[3], Object)
        self.assertEqual(json_object[3], self.test_literal)

    def test_get_from_list(self):
        self.macro_test_get_from_list_or_tuple(jsify(self.test_types_list))

    def test_get_from_tuple(self):
        self.macro_test_get_from_list_or_tuple(jsify(self.test_types_tuple))

    def test_create_attributes_in_dict(self):
        json_object = jsify(self.test_dict.copy())
        json_object.new_literal = self.test_literal
        json_object.new_dict = self.test_dict
        json_object.new_list = self.test_list
        json_object.new_tuple = self.test_tuple
        self.assertDictEqual(unjsify(json_object), self.test_dict | dict(
            new_literal=self.test_literal, new_dict=self.test_dict, new_list=self.test_list, new_tuple=self.test_tuple))

        additional_json_object = jsify(self.test_dict)
        json_object.additional_json = additional_json_object
        self.assertNotIsInstance(unjsify(json_object.additional_json), Object)

        json_object = jsify(self.test_dict.copy())
        json_object['new_literal'] = self.test_literal
        json_object['new_dict'] = self.test_dict
        json_object['new_list'] = self.test_list
        json_object['new_tuple'] = self.test_tuple
        self.assertDictEqual(unjsify(json_object), self.test_dict | dict(
            new_literal=self.test_literal, new_dict=self.test_dict, new_list=self.test_list, new_tuple=self.test_tuple))

        additional_json_object = jsify(self.test_dict)
        json_object['additional_json'] = additional_json_object
        self.assertNotIsInstance(unjsify(json_object['additional_json']), Object)

    def test_create_elements_in_list(self):
        json_object = jsify(self.test_list.copy())
        json_object.append(self.test_literal)
        json_object.append(self.test_dict)
        json_object.append(self.test_list)
        json_object.append(self.test_tuple)
        self.assertListEqual(unjsify(json_object), self.test_list +
                             [self.test_literal, self.test_dict, self.test_list, self.test_tuple])

        additional_json_object = jsify(self.test_dict)
        json_object.append(additional_json_object)
        self.assertNotIsInstance(unjsify(json_object[-1]), Object)

    def test_vars_dir(self):
        # list -> dir contains string indexes
        json_object = jsify(self.test_list)
        for i in range(len(self.test_list)):
            self.assertIn(str(i), dir(json_object))

        # tuple -> dir contains string indexes
        json_object = jsify(self.test_tuple)
        for i in range(len(self.test_tuple)):
            self.assertIn(str(i), dir(json_object))

        # dict -> dir contains all original dict keys (as strings)
        json_object = jsify(self.test_dict)
        for key in self.test_dict.keys():
            self.assertIn(str(key), dir(json_object))

    def test_contains(self):
        json_object = jsify(self.test_dict)
        self.assertIn('a', json_object)
        self.assertNotIn('v', json_object)
        json_object = jsify(self.test_list)
        self.assertIn(self.test_dict, json_object)
        self.assertIn(1, json_object)
        self.assertNotIn(10, json_object)
        json_object = jsify(self.test_tuple)
        self.assertIn(self.test_dict, json_object)
        self.assertIn(1, json_object)
        self.assertNotIn(10, json_object)

    def macro_test_copy(self, obj, modified_key=None):
        json_object = jsify(obj)
        json_object_copy1 = json_object.__copy__()
        json_object_copy2 = copy(json_object_copy1)
        self.assertIsInstance(json_object_copy1, Object)
        self.assertIsInstance(json_object_copy2, Object)
        self.assertEqual(unjsify(json_object_copy1), obj)
        self.assertEqual(unjsify(json_object_copy2), obj)
        if modified_key is not None:
            json_object_copy1[modified_key] = None
            json_object_copy2[modified_key] = None
            self.assertNotEqual(unjsify(json_object_copy1), obj)
            self.assertNotEqual(unjsify(json_object_copy2), obj)

    def test_copy(self):
        self.macro_test_copy(self.test_list, 0)
        self.macro_test_copy(self.test_tuple)
        self.macro_test_copy(self.test_dict, 'a')

    def test_tuple_functions(self):
        json_object = jsify(self.test_tuple)
        self.assertEqual(json_object.count(1), self.test_tuple.count(1))
        self.assertEqual(json_object.index(1), self.test_tuple.index(1))

    def test_list_functions(self):
        test_list = self.test_list.copy()
        json_object = jsify(test_list).copy()
        self.assertEqual(json_object.count(self.test_dict), test_list.count(self.test_dict))
        self.assertEqual(json_object.count(jsify(self.test_dict)), test_list.count(self.test_dict))
        self.assertEqual(json_object.index(self.test_dict), test_list.index(self.test_dict))
        self.assertEqual(json_object.index(jsify(self.test_dict)), test_list.index(self.test_dict))
        json_object.append(10)
        json_object.append(jsify(self.test_dict))
        test_list.append(10)
        test_list.append(self.test_dict)
        self.assertEqual(unjsify(json_object), test_list)
        inserted = [9,8,7]
        json_object.insert(2, jsify(inserted))
        self.assertNotIsInstance(unjsify(json_object)[2], Object)
        test_list.insert(2, inserted)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.remove(jsify(inserted))
        test_list.remove(inserted)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.extend(jsify(inserted))
        test_list.extend(inserted)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.pop(3)
        test_list.pop(3)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.reverse()
        test_list.reverse()
        self.assertEqual(unjsify(json_object), test_list)
        for value in list(iter(json_object)):
            if isinstance(value, Dict):
                json_object.remove(value)
                test_list.remove(value)
        json_object.sort(key=lambda a: str(a))
        test_list.sort(key=lambda a: str(a))
        self.assertEqual(unjsify(json_object), test_list)
        json_object.clear()
        test_list.clear()
        self.assertEqual(unjsify(json_object), test_list)

    def test_list_arithmetic(self):
        l1 = jsify([1, 2, 3])
        l2 = jsify([4, 5])

        # Addition
        self.assertEqual(list(l1 + l2), [1, 2, 3, 4, 5])

        # Multiplication
        self.assertEqual(list(l1 * 2), [1, 2, 3, 1, 2, 3])
        self.assertEqual(list(2 * l2), [4, 5, 4, 5])

        # In-place addition
        l3 = jsify([1, 2])
        l3 += jsify([3, 4])
        self.assertEqual(list(l3), [1, 2, 3, 4])

        # In-place multiplication
        l4 = jsify([1, 2])
        l4 *= 2
        self.assertEqual(list(l4), [1, 2, 1, 2])

    def test_list_comparisons(self):
        l1 = jsify([1, 2, 3])
        l2 = jsify([1, 2, 4])
        l3 = jsify([1, 2, 3])

        self.assertTrue(l1 < l2)
        self.assertTrue(l2 > l1)
        self.assertTrue(l1 <= l3)
        self.assertTrue(l1 >= l3)
        self.assertFalse(l1 > l2)
        self.assertFalse(l1 < l3)
        self.assertFalse(l1 > l3)
        self.assertFalse(l2 < l1)

    def test_list_indexing_and_slicing(self):
        l1 = jsify([1, 2, 3, 4, 5])

        # Negative index
        self.assertEqual(l1[-1], 5)

        # Slicing
        self.assertEqual(list(l1[1:3]), [2, 3])

        # Delete slice
        l1 = jsify([1, 2, 3, 4, 5])
        #del l1[1:3]
        #self.assertEqual(list(l1), [1, 4, 5])

    def test_dict_functions(self):
        test_dict = self.test_dict.copy()
        json_object = jsified_copy(jsify(test_dict))
        self.assertEqual(jsified_get(json_object, 'a'), test_dict.get('a'))
        self.assertListEqual(list(jsified_items(json_object)), list(test_dict.items()))
        self.assertListEqual(list(jsified_keys(json_object)), list(test_dict.keys()))
        self.assertListEqual(list(jsified_values(json_object)), list(test_dict.values()))
        jsified_pop(json_object, 'a')
        test_dict.pop('a')
        self.assertEqual(jsify(json_object), test_dict)
        jsified_popitem(json_object)
        test_dict.popitem()
        self.assertEqual(len(json_object), len(test_dict))
        default_value1 = jsified_setdefault(json_object, 'default_test', 3)
        jsified_setdefault(json_object, 'default_test', 8)
        default_value2 = test_dict.setdefault('default_test', 3)
        test_dict.setdefault('default_test', 8)
        self.assertEqual(default_value1, default_value2)
        self.assertEqual(default_value1, json_object.default_test)
        self.assertEqual(default_value2, test_dict['default_test'])
        test_dict = dict(a=1,b=2)
        json_object = jsified_copy(test_dict)
        jsified_update(json_object, dict(z=1, n=2, m=3))
        test_dict.update(dict(z=1, n=2, m=3))
        self.assertEqual(jsify(json_object), test_dict)

    def test_json_dump(self):
        json_object = jsify(dict(a=1, b=2, c=jsify(self.test_dict), d=jsify(self.test_list),
                                 e=jsify(self.test_tuple), undef=Undefined))
        test_dict_with_undefined = dict(a=1, b=2, c=self.test_dict, d=self.test_list, e=self.test_tuple,
                                        undef=Undefined)
        test_dict_without_undefined = dict(a=1, b=2, c=self.test_dict, d=self.test_list, e=self.test_tuple)
        self.assertNotEqual(jsified_dumps(json_object, omit_undefined=False), jsified_dumps(test_dict_with_undefined))
        self.assertEqual(jsified_dumps(json_object, omit_undefined=False),
                         jsified_dumps(test_dict_with_undefined, omit_undefined=False))
        self.assertEqual(jsified_dumps(json_object), jsified_dumps(test_dict_without_undefined))
        self.assertNotEqual(jsified_dumps(json_object, omit_undefined=False), jsified_dumps(test_dict_without_undefined))

    def test_keys_values_items(self):
        json_object = jsify(self.test_dict)
        keys = jsified_keys(json_object)
        self.assertEqual(list(keys), list(self.test_dict.keys()))
        values = jsified_values(json_object)
        self.assertEqual(list(values), list(self.test_dict.values()))
        items = jsified_items(json_object)
        self.assertEqual(list(items), list(self.test_dict.items()))

    """
    
    def test_pickle(self):
        json_object = jsify(self.test_list)
        json_object.append(self.test_literal)
        json_object.append(self.test_dict)
        json_object.append(self.test_tuple)
        pickled = pickle.dumps(json_object)
        depickled = pickle.loads(pickled)
        dir(depickled)
        self.assertEqual(depickled, json_object)

    """

    def test_undefined(self):
        json_object = jsify(self.test_dict)
        self.assertEqual(Undefined, None)
        self.assertNotEqual(Undefined, 0)
        self.assertTrue(Undefined is not True)
        self.assertTrue(Undefined is not False)
        self.assertTrue(Undefined != True)
        self.assertTrue(Undefined != False)
        self.assertTrue(Undefined == None)
        self.assertTrue(Undefined is not None)
        self.assertIs(json_object.not_defined_property, Undefined)
        self.assertIs(json_object.not_defined_property.fghjj.dsffsd['42'], Undefined)

    def test_iterator(self):
        dict_iterator = Iterator(self.test_dict)
        for json_key, native_key in zip(dict_iterator, self.test_dict.keys()):
            self.assertEqual(json_key, native_key)
        list_iterator = Iterator(self.test_list)
        for json_value, native_value in zip(list_iterator, self.test_list):
            self.assertEqual(json_value, native_value)
        tuple_iterator = Iterator(self.test_tuple)
        for json_value, native_value in zip(tuple_iterator, self.test_tuple):
            self.assertEqual(json_value, native_value)
        dict_iterator = Iterator(jsify(self.test_dict))
        for json_key, native_key in zip(dict_iterator, self.test_dict.keys()):
            self.assertEqual(json_key, native_key)
        list_iterator = Iterator(jsify(self.test_list))
        for json_value, native_value in zip(list_iterator, self.test_list):
            self.assertEqual(json_value, native_value)
        tuple_iterator = Iterator(jsify(self.test_tuple))
        for json_value, native_value in zip(tuple_iterator, self.test_tuple):
            self.assertEqual(json_value, native_value)

    def test_benchmark(self):
        N = 10000 # 1000000000000000000
        start = time.perf_counter()
        for n in range(N):
            d = jsify(self.test_dict)
            d.new_attribute = {}
            d.new_attribute.newdict = {}
            d.new_list = [1,2,3,4,5]
            a = d.mew_list[2]
            d.new_list[2] = {}
            d.new_attribute.new_subattribute = [1,2,3,4,5]
            d.new_list_clone = d.new_attribute.new_subattribute
            d.new_list_clone[4] = 10
        print(f"Jsify {N} operations: {time.perf_counter() - start:.6f} sec")
        start = time.perf_counter()
        for n in range(N):
            d = SimpleNamespace(**self.test_dict)
            d.new_attribute = SimpleNamespace()
            d.new_attribute.new_subattribute = [1, 2, 3, 4, 5]
            d.new_list_clone = d.new_attribute.new_subattribute
            d.new_list_clone[4] = 10
        print(f"SimpleNamespace {N} operations: {time.perf_counter() - start:.6f} sec")
        start = time.perf_counter()
        for n in range(N):
            d = Box(self.test_dict)
            d.new_attribute = SimpleNamespace()
            d.new_attribute.new_subattribute = [1, 2, 3, 4, 5]
            d.new_list_clone = d.new_attribute.new_subattribute
            d.new_list_clone[4] = 10
        print(f"Box {N} operations: {time.perf_counter() - start:.6f} sec")
        start = time.perf_counter()
        for n in range(N):
            d = DotMap(self.test_dict)
            d.new_attribute = SimpleNamespace()
            d.new_attribute.new_subattribute = [1, 2, 3, 4, 5]
            d.new_list_clone = d.new_attribute.new_subattribute
            d.new_list_clone[4] = 10
        print(f"DotMap {N} operations: {time.perf_counter() - start:.6f} sec")

    def test_dir_and_orig_access(self):
        # Dict
        d = {"a": 1, "b": 2, 3: "c"}
        obj = jsify(d)
        for k in d.keys():
            self.assertIn(str(k), dir(obj))
        self.assertEqual(type(obj.__orig__), type(d))

        # List
        l = [1, 2, 3, 4]
        obj = jsify(l)
        for i in range(len(l)):
            self.assertIn(str(i), dir(obj))
        self.assertEqual(type(obj.__orig__), type(l))

        # Tuple
        t = (10, 20, 30)
        obj = jsify(t)
        for i in range(len(t)):
            self.assertIn(str(i), dir(obj))
        self.assertEqual(type(obj.__orig__), type(t))

    def memory_usage(self):
        import os, psutil
        process = psutil.Process(os.getpid())
        mem_bytes = process.memory_info().rss  # resident set size in bytes
        mem_mb = mem_bytes // (4 * 1024)
        return mem_mb


    def test_memory_leak(self):
        start_memory = self.memory_usage()
        for i in range(30000):

            # CREATE
            jsify(1)
            jsify(1.1)
            jsify("string")
            jsify(None)
            jsify(True)

            json_object = jsify(self.test_dict)
            unjsify(json_object)

            jsify(self.test_dict, **self.test_merge)
            jsify(self.test_list)
            jsify(self.test_tuple)
            
            json_object = jsify(self.test_types_dict)
            json_object.literal
            json_object.dict
            json_object.list
            json_object.tuple
            json_object['literal']
            json_object['dict']
            json_object['list']
            json_object['tuple']

            jsify(self.test_types_list)
            jsify(self.test_types_tuple)

            json_object = jsify(self.test_dict.copy())
            json_object.new_literal = self.test_literal
            json_object.new_dict = self.test_dict
            json_object.new_list = self.test_list
            json_object.new_tuple = self.test_tuple

            additional_json_object = jsify(self.test_dict)
            json_object.additional_json = additional_json_object

            json_object = jsify(self.test_dict.copy())
            json_object['new_literal'] = self.test_literal
            json_object['new_dict'] = self.test_dict
            json_object['new_list'] = self.test_list
            json_object['new_tuple'] = self.test_tuple

            additional_json_object = jsify(self.test_dict)
            json_object['additional_json'] = additional_json_object


            json_object = jsify(self.test_list.copy())
            json_object.append(self.test_literal)
            json_object.append(self.test_dict)
            json_object.append(self.test_list)
            json_object.append(self.test_tuple)
            additional_json_object = jsify(self.test_dict)
            json_object.append(additional_json_object)

            json_object = jsify(self.test_list)
            dir(json_object)

            json_object = jsify(self.test_tuple)
            dir(json_object)

            json_object = jsify(self.test_dict)
            dir(json_object)

            json_object = jsify(self.test_dict)
            'a' in json_object
            'v' in json_object
            json_object = jsify(self.test_list)
            self.test_dict in json_object
            1 in json_object
            10 in json_object
            json_object = jsify(self.test_tuple)
            self.test_dict in json_object
            1 in json_object
            10 in json_object

            # COPY
            from copy import copy
            for obj, modified_key in [
                (self.test_list, 0),
                (self.test_tuple, None),
                (self.test_dict, 'a')
            ]:
                json_object = jsify(obj)
                json_object_copy1 = json_object.__copy__()
                json_object_copy2 = copy(json_object_copy1)
                if modified_key is not None:
                    json_object_copy1[modified_key] = None
                    json_object_copy2[modified_key] = None

            # TUPLE/LIST FUNCS
            json_object = jsify(self.test_tuple)
            json_object.count(1)
            json_object.index(1)
            test_list = self.test_list.copy()
            json_object = jsify(test_list).copy()
            json_object.count(self.test_dict)
            json_object.count(jsify(self.test_dict))
            json_object.index(self.test_dict)
            json_object.index(jsify(self.test_dict))
            json_object.append(10)
            json_object.append(jsify(self.test_dict))
            
            inserted = [9,8,7]
            json_object.insert(2, jsify(inserted))
            json_object.remove(jsify(inserted))
            json_object.extend(jsify(inserted))
            json_object.pop(3)
            json_object.reverse()

            for value in list(iter(json_object)):
                if isinstance(value, Dict):
                    json_object.remove(value)

            json_object.sort(key=lambda a: str(a))
            json_object.clear()

            # ARYTMETYKA LIST
            l1 = jsify([1, 2, 3])
            l2 = jsify([4, 5])
            l1 + l2
            l1 * 2
            2 * l2
            l3 = jsify([1, 2])
            l3 += jsify([3, 4])
            l4 = jsify([1, 2])
            l4 *= 2

            # LIST COMP
            l1 = jsify([1, 2, 3])
            l2 = jsify([1, 2, 4])
            l3 = jsify([1, 2, 3])
            l1 < l2
            l2 > l1
            l1 <= l3
            l1 >= l3
            l1 > l2
            l1 < l3
            l1 > l3
            l2 < l1

            # INDEXING/SLICING
            l1 = jsify([1, 2, 3, 4, 5])
            l1[-1]
            l1[1:3]

            # DICT FUNCS
            test_dict = self.test_dict.copy()
            json_object = jsified_copy(jsify(test_dict))
            jsified_get(json_object, 'a')
            list(jsified_items(json_object))
            list(jsified_keys(json_object))
            list(jsified_values(json_object))
            jsified_pop(json_object, 'a')
            jsified_popitem(json_object)
            jsified_setdefault(json_object, 'default_test', 3)
            jsified_setdefault(json_object, 'default_test', 8)
            test_dict = dict(a=1, b=2)
            json_object = jsified_copy(test_dict)
            jsified_update(json_object, dict(z=1, n=2, m=3))

            # KEYS/VALUES/ITEMS
            json_object = jsify(self.test_dict)
            keys = jsified_keys(json_object)
            list(keys)
            values = jsified_values(json_object)
            list(values)
            items = jsified_items(json_object)
            list(items)

            # UNDEFINED
            json_object = jsify(self.test_dict)
            Undefined
            json_object.not_defined_property
            json_object.not_defined_property.fghjj.dsffsd['42']

            # ITERATOR
            Iterator(self.test_dict)
            Iterator(self.test_list)
            Iterator(self.test_tuple)
            Iterator(jsify(self.test_dict))
            Iterator(jsify(self.test_list))
            Iterator(jsify(self.test_tuple))

        for n in range(10):
            gc.collect()
            time.sleep(0.1)

        print(f"Start memory usage: {start_memory}\nFinal usage: {self.memory_usage()}")
        self.assertEqual(start_memory, self.memory_usage())

    def test_unjsify_deepcopy_mixed_nesting(self):
        """
        Test that unjsify_deepcopy handles nested and mixed jsified objects inside plain Python structures.
        """
        nested = {"deep": 123}
        jsified_nested = jsify(nested)
        original = {
            "plain": [1, 2, 3],
            "jsified_dict": jsified_nested,
            "mixed": [
                4,
                jsified_nested,
                {"plain_inner": jsified_nested}
            ]
        }
        wrapped = jsify(original)
        result = unjsify_deepcopy(wrapped)

        self.assertEqual(result["plain"], [1, 2, 3])
        self.assertEqual(result["jsified_dict"], {"deep": 123})
        self.assertEqual(result["mixed"][1], {"deep": 123})
        self.assertEqual(result["mixed"][2]["plain_inner"], {"deep": 123})
        self.assertIsNot(result, original)
        self.assertIsNot(result["jsified_dict"], nested)
        self.assertIsNot(result["mixed"][2]["plain_inner"], nested)
