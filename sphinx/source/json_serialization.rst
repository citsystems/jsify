.. _json_serialization:

.. meta::
   :keywords: Jsify, Python, JSON serialization, ObjectEncoder, jsify, unjsify, custom JSON encoder, undefined values, omit_undefined, data serialization
   :description: Learn how to serialize Jsify Object instances and other jsified structures into JSON format using custom encoders. This guide covers the use of ObjectEncoder, handling undefined values, and controlling the serialization process with the omit_undefined feature.

Serializing `Object` Instances with JSON
========================================

The Jsify library provides seamless integration with Python's JSON ecosystem via dedicated serialization functions: ``jsified_dump`` and ``jsified_dumps``. You **must always use** these functions to serialize ``Object`` instances or any jsified structure. Direct use of Python's built-in ``json.dump`` or ``json.dumps`` **will not work** for Jsify objects.

**Key Concept: Custom JSON Encoding**

When you serialize a ``Object``, ``Dict``, ``List``, or ``Tuple`` using ``jsified_dump`` or ``jsified_dumps``, the library ensures that all Jsify instances are converted to their underlying Python types (such as dictionaries, lists, and tuples) before serialization. The output is clean JSON without any Jsify-specific attributes.

**Basic Serialization Example:**

To serialize a ``Object`` to a JSON string, always use ``jsified_dumps``:

.. code-block:: python

    from jsify import jsify, jsified_dumps, Undefined

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
    json_string = jsified_dumps(json_obj)

    print(json_string)
    # Outputs: {"name": "Alice", "details": {"age": 30, "city": "Wonderland"}}

**Controlling the Handling of Undefined Values**

By default, ``jsified_dump`` and ``jsified_dumps`` omit any fields with the value ``Undefined`` from the output. You can control this behavior with the ``omit_undefined`` parameter—set ``omit_undefined=False`` to serialize ``Undefined`` fields as ``null``.

**Example:**

.. code-block:: python

    # Serialize the jsified object to a JSON string, preserving Undefined as null
    json_string = jsified_dumps(json_obj, omit_undefined=False)

    print(json_string)
    # Outputs: {"name": "Alice", "details": {"age": 30, "city": "Wonderland"}, "undef": null}

.. _omit_undefined_usage:

When to Use the ``omit_undefined`` Feature
------------------------------------------

The ``omit_undefined`` parameter is useful when you want to exclude or preserve fields with ``Undefined`` values in your JSON output.

Typical scenarios:

1. **Interfacing with APIs:** Ensure payloads only contain explicitly set fields.
2. **Clean Configuration Files:** Exclude unset/default fields for readability.
3. **Reducing Data Size:** Smaller JSON outputs save bandwidth and storage.

**Summary:**
Always use ``jsified_dump`` and ``jsified_dumps`` for JSON serialization of Jsify objects. Direct use of Python’s ``json.dump`` or ``json.dumps`` will fail or produce incorrect results.
