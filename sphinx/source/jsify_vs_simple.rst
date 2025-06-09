.. _jsify_vs_simple:

Jsify vs. Simplify: Two Ways of Dot Notation Access
===================================================

Jsify offers two distinct approaches for dot notation access to data loaded from JSON or similar sources:

1. **jsify:** Uses high-performance C extensions, wrapping objects for advanced, JavaScript-like attribute access (with `Undefined` support and mutation).
2. **simplify:** Converts dictionaries into Python’s standard `SimpleNamespace` for basic dot notation access, using pure Python.

**Comparison Table**

+---------------------+---------------------------------------+--------------------------------------+
| Feature             | jsify                                 | simplify (SimpleNamespace)           |
+=====================+=======================================+======================================+
| Performance         | Extremely fast (C extension);         | Fast (pure Python), but slower       |
|                     | ~2× slower than SimpleNamespace,      | than native dict access              |
|                     | but much more powerful                |                                      |
+---------------------+---------------------------------------+--------------------------------------+
| Dot notation        | Yes, for any level of nesting         | Yes, for dicts; recursive on load    |
+---------------------+---------------------------------------+--------------------------------------+
| Fallback for        | Returns `Undefined` (no exception)    | Raises AttributeError                |
| missing attributes  |                                       |                                      |
+---------------------+---------------------------------------+--------------------------------------+
| Mutation support    | Fully supports setting and deleting   | You can set new attributes, but      |
|                     | items/attributes (syncs with dict)    | doesn't sync with underlying dict    |
+---------------------+---------------------------------------+--------------------------------------+
| Type preservation   | Keeps reference to original object    | Converts dicts only; lists/tuples    |
|                     | (no deep copy)                        | remain native                        |
+---------------------+---------------------------------------+--------------------------------------+
| Compatibility       | API feels like JavaScript             | Standard Python (`types.SimpleNamespace`)|
+---------------------+---------------------------------------+--------------------------------------+
| Serialization       | Custom JSON encoder for jsify objects | Standard JSON encoding, but may      |
|                     |                                       | lose some type info                  |
+---------------------+---------------------------------------+--------------------------------------+
| Error handling      | Safe for any depth, robust to         | AttributeError for missing keys;     |
|                     | unexpected/missing data               | can break if structure is irregular  |
+---------------------+---------------------------------------+--------------------------------------+

**When to use jsify:**
- You need high performance and advanced attribute access, especially for complex/nested data.
- You want JavaScript-like `Undefined` instead of exceptions on missing fields.
- You work with APIs, configs, or unpredictable structures.
- You care about mutating the data (bi-directional sync with the original object).

**When to use simplify:**
- You want basic dot notation for simple, read-mostly JSON data.
- You don’t need custom error handling or `Undefined` behavior.
- You prefer pure Python, or are working in constrained environments.

**Example: Using Simplify**

.. code-block:: python

    from jsify.simplified import loads_simplified

    data = loads_simplified('{"a": 1, "b": {"c": 2}}')
    print(data.a)        # 1
    print(data.b.c)      # 2
    print(data.z)        # raises AttributeError

**Example: Using Jsify**

.. code-block:: python

    from jsify import jsify, Undefined

    obj = jsify({"a": 1, "b": {"c": 2}})
    print(obj.a)         # 1
    print(obj.b.c)       # 2
    print(obj.z)         # Undefined (no exception)

---

**Summary:**
- Use **jsify** for robustness, speed, and JavaScript-like handling.
- Use **simplify** for simple, standard Python dot access with `SimpleNamespace`.

