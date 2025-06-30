Introduction
============

.. _introduction:

Welcome to **jsify** – a Python library with a blazing fast C extension that brings JavaScript-like dot access, lazy dynamic wrapping, and safe deep data handling to your nested structures. jsify is designed for complex, unpredictable, or deeply nested JSON and Python data, delivering high performance for common dynamic access patterns.

.. note::

   This library uses a C extension for ultra-fast access to your data structures.

Contents
--------

- :ref:`concepts`
  - :ref:`simplifiedobject`
  - :ref:`jsifyobjects`
  - :ref:`undefined`
- :ref:`advantages`
  - :ref:`why-simplifiedobject`
  - :ref:`why-jsify`
  - :ref:`no-key-conflicts`

.. _concepts:

Concepts
========

Key Object Types: SimplifiedObject vs jsify objects
---------------------------------------------------

jsify provides two main dynamic wrappers:

- ``SimplifiedObject``: For simple dot-access with missing-attribute safety, modeled after Python's ``SimpleNamespace``.
- ``jsify`` wrappers (``Object``, ``Dict``, ``List``, etc): For deep, JavaScript-style dot/item access and automatic lazy wrapping.

You can use either approach depending on your requirements. See below for precise behaviors.

.. _simplifiedobject:

SimplifiedObject: Simple & Safe Dot Access
------------------------------------------

A ``SimplifiedObject`` is like an improved ``SimpleNamespace``:

- Dot access for every key—missing attributes return ``Undefined`` instead of raising errors.
- Only the top-level dict is converted by default; nested dicts remain dicts unless you recursively wrap or use ``loads_simplified`` with an object hook to convert all levels.

**Example:**

.. code-block:: python

   from jsify.simplify import loads_simplified, Undefined

   data = '{"user": {"profile": null}}'
   obj = loads_simplified(data)

   # Works: user exists (SimplifiedObject), profile is None (no error).
   if obj.user.profile is None:
       print("No profile")

   # If 'profile' is a dict and you want further dot access,
   # use loads_simplified on nested dicts as needed.

Missing attributes on a ``SimplifiedObject`` always return ``Undefined``—not errors. However, deep safe chaining only works for dicts converted to ``SimplifiedObject``.

**Another Example:**

.. code-block:: python

   data = '{"a": 1, "b": 2}'
   obj = loads_simplified(data)
   print(obj.a)  # 1
   print(obj.z)  # <Undefined>, no error

   # If obj.b is a dict, you must wrap it for dot access on its keys.

.. _jsifyobjects:

jsify Objects: Advanced Dynamic Wrapping
----------------------------------------

``jsify`` turns dicts, lists, or tuples (even deeply nested) into JavaScript-style objects:

- **Blazing fast:** Built on a C extension for top performance.
- **Lazy wrapping:** Only wraps as you access, not eagerly.
- **Reflects changes** in the original structure; wrappers are views, not copies.
- **Supports both dot and item access**, just like in JavaScript.

**Example:**

.. code-block:: python

   from jsify import jsify

   data = {"settings": {"theme": "dark"}, "items": [1, 2, 3]}
   obj = jsify(data)

   # Dot access
   print(obj.settings.theme)    # "dark"
   # List access
   print(obj.items[1])          # 2

   # Changes in the original dict are reflected in the wrapper
   data["settings"]["theme"] = "light"
   print(obj.settings.theme)    # "light"

**Nested mutation example:**

.. code-block:: python

   orig = {"foo": {"bar": 1}}
   o = jsify(orig)
   print(o.foo.bar)    # 1
   orig["foo"]["bar"] = 2
   print(o.foo.bar)    # 2

.. _undefined:

Undefined: Error-Free Access for Missing Keys
---------------------------------------------

``Undefined`` is a special singleton returned for any missing key or attribute on jsify wrappers or ``SimplifiedObject``. It behaves like JavaScript's ``undefined``:

- All missing keys/attributes return ``Undefined`` when accessed on a jsify or SimplifiedObject wrapper.
- ``Undefined`` is safe to chain: any attribute/item access on it yields itself, and it is falsy in boolean checks.
- Note: You must use ``jsify()`` or ``loads_simplified()`` to get this behavior; plain dict/list/tuple will not auto-return ``Undefined``.

**Example:**

.. code-block:: python

   wrapped = jsify({"user": {}})
   print(wrapped.user.profile.email)  # <Undefined>, never raises error

   if wrapped.user.profile.email is Undefined:
       print("Email not available")

**Boolean check:**

.. code-block:: python

   if not wrapped.user.notexisting.anything:
       print("No value!")  # This line executes because Undefined is falsy

.. _advantages:

Advantages
==========

.. _why-simplifiedobject:

Why SimplifiedObject?
---------------------

- Never raises exceptions for missing attributes—returns ``Undefined``.
- Cleaner code: no need for multiple checks or try/except blocks.
- Instantly converts JSON/dict to dot-access objects for convenient use.
- Can be used with the ``object_hook`` to recursively wrap dicts from JSON.

See example above at :ref:`simplifiedobject`.

.. _why-jsify:

Why jsify?
----------

- **Blazing fast C extension:** Efficient even with very large or deeply nested data.
- **Lazy and reference-based:** You see changes live, as objects are mutated.
- **Handles all nestings:** Works for dicts, lists, tuples, and deep chains.
- **Safe chaining:** Missing paths never error—just return ``Undefined``.
- **JSON (de)serialization:** Can automatically omit or include ``Undefined`` values.

See example above at :ref:`jsifyobjects`.

**Example: Serialization**

.. code-block:: python

   from jsify.json import jsified_dumps, Undefined
   obj = jsify({"a": 1, "b": None, "c": Undefined})
   print(jsified_dumps(obj))                  # {"a": 1, "b": null}
   print(jsified_dumps(obj, omit_undefined=False))  # {"a": 1, "b": null, "c": null}

.. _no-key-conflicts:

No Key Conflicts
----------------

- Your data’s keys always take priority (e.g., ``obj.items`` gives the value of ``"items"`` in your dict, not the method).
- Use helper functions for classic methods: ``jsified_items(obj)``, ``jsified_update(obj, data)``, etc.
- Or unwrap with ``unjsify(obj)`` to get back the original dict and standard methods.

**Example:**

.. code-block:: python

   from jsify import jsify, jsified_items, unjsify

   data = {"items": "DATA"}
   obj = jsify(data)

   print(obj.items)                 # "DATA" (your dict value)
   print(list(jsified_items(obj)))  # dict items, e.g. [("items", "DATA")]

   # Or get classic dict methods:
   orig = unjsify(obj)
   print(list(orig.items()))        # [('items', 'DATA')]

**Example: Key masking built-ins**

.. code-block:: python

   data = {"update": "NOT_A_METHOD"}
   obj = jsify(data)
   print(obj.update)   # "NOT_A_METHOD"
   # Still call classic update via helper:
   from jsify import jsified_update
   jsified_update(obj, {"x": 5})
   print(obj.x)  # 5

----

:doc:`Next: Installation <installation>`
