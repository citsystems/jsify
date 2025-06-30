List
====

Overview
--------

:class:`jsify.List` is the jsified wrapper for Python lists, created by passing any list (or list-containing structure) to :func:`jsify`.

It supports:

- **Standard index access** for all elements.
- **All standard list methods**: append, extend, insert, remove, pop, clear, copy, count, index, sort, reverse, etc.
- **Mutable and reference-based**: changes are always reflected in the original data and vice versa.
- **Safe chaining**: missing elements accessed by index out of range return ``Undefined``.
- **Iteration returns a :class:`jsify.Iterator`** supporting Python and JavaScript-like iteration semantics.

Creating a Jsified List
-----------------------

.. code-block:: python

   from jsify import jsify

   lst = [{"x": 1}, {"y": 2}, 3]
   obj = jsify(lst)

   print(type(obj))       # <class 'jsify.List'>

Accessing Elements
------------------

- Use standard index access: ``obj[0]``
- **Do not use dot-style attribute access for list elements or keys**; unlike dicts, jsified lists do **not** support attribute access for elements or keys to avoid collision with list methods.
- For nested dicts/lists inside the list, use index access combined with attribute access on those nested dicts/lists.

.. code-block:: python

   print(obj[0]["x"])    # 1  (if element is dict)
   print(obj[1]["y"])    # 2
   print(obj[2])         # 3  (native int)

   # Dot access like `obj.nope` is not supported on lists and may conflict with methods.

.. note::

   This design preserves full access to list methods and avoids name collisions.

Iteration
---------

- Iterating over a :class:`jsify.List` returns a :class:`jsify.Iterator`.
- The iterator supports Python and JavaScript-like iteration semantics.

.. code-block:: python

   it = iter(obj)
   print(type(it))  # <class 'jsify.Iterator'>

   for item in it:
       print(item)

Standard List Methods
---------------------

:class:`jsify.List` supports all standard Python list methods, including:

- ``append(value)``
- ``extend(iterable)``
- ``insert(index, value)``
- ``remove(value)``
- ``pop([index])``
- ``clear()``
- ``copy()``
- ``count(value)``
- ``index(value)``
- ``sort(key=None, reverse=False)``
- ``reverse()``
- ``__len__()``
- ``__getitem__()``
- ``__setitem__()``
- ``__delitem__()``
- ``__iter__()``
- Slicing
- Comparison (`==`, `<`, etc.)
- String conversion and representation

.. code-block:: python

   obj.append({"z": 9})
   print(obj[-1]["z"])    # 9

   obj[0]["x"] = 42
   print(lst[0]["x"])  # 42  # Changes affect original list

   obj.remove(3)
   print(len(obj))     # len(lst) after removal

   # Iteration and length
   for item in obj:
       print(item)
   print(len(obj))

   # List arithmetic and slicing
   print(list(obj * 2))
   sublist = obj[1:]
   print(type(sublist))

   # String representation
   print(str(obj))
   print(repr(obj))

Reference Behavior
------------------

- All changes to the jsified list (and its nested elements) are immediately reflected in the original Python list and vice versa.
- Assigning a jsified object as a list element keeps it jsified.
- For example:

.. code-block:: python

   obj[0]["x"] = 100
   print(lst[0]["x"])  # 100

- For converting back to native types throughout nested structures, see :doc:`jsify_unjsify`.

Limitations and Gotchas
-----------------------

- All mutation operations (``append``, ``insert``, ``pop``, etc.) directly modify the original data.
- Slicing always produces a new jsified List (never a native Python list).
- When unjsifying, only the top-level list becomes native unless you use ``unjsify_deepcopy`` to recurse.
- Methods like ``index()`` and ``count()`` use Python equality comparison:
  - Be cautious comparing jsified children with native objects; equality may not behave as expected.
- No type enforcement is performed; lists may contain mixed jsified and native elements.
- Indexing out of range **returns :class:`jsify.Undefined` instead of raising an exception**.
- Dot-style attribute access on the list itself for elements or keys is **not supported** to avoid method name collisions.

Exceptions
----------

- ``remove(value)`` raises ``ValueError`` if the value is not found.
- ``index(value)`` raises ``ValueError`` if the value is not found.
- ``pop(index)`` raises ``IndexError`` if the list is empty or index is out of range.

See Also
--------

- :class:`jsify.List` — This class.
- :class:`jsify.Tuple` — Jsified tuples.
- :class:`jsify.Dict` — Jsified dictionaries.
- :doc:`jsify_unjsify` — Conversion and reference handling.
- :class:`jsify.Iterator` — Iterators returned by lists and other containers.

Examples
--------

.. code-block:: python

   from jsify import jsify

   data = [{"a": 1}, {"b": 2}, 3]
   js_list = jsify(data)

   # Access nested attributes with index and dot notation on dicts
   print(js_list[0]["a"])  # 1

   # Modify nested values; changes reflect in original list
   js_list[1]["b"] = 20
   print(data[1]["b"])  # 20

   # Append new item
   js_list.append({"c": 3})
   print(js_list[-1]["c"])  # 3

   # Slicing returns jsified List
   sublist = js_list[:2]
   print(type(sublist))  # <class 'jsify.List'>

   # Iteration
   for item in js_list:
       print(item)

   # Equality caution: comparing jsified with native
   print(js_list[2] == 3)       # True
   print(js_list[0] == {"a": 1}) # May be False due to jsify wrappers
