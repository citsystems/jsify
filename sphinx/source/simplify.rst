SimplifiedObject
================

.. currentmodule:: jsify.simplify

Overview
--------

``SimplifiedObject`` is a lightweight Python object that provides safe attribute-style (dot) access to nested data.
You can create it **directly with its constructor** or by loading JSON using :func:`loads_simplified` or :func:`load_simplified`.

Missing attributes **never raise errors**—they return the special ``Undefined`` object for safe, error-free deep access.

How to Create
-------------

You can create a ``SimplifiedObject`` in two ways:

**1. Directly from Python data:**

.. code-block:: python

   from jsify.simplify import SimplifiedObject, Undefined

   obj = SimplifiedObject(a=1, b=2, c={'x': 5})

   print(obj.a)         # 1
   print(obj.c['x'])    # 5 (if c is a dict)
   print(obj.missing)   # Undefined

**Note:** When created directly, nested dicts like `c` remain plain dicts and are not automatically converted to
``SimplifiedObject`` instances. Use :func:`loads_simplified` or :func:`load_simplified` for recursive conversion.

**2. By parsing JSON (auto-recursive conversion):**

.. code-block:: python

   from jsify.simplify import loads_simplified

   s = '{"user": {"profile": {}, "age": 25}}'  # Changed null to empty dict
   obj = loads_simplified(s)

   print(obj.user.age)          # 25
   print(obj.user.profile)      # SimplifiedObject({})
   print(obj.user.profile.foo)  # Undefined

   # All nested dicts become SimplifiedObject for full dot-access!

Deep Attribute Access and ``Undefined``
---------------------------------------

Any missing attribute at any depth returns the special ``Undefined`` object:

.. code-block:: python

   name = obj.user.profile.name
   if name is Undefined:
       print("Name is not available")

   # Deep chaining is always safe:
   print(obj.x.y.z)  # Always returns Undefined

Falsy and Comparison Behavior
-----------------------------

- ``Undefined`` is *falsy* in boolean context.
- It compares as equal to ``None``, but is not identical to ``None``.

.. code-block:: python

   if not obj.some.missing.attribute:
       print("Not present or falsy")

   assert obj.unknown is Undefined
   assert obj.unknown == None
   assert obj.unknown is not None

Serialization
-------------

Serialize ``SimplifiedObject`` instances to JSON using :func:`simplified_dumps` or :func:`simplified_dump`:

.. code-block:: python

   from jsify.simplify import simplified_dumps, simplified_dump

   d = SimplifiedObject(a=1, b=None, c=Undefined)
   print(simplified_dumps(d))
   # Outputs: {"a": 1, "b": null, "c": null}

   # Undefined attributes serialize as null.

   # To dump to a file:

   import io
   f = io.StringIO()
   simplified_dump(d, f)  # Correct argument order: object, file
   f.seek(0)
   print(f.read())

Working with Nested Structures and Recursive Dot Access
------------------------------------------------------

Nested dicts stay as dicts unless you wrap them.
**For recursive dot access at every depth**, you have two main options:

- **Manually nest SimplifiedObjects:**

  .. code-block:: python

     inner = SimplifiedObject(x=5)
     outer = SimplifiedObject(a=1, b=inner)
     print(outer.b.x)  # 5

  If you want lists of dot-access objects:

  .. code-block:: python

     obj = SimplifiedObject(items=[SimplifiedObject(x=1), SimplifiedObject(x=2)])
     print(obj.items[0].x)  # 1

- **Auto-recursive dot access:**

  For **automatic recursive wrapping** of all nested dicts and lists, use the Jsify Object system:

  .. code-block:: python

     from jsify.cjsify import jsify

     obj = jsify({'user': {'name': 'Alice', 'age': 30}})
     print(obj.user.name)  # Alice

Manual Construction Tips
------------------------

- You can pass any keyword arguments; they become attributes.
- You can assign new attributes after creation, but nested dicts remain plain dicts unless wrapped.

.. code-block:: python

   obj = SimplifiedObject(foo={'bar': 123})
   print(obj.foo['bar'])  # 123
   # But obj.foo is a dict, not a SimplifiedObject, unless you wrap it manually

Limitations and Gotchas
-----------------------

- **Direct constructor use:** Only the top level is a ``SimplifiedObject``—nested dicts remain plain dicts unless you wrap them yourself.
- **Using ``loads_simplified`` or ``load_simplified``:**
  The **entire nested structure is recursively converted**—all dicts become ``SimplifiedObject``, so you always have dot-access at every level.
- **No item access on top-level:** ``SimplifiedObject`` inherits from ``SimpleNamespace``, which does not support item access (`obj['key']`) at the top level. Use attribute access (`obj.key`) instead.
  If you need dictionary-like access, convert to dict with ``obj.__dict__`` or use ``loads_simplified`` and work with the original JSON dicts.
- **Undefined is not None:** Treat ``Undefined`` as a special "missing" value. It is falsy and compares equal to None, but it is a distinct singleton and not identical to ``None``.
- **Importing Undefined:**
  Remember to import ``Undefined`` explicitly from ``jsify.simplify`` when you want to compare or check for missing values.

See Also
--------

- :doc:`jsify` — For fully automatic, deep, recursive dot access, mutation support, and C-extension speed.

----

``SimplifiedObject`` is ideal for **quick, simple, error-free** dot-access to shallow or partially known data—either from JSON or built manually.
