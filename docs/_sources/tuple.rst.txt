Tuple
=====

Overview
--------

The :class:`jsify.Tuple` class is a jsified wrapper for Python tuples created by passing any tuple (or tuple-containing structure) to :func:`jsify.jsify`.

It supports:

- **Index access** to all nested dict/list/tuple children, all recursively jsified.
- **Attribute (dot) access** for nested dicts and lists that are jsified, but **dot access on the tuple itself is not supported** due to possible collisions with standard tuple methods.
- **All standard tuple methods**: slicing, `len()`, `count()`, `index()`, and more.
- **Iteration returns a :class:`jsify.Iterator`** that supports JavaScript-like iteration semantics.
- **Reference-based:** changes to mutable children (dicts, lists) are reflected in the original data.
- **Safe chaining:** missing attributes always return the singleton :class:`jsify.Undefined`.

Creating a jsified Tuple
------------------------

.. code-block:: python

   from jsify import jsify

   tup = ({"x": 1}, {"y": 2}, 3)
   obj = jsify(tup)

   print(type(obj))       # <class 'jsify.Tuple'>

Accessing Elements
------------------

- Use standard index access: ``obj[0]``
- Use attribute (dot) access for any nested dicts/lists/tuples that are jsified
- **Do not use dot-style attribute access on the tuple itself**, as this may conflict with tuple method names.

.. code-block:: python

   print(obj[0].x)    # 1
   print(obj[1].y)    # 2
   print(obj[2])      # 3

   # Slicing returns a new jsified Tuple
   sub = obj[:2]
   print(type(sub))   # <class 'jsify.Tuple'>
   print(sub[1].y)    # 2

Iteration
---------

- Iterating over a :class:`jsify.Tuple` returns a :class:`jsify.Iterator` instance.
- The iterator supports Python and JavaScript-like iteration semantics.

.. code-block:: python

   it = iter(obj)
   print(type(it))  # <class 'jsify.Iterator'>

   for item in it:
       print(item)

Standard Tuple Methods
----------------------

The :class:`jsify.Tuple` supports all standard Python tuple methods, including:

- ``count(value)``
- ``index(value)``
- ``__len__()``
- ``__getitem__()``
- Slicing
- Comparison operators (`==`, `<`, etc.)
- String conversion and representation

.. code-block:: python

   print(obj.count({"x": 1}))      # 1
   print(obj.index({"y": 2}))      # 1

   print(len(obj))                 # 3

   print(str(obj))
   print(repr(obj))

Reference Behavior
------------------

- Tuples themselves are immutable (assignment to elements is not allowed).
- Mutable children (e.g., dicts, lists) inside the tuple remain reference-based and changes affect the original data.

.. code-block:: python

   original = ({"a": 1},)
   t = jsify(original)
   t[0].a = 42
   print(original[0]["a"])  # 42

Limitations and Gotchas
-----------------------

- Assignment to tuple elements (e.g., ``obj[0] = value``) raises ``TypeError``.
- Slicing always produces a new jsified Tuple (never a list).
- ``count()`` and ``index()`` use Python's equality semantics (`==`), so comparisons may differ if values are wrapped.
- Indexing out of range **returns :class:`jsify.Undefined` instead of raising an exception**.
- Iteration returns a :class:`jsify.Iterator`, not the tuple itself.
- Dot-style attribute access on the tuple itself is **not supported** to avoid collisions with tuple methods.
- Use :func:`jsify.unjsify` or :func:`jsify.unjsify_deepcopy` to convert back to native tuples.
- Missing attributes or keys return :class:`jsify.Undefined`.

See Also
--------

- :class:`jsify.List` for jsified lists
- :class:`jsify.Dict` for jsified dicts
- :func:`jsify.jsify` and :func:`jsify.unjsify` for conversion
- :class:`jsify.Iterator` for iterators returned by tuples and other containers
- :class:`jsify.Undefined` singleton representing missing values
