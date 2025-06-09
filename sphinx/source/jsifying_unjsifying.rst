.. _jsifying_and_unjsifying:

.. meta::
   :keywords: Jsify, Python, jsify, jsified_copy, jsified_deepcopy, unjsify, unjsify_deepcopy, dejsify, Object, Dict, List, Tuple, JSON, data structures, attribute access, dot notation, serialization, data conversion, shallow copy, deep copy, unwrap, wrapper
   :description: Comprehensive overview of Jsify's core conversion and copy functions: jsify, jsified_copy, jsified_deepcopy, unjsify, unjsify_deepcopy, and dejsify. Learn how to wrap, copy, and convert between native Python types and Jsify objects with dot notation and full JSON-like access.

Jsifying and unjsifying the objects
------------------------------------

Jsify provides a set of key functions for converting, copying, and unwrapping Jsify-wrapped objects and standard Python data types:

**1. jsify**

Wraps a Python object (dict, list, tuple, etc.) as a Jsify object for dot-style attribute access and dynamic manipulation.

- Returns a Jsify wrapper: `Object`, `Dict`, `List`, or `Tuple`.
- Deep/nested wrapping is **lazy**: only the top-level object is wrapped; deeper elements are wrapped automatically on attribute or item access.
- **Typical usage:** It's usually enough to call `jsify` on the top-level object—nested access will always work seamlessly.

**Example:**

.. code-block:: python

    data = {'user': {'name': 'Alice', 'info': {'age': 30}}}
    obj = jsify(data)
    print(obj.user.info.age)  # Outputs: 30

**2. jsified_copy**

Returns a shallow Jsify-wrapped copy of the object.

- Performs a shallow copy of the original data (only the outermost container is new).
- The result is again Jsify-wrapped.
- Inner mutable objects (like lists, dicts) are **not** copied.

**Example:**

.. code-block:: python

    obj = jsify({'x': [1, 2]})
    c = jsified_copy(obj)
    # c is a new Jsify wrapper, c.x is the *same* list as obj.x

**3. jsified_deepcopy**

Returns a deep Jsify-wrapped copy of the object.

- Recursively deep-copies the original data.
- Result is a Jsify-wrapped structure with no shared mutable references at any level.

**Example:**

.. code-block:: python

    obj = jsify({'x': [1, 2]})
    d = jsified_deepcopy(obj)
    # d is a new Jsify wrapper, d.x is a *new* list, independent from obj.x

**4. unjsify**

Returns the original Python object from a Jsify wrapper.

- Only the top-level Jsify object is unwrapped.
- Nested objects are usually already plain Python types because Jsify wraps only on access.
- In most real cases, a single call to `unjsify` will recover the full, deeply-native structure.

**Example:**

.. code-block:: python

    obj = jsify({'a': {'b': 1}})
    result = unjsify(obj)
    # result == {'a': {'b': 1}}

**5. unjsify_deepcopy**

Returns a *deep copy* of the object with all Jsify wrappers removed.

- Deeply unwraps and copies the data.
- The output is a completely new native structure.

**Example:**

.. code-block:: python

    obj = jsify({'a': {'b': 1}})
    result = unjsify_deepcopy(obj)
    # result == {'a': {'b': 1}} (no Jsify wrappers anywhere, all data is copied)

**6. dejsify**

Recursively replaces all Jsify objects with their underlying values, *in-place*, without making a copy.

- The structure is modified so every Jsify wrapper becomes its underlying Python value.
- No new containers (dicts/lists) are created—just substitution.

**Example:**

.. code-block:: python

    obj = jsify({'a': {'b': 1}})
    result = dejsify(obj)
    # result is the same structure as obj, but all Jsify wrappers are replaced by plain types

**Summary Table**

+------------------------+------------------------------+-----------------------------------------------+
| Function               | Recursion Depth              | Copy or In-place / Wrap or Unwrap             |
+========================+==============================+===============================================+
| jsify                  | Top-level only (lazy nested) | No copy, wraps for dot access                 |
+------------------------+------------------------------+-----------------------------------------------+
| jsified_copy           | Top-level only               | Shallow copy, wrap                            |
+------------------------+------------------------------+-----------------------------------------------+
| jsified_deepcopy       | Deep (recursive)             | Deep copy, wrap                               |
+------------------------+------------------------------+-----------------------------------------------+
| unjsify                | Top-level only               | No copy, unwrap                               |
+------------------------+------------------------------+-----------------------------------------------+
| unjsify_deepcopy       | Deep (recursive)             | Deep copy, unwrap                             |
+------------------------+------------------------------+-----------------------------------------------+
| dejsify                | Deep (recursive)             | In-place, unwrap                              |
+------------------------+------------------------------+-----------------------------------------------+

**Note:** For most applications, you only need to call `jsify` on your top-level object; dot-style access and lazy wrapping will just work for all nested content.
