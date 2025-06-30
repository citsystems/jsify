Dict Functions
==============

Overview
--------

Jsified Dicts support **all standard Python dict operations** using helper functions from the ``jsify`` package.
These helpers provide classic dict behavior even if a key shadows a method name (e.g., ``obj.items`` is a value, not a method).
**All helpers accept both jsified and plain Python dicts, always returning jsified types** (not built-in Python objects).

Use these helpers for safe, predictable access and manipulation of any :class:`jsify.Dict` or plain ``dict`` object.

Helper Functions
----------------

All functions take a jsified dict or plain dict as the first argument, and always return jsified wrappers (`jsify.List`, `jsify.Tuple`, or jsified values).

**jsified_items(obj)**
   - Returns a jsified list of (key, value) pairs.

   .. code-block:: python

      from jsify import jsify, jsified_items

      obj = jsify({"a": 1, "b": 2})
      for k, v in jsified_items(obj):
          print(k, v)   # a 1   b 2

**jsified_keys(obj)**
   - Returns a jsified list of keys.

   .. code-block:: python

      from jsify import jsified_keys
      print(list(jsified_keys(obj)))  # ['a', 'b']

**jsified_values(obj)**
   - Returns a jsified list of values.

   .. code-block:: python

      from jsify import jsified_values
      print(list(jsified_values(obj)))  # [1, 2]

**jsified_update(obj, other)**
   - Updates the dict in place with key-value pairs from another mapping or iterable. Modifies the underlying object and returns None.

   .. code-block:: python

      from jsify import jsified_update
      jsified_update(obj, {"c": 3})
      print(obj.c)  # 3

**jsified_get(obj, key, default=None)**
   - Returns the value for `key` if present, else `default`. The return value is jsified unless it is a primitive type.

   .. code-block:: python

      from jsify import jsified_get
      print(jsified_get(obj, "z", default=123))  # 123

**jsified_setdefault(obj, key, default)**
   - If key is in the dict, returns its value (jsified). If not, inserts key with `default` and returns `default` (jsified). `default` is required.

   .. code-block:: python

      from jsify import jsified_setdefault
      print(jsified_setdefault(obj, "q", 42))  # 42

**jsified_pop(obj, key, default=None)**
   - Removes `key` and returns its value (jsified), or `default` if key not found.

   .. code-block:: python

      from jsify import jsified_pop
      print(jsified_pop(obj, "q", default=123))  # 42

**jsified_popitem(obj)**
   - Removes and returns a jsified tuple `(key, value)` pair.
   - Raises ``KeyError`` if the dict is empty.

   .. code-block:: python

      from jsify import jsified_popitem
      k, v = jsified_popitem(obj)
      print(f"Popped: {k}={v}")

Usage Notes
-----------

- All helpers operate directly on the original dict by reference.
- Return values are **jsified wrappers** (not built-in Python types), e.g., `jsify.List`, `jsify.Tuple`, or jsified values.
- These functions avoid problems with keys shadowing method names: ``obj.items`` is a key value, ``jsified_items(obj)`` is always the method.
- You can iterate over jsified lists and tuples as with standard Python types, but their type is not `list` or `tuple`.

Limitations
-----------

- Not all built-in dict methods (like ``fromkeys``, ``copy``, etc.) are wrapped; use classic dict conversion via ``unjsify_deepcopy`` if needed.
- **Return types are always jsified wrappers**, not Python built-ins. Use ``unjsify`` or ``unjsify_deepcopy`` to get plain Python objects if needed.
- Popping from an empty dict with ``jsified_popitem`` raises a ``KeyError`` (same as a normal dict).

See Also
--------

- :doc:`dict` for jsified dict interface, mutation, and reference rules
- :doc:`jsify_unjsify` for conversion and deep unjsify
