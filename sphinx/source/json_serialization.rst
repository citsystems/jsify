.. _json_serialization:

Serializing `Object` Instances with JSON
============================================

The Jsify library provides seamless integration with Python's built-in `json` module, allowing you to serialize `Object` instances and other jsified structures into JSON format. This is achieved through the use of the `ObjectEncoder`, a custom JSON encoder that ensures `Object` instances are correctly converted back into their original Python representations before serialization.

**Key Concept: Custom JSON Encoding**

When you serialize a `Object`, `Dict`, `List`, or `Tuple` using the `json` module, the `ObjectEncoder` is automatically invoked to convert these instances into their underlying native Python objects (like dictionaries, lists, and tuples). This ensures that the resulting JSON is a standard representation of the data, free from any Jsify-specific attributes or behaviors.

**Basic Serialization Example:**

To serialize a `Object` to a JSON string, you can use the `json.dumps` function. This function will use `ObjectEncoder` to handle the conversion.

.. code-block:: python

    import json
    from jsify import jsify, Undefined

    # Example data
    data = {
        'name': 'Alice',
        'details': {
            'age': 30,
            'city': 'Wonderland'
        },
        'undef': Undefined
    }

    # Convert to a jsified object
    json_obj = jsify(data)

    # Serialize the jsified object to a JSON string
    json_string = json.dumps(json_obj)

    print(json_string)
    # Outputs: {"name": "Alice", "details": {"age": 30, "city": "Wonderland"}}
**Preserving Undefined Values:**

By default, the `dumps` and `dump` functions omit any fields that have the value `Undefined`. You can control this
behavior with the `omit_undefined` parameter. If omitting is disabled then Undefined values are replaced by `null`.

**Example**

.. code-block:: python

    # Serialize the jsified object to a JSON string preserving Undefined values
    json_string = json.dumps(json_obj, omit_undefined=False)

    print(json_string)
    # Outputs: {"name": "Alice", "details": {"age": 30, "city": "Wonderland"}, "undef": null}
.. _omit_undefined_usage:

When to Use the `omit_undefined` Feature
----------------------------------------

The `omit_undefined` feature in the Jsify library's JSON serialization process is particularly useful in scenarios where you need to maintain clean and concise JSON outputs by excluding fields that are not explicitly defined or have no meaningful value. This feature allows you to control whether fields with the `Undefined` value should be included in the final JSON output or omitted entirely.

Following are the sample scenarios for using `omit_undefined` feature:

1. **Interfacing with APIs:**

   When interacting with external APIs, it's often important to only send fields that have been explicitly set. Including undefined or null-like fields can lead to unintended consequences, such as errors or misinterpretation by the receiving system. By omitting `Undefined` fields, you can ensure that your JSON payloads are lean and only include relevant data.

2. **Generating Clean Configuration Files:**

   When generating JSON-based configuration files, it's often desirable to exclude fields that have not been explicitly set, leaving out unnecessary defaults. This results in a cleaner and more maintainable configuration file that only includes relevant settings.

3. **Reducing Data Storage and Transmission Costs:**

   In scenarios where data is stored or transmitted frequently, minimizing the size of the JSON output can lead to significant cost savings. By omitting undefined fields, you can reduce the payload size, leading to lower storage requirements and faster data transmission.
