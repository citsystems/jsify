.. _using_dictionaries:

.. meta::
   :keywords: Jsify, Python, dictionaries, jsified dictionaries, Dict, JSON-like objects, attribute access, data manipulation, dictionary functions, JSON-like behavior
   :description: Learn how to use jsified dictionaries in the Jsify library. This guide explains how to convert Python dictionaries into Jsify Dict instances for attribute-style access, and details the use of standalone functions to manipulate these dictionaries while avoiding naming collisions.

Using Jsified Dictionaries
==========================

The Jsify library allows you to work with dictionaries in a more flexible and dynamic way by converting them into `Dict` instances, which are specialized versions of `Object`. These jsified dictionaries enable attribute-style access to their keys and provide a more intuitive interface for manipulating nested data structures. However, to avoid potential naming collisions that could arise from adding methods directly to these JSON-like objects, some dictionary manipulation functions are implemented separately as standalone functions rather than as methods of `Dict`.

**Creating and Using Jsified Dictionaries:**

To create a jsified dictionary, you can use the `jsify` function, which converts a standard Python dictionary into a `Dict`. This allows you to access dictionary keys as if they were attributes of an object.

**Example:**

.. code-block:: python

    from jsify import jsify

    # Standard Python dictionary
    data = {
        'name': 'Alice',
        'details': {
            'age': 30,
            'city': 'Wonderland'
        }
    }

    # Convert to a jsified dictionary
    json_dict = jsify(data)

    # Accessing keys using attribute-style access
    print(json_dict.name)  # Outputs: Alice
    print(json_dict.details.age)  # Outputs: 30

    # Accessing nested dictionary keys with the same ease
    print(json_dict.details.city)  # Outputs: Wonderland

**Handling Dictionary Manipulations:**

While `Dict` provides an intuitive way to access and modify dictionary data, certain dictionary operations are implemented as separate functions. This design choice is intentional to avoid naming collisions in JSON-like data, where keys might have the same names as methods, potentially causing unexpected behavior.

**Standalone Dictionary Manipulation Functions:**

The library includes several standalone functions for common dictionary operations that would traditionally be methods in a regular Python dictionary:

- **jsified_copy:** Creates a shallow copy of a `Dict`.
- **jsified_get:** Retrieves a value for a specified key, with support for a default value if the key is not found.
- **jsified_update:** Updates the dictionary with key-value pairs from another dictionary.
- **jsified_values, jsified_keys, jsified_items:** Functions that return views of the dictionary’s values, keys, and items, respectively.

**Example:**

.. code-block:: python

    from jsify import jsified_copy, jsified_get, jsified_update

    # Example jsified dictionary
    json_dict = jsify({'key1': 'value1', 'key2': 'value2'})

    # Copying the dictionary
    copied_dict = jsified_copy(json_dict)
    print(copied_dict)  # Outputs a copy of the jsified dictionary

    # Using jsified_get to safely access a key
    value = jsified_get(json_dict, 'key1', 'default_value')
    print(value)  # Outputs: value1

    # Updating the dictionary with new key-value pairs
    jsified_update(json_dict, {'key3': 'value3'})
    print(json_dict.key3)  # Outputs: value3

**Why Separate Functions?**

In JSON-like data structures, it's crucial to avoid method naming collisions. For example, if a dictionary key were named "get", it could conflict with a `get` method, leading to unexpected behavior. By implementing operations like `get`, `update`, and `copy` as standalone functions, Jsify maintains the integrity of JSON-like data while still providing the functionality needed to manipulate dictionaries effectively.

This approach ensures that you can safely work with keys that might otherwise clash with common method names, allowing for a more consistent and predictable experience when handling JSON-like data in Python.

.. _views_functions:

**Using View Functions with Jsified Dictionaries**

The Jsify library provides standalone functions for retrieving views of a `Dict`'s keys, values, and items
(`jsified_keys`, `jsified_values`, and `jsified_items`), similar to the standard dictionary methods in Python.
These functions return a `Iterator`, which allows for iteration over the results while maintaining the JSON-like
behavior of the data.

**Example of Usage:**

Consider the following example where we work with a jsified dictionary and use the view functions:

.. code-block:: python

    from jsify import jsify, jsified_keys, jsified_values, jsified_items

    # Example jsified dictionary
    json_dict = jsify({
        'name': 'Alice',
        'age': 30,
        'city': 'Wonderland'
    })

    # Getting a view of the keys
    keys_view = jsified_keys(json_dict)
    for key in keys_view:
        print(key)  # Outputs: 'name', 'age', 'city'

    # Getting a view of the values
    values_view = jsified_values(json_dict)
    for value in values_view:
        print(value)  # Outputs: 'Alice', 30, 'Wonderland'

    # Getting a view of the items (key-value pairs)
    items_view = jsified_items(json_dict)
    for key, value in items_view:
        print(f'{key}: {value}')
        # Outputs:
        # name: Alice
        # age: 30
        # city: Wonderland

**Remark on `Iterator` Result:**

The view functions `jsified_keys`, `jsified_values`, and `jsified_items` return a `Iterator`, which is an iterator
specifically designed to work with JSON-like objects in the Jsify library. `Iterator` preserves the JSON-like
behavior during iteration, meaning that if you access elements of the iterator, they retain their `Object`
characteristics.

This is particularly useful when working with nested structures, as you can iterate over keys, values, or items and
still access deeply nested data using attribute-style access or other JSON-like operations.

**Example:**

.. code-block:: python

    nested_dict = jsify({
        'user1': {
            'name': 'Bob',
            'details': {
                'age': 25,
                'city': 'Metropolis'
            }
        },
        'user2': {
            'name': 'Alice',
            'details': {
                'age': 30,
                'city': 'Warsaw'
            }
        }
    })

    # Iterating over nested keys
    user_keys = jsified_keys(nested_dict.user1.details)
    for key in user_keys:
        print(key)  # Outputs: 'age', 'city'

    # Accessing nested values during iteration
    for value in jsified_values(nested_dict):
        print(f'{value.name} of age {value.details.age}')
    # Outputs: 'Bob of age 25', 'Alice of age 30'

    # Accessing nested items during iteration
    for key, value in jsified_items(nested_dict):
        print(f'{key}: {value.name} of age {value.details.age}')
    # Outputs: 'user1: Bob of age 25', 'user2: Alice of age 30'

The use of `Iterator` ensures that even as you iterate over the elements of a `Dict`, you maintain the ability to interact with the data in a JSON-like manner. This seamless integration of iteration and JSON-like behavior makes the Jsify library particularly powerful when dealing with complex and nested data structures.
