.. _json_serialization:

Serializing `JsonObject` Instances with JSON
============================================

The Jsify library provides seamless integration with Python's built-in `json` module, allowing you to serialize `JsonObject` instances and other jsified structures into JSON format. This is achieved through the use of the `JsonObjectEncoder`, a custom JSON encoder that ensures `JsonObject` instances are correctly converted back into their original Python representations before serialization.

**Key Concept: Custom JSON Encoding**

When you serialize a `JsonObject`, `JsonDict`, `JsonList`, or `JsonTuple` using the `json` module, the `JsonObjectEncoder` is automatically invoked to convert these instances into their underlying native Python objects (like dictionaries, lists, and tuples). This ensures that the resulting JSON is a standard representation of the data, free from any Jsify-specific attributes or behaviors.

**Basic Serialization Example:**

To serialize a `JsonObject` to a JSON string, you can use the `json.dumps` function. This function will use `JsonObjectEncoder` to handle the conversion.

.. code-block:: python

    import json
    from jsify import jsify

    # Example data
    data = {
        'name': 'Alice',
        'details': {
            'age': 30,
            'city': 'Wonderland'
        }
    }

    # Convert to a jsified object
    json_obj = jsify(data)

    # Serialize the jsified object to a JSON string
    json_string = json.dumps(json_obj)

    print(json_string)
    # Outputs: {"name": "Alice", "details": {"age": 30, "city": "Wonderland"}}
