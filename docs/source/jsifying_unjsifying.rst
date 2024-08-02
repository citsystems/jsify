.. _jsify:

Jsifying and unjsyfing objects
===========================

The `jsify` and `unjsify` functions are key utilities for converting between standard Python data structures and `JsonObject` instances within the library. These functions enable smooth integration of Python's native types with the JSON-like behavior provided by `JsonObject`, allowing for flexible and dynamic data manipulation.

`jsify`
-------

The `jsify` function converts standard Python objects such as dictionaries, lists, and tuples into their corresponding `JsonObject` representations. This conversion enables attribute-style access and other JSON-like features, making it easier to work with complex nested data structures.

**Usage Example:**

.. code-block:: python

    from jsify import jsify

    # Convert a dictionary into a JsonObject
    data = {'key1': 'value1', 'key2': {'nestedKey': 'nestedValue'}}
    json_obj = jsify(data)

    # Access nested elements using attribute-style access
    print(json_obj.key2.nestedKey)  # Outputs: nestedValue

**Parameters:**

- ``o`` : The object to convert, which can be of type ``dict``, ``list``, ``tuple``, or any other object.
- ``kwargs`` : Additional keyword arguments to customize the conversion.

**Returns:**

- A `JsonObject`, `JsonDict`, `JsonList`, or `JsonTuple`, depending on the type of the input object.

`unjsify` and `deep_unjsify`
---------

The `unjsify` function converts a `JsonObject` back into its original Python representation, such as a dictionary, list, or tuple. This function is useful when you need to serialize or process the data in its native form after manipulating it using the JSON-like interface.

**Usage Example:**

.. code-block:: python

    from jsify import unjsify

    # Assuming json_obj is a JsonObject
    original_data = unjsify(json_obj)

    # The original_data is now a standard Python dictionary
    print(original_data)  # Outputs: {'key1': 'value1', 'key2': {'nestedKey': 'nestedValue'}}

**Parameters:**

- ``obj`` : The `JsonObject` to convert back into its original form.

**Returns:**

- The original object if ``obj`` is a `JsonObject`, otherwise returns the object unchanged.

**Deep unjsifying:**

In scenarios where you have nested `JsonObject` instances and want to deeply convert them back to their original Python structures, the `deep_unjsify` function can be used. It performs a recursive unjsification, ensuring that all nested `JsonObject` instances are properly converted.
This function is particularly useful in scenarios where you have complex, deeply nested JSON-like objects that need to be converted back to standard Python types, such as dictionaries, lists, and tuples, for further processing or serialization.


**Using `deep_unjsify`:**

.. code-block:: python

    from jsify import jsify, deep_unjsify

    # Complex deeply jsified structure
    json_obj = jsify({
        'level1': jsify({
            'level2': jsify({
                'level3': 'value'
            }),
            'level2_list': [
                {'nested_key': 'nested_value'},
                {'another_key': 'another_value'}
            ]
        })
    })

    # Accessing elements in a JSON-like manner
    print(json_obj.level1.level2.level3)  # Outputs: value
    print(json_obj.level1.level2_list[0].nested_key)  # Outputs: nested_value

    # Now, deeply unjsify the JsonObject back to its original form
    original_data = deep_unjsify(json_obj)

    # Verify the structure
    print(original_data)

**Expected Output:**

As a result, the `original_data` object should consist of native `dict` and `list` instance objects.

.. code-block:: python

    {
        'level1': {
            'level2': {
                'level3': 'value'
            },
            'level2_list': [
                {'nested_key': 'nested_value'},
                {'another_key': 'another_value'}
            ]
        }
    }

By utilizing the `jsify` and `unjsify` functions, developers can easily switch between Python's native data types and the enhanced JSON-like structures provided by the library, facilitating more flexible and intuitive data manipulation.
