Dict
====

Overview
--------

:class:`jsify.Dict` is the jsified wrapper for Python dictionaries, created by passing any dict (or dict-containing structure) to :func:`jsify`.

**Key features:**

- **Dot-style attribute access** for all keys (even deeply nested).
- **Bracket/item access:** `obj['key']` works as expected.
- **Most standard dict operations via helpers:** see "Dict Methods" and :doc:`dict_functions` for details.
- **Mutable and reference-based:** changes are always reflected in the original data and vice versa, including all nested containers.
- **Safe chaining:** missing attributes/keys always return ``Undefined``, never raise `KeyError` or `AttributeError`.
- **Consistent interface:** all nested dicts/lists are jsified recursively, changing their type and adding dot-access and chaining.
- **Iteration returns a :class:`jsify.Iterator`** that supports Python and JavaScript-like iteration semantics.

.. warning::

   Jsified ``Dict`` objects do *not* provide most standard dict methods as direct attributes (e.g., ``obj.items()`` or ``obj.copy()`` will not work).
   Instead, use the corresponding ``jsified_*`` helper functions.
   If a key matches a dict method name (e.g., ``"items"``, ``"get"``), the key always takes priority and the method is unavailable by attribute.
   For native type methods, use ``unjsify(obj)`` to obtain a standard dict.

Creating a Jsified Dict
-----------------------

.. code-block:: python

   from jsify import jsify

   d = {"a": 1, "b": {"c": 2}, "arr": [1, 2]}
   obj = jsify(d)

   print(type(obj))       # <class 'jsify.Dict'>
   print(type(obj.b))     # <class 'jsify.Dict'>
   print(type(obj.arr))   # <class 'jsify.List'>

.. note::

   All nested dicts and lists will be jsified recursively.
   Their type and interface change to support dot/item access, safe chaining, and JavaScript-like behaviors.
   Use ``unjsify(obj)`` if you need a raw Python dict or list.

Accessing Elements
------------------

- Use dot access: ``obj.a``
- Use item (bracket) access: ``obj["a"]``
- Both work at any depth; all nested dicts/lists are jsified

.. code-block:: python

   print(obj.a)          # 1
   print(obj["a"])       # 1
   print(obj.b.c)        # 2
   print(obj["b"]["c"])  # 2

   # Lists inside dicts are jsified:
   print(obj.arr[1])     # 2
   print(type(obj.arr))  # <class 'jsify.List'>

   # Safe for missing keys/attributes (never raises):
   print(obj.nope)       # Undefined
   print(obj["nope"])    # Undefined

.. important::

   Dot-style attribute access **never raises** for missing keys—missing attributes always return ``Undefined``.
   This enables safe chaining, e.g., ``obj.not_here.foo.bar`` is valid and always returns ``Undefined``.

   If a dict key matches a Python dict method name (e.g., ``"items"``, ``"get"``, etc.), dot-access returns the key’s value, **not** the method.
   Dict methods are not available as attributes if shadowed.

Iteration
---------

- Iterating over a :class:`jsify.Dict` returns a :class:`jsify.Iterator`.
- The iterator supports Python and JavaScript-like iteration semantics.

.. code-block:: python

   it = iter(obj)
   print(type(it))  # <class 'jsify.Iterator'>

   for key in it:
       print(key)

Standard Dict Methods
---------------------

:class:`jsify.Dict` supports **most standard Python dict operations** via helper functions in the jsify package.
Classic methods like ``items()``, ``keys()``, ``values()``, etc. are **not** available directly on jsified objects—use helpers:

- ``jsified_items(obj)`` – Returns a jsified list of (key, value) pairs
- ``jsified_keys(obj)`` – Returns a jsified list of keys
- ``jsified_values(obj)`` – Returns a jsified list of values
- ``jsified_update(obj, other)`` – Updates the dict in place
- ``jsified_get(obj, key, default=None)`` – Safe get with default
- ``jsified_setdefault(obj, key, default)`` – Set default value if missing
- ``jsified_pop(obj, key[, default])`` – Pop a key
- ``jsified_popitem(obj)`` – Remove and return a (key, value) pair

See :doc:`dict_functions` for all available helpers and full documentation.

.. code-block:: python

   from jsify import (
       jsified_items, jsified_keys, jsified_values,
       jsified_update, jsified_get, jsified_setdefault,
       jsified_pop, jsified_popitem
   )

   obj = jsify({"x": 1, "y": 2})

   print(list(jsified_keys(obj)))    # ['x', 'y']
   print(list(jsified_values(obj)))  # [1, 2]
   print(list(jsified_items(obj)))   # [('x', 1), ('y', 2)]

   jsified_update(obj, {"z": 3})
   print(obj.z)     # 3

   print(jsified_get(obj, "x"))     # 1
   jsified_pop(obj, "x")
   print(obj.x)     # Undefined

   jsified_setdefault(obj, "w", 99)
   print(obj.w)     # 99

   k, v = jsified_popitem(obj)
   print(f"Removed: {k}={v}")

Reference Behavior
------------------

- All changes to the jsified dict **and its nested elements** are reflected in the original Python dict, and vice versa.
- Mutations are always reference-based: editing any nested dict/list structure via a jsified object mutates the original.
- Assigning a jsified object as a value in a dict keeps it jsified (see deep unjsify in :doc:`jsify_unjsify` if you want to convert back to native types everywhere).

Limitations and Gotchas
-----------------------

- All mutation operations (assignment, pop, update, etc.) directly affect the original data, recursively for all contained structures.
- When unjsifying, only the top-level dict becomes native unless you use ``unjsify_deepcopy`` (see :doc:`jsify_unjsify`).
- Classic dict methods (such as ``copy``, ``clear``, ``fromkeys``, etc.) are **not** available as direct methods.
  Use provided helper functions for supported operations, or unjsify to access native methods.
- Type checks with ``isinstance(obj, dict)`` or ``type(obj) is dict`` will **not work**—jsified objects are not standard dicts/lists/tuples.
  Use ``unjsify(obj)`` for such checks.
- If your keys clash with dict method names (e.g., ``obj.items``), the key always takes priority; use the helper function for the classic method.

See Also
--------

- :doc:`dict_functions` for full documentation of dict utilities and helpers
- :doc:`list` for jsified lists
- :doc:`tuple` for jsified tuples
- :doc:`jsify_unjsify` for conversion, reference rules, and copying
- :class:`jsify.Iterator` for iterators returned by dicts and other containers
