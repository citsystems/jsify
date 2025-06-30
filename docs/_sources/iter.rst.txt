Iterator
========

Overview
--------

:class:`jsify.Iterator` is the jsified wrapper for Python iterators, created by passing any Python iterator to :func:`jsify`.
It provides:

- **Sequential access only:** you can only iterate forward; there is no random or indexed access to the iterator itself.
- **Yields jsified values:** every value yielded is automatically jsified (if possible: e.g. dicts, lists, tuples are wrapped for dot/index access).
- **Dot/index access on yielded items:** if a yielded value is a dict, list, or tuple, you can use dot or index access on it; for other types, use as-is.
- **Safe chaining on yielded objects:** missing attributes or indexes on jsified dicts/lists/tuples yield ``Undefined``, allowing safe chaining.
- **Reference semantics:** the iterator wraps the original Python iterator directly; once exhausted, it cannot be rewound or reused.

.. note::

   ``jsify.Iterator`` does **not** support random access, indexing, or attribute chaining itself; these features apply only to the items yielded by the iterator (if they are jsifiable).

Creating a Jsified Iterator
---------------------------

To create a jsified iterator, pass any Python iterator (not just any iterable) to :func:`jsify`:

.. code-block:: python

   from jsify import jsify

   it = iter([{"a": 1}, {"b": 2}, 3])
   obj = jsify(it)
   print(type(obj))  # <class 'jsify.Iterator'>

   # Trying to pass a non-iterator (like an int or plain list) will not return a jsify.Iterator.

Basic Usage
-----------

You can iterate as with any Python iterator. Each yielded value is jsified, so you can use dot/index access if possible:

.. code-block:: python

   for item in obj:
       print(item)  # item is jsified: supports .a/.b if item is dict, [0] if list/tuple, otherwise returned as-is

   # Or access elements one by one:
   item = next(obj)
   if hasattr(item, "a"):
       print(item.a)
   else:
       print(item)

   # Nested dicts/lists/tuples are jsified recursively
   obj2 = jsify(iter([{"x": {"y": 5}}]))
   print(next(obj2).x.y)  # 5

   # Attempting to access .foo on a non-jsified item (like int/str) returns AttributeError as normal.

Iterator Semantics and Limitations
----------------------------------

- The jsified iterator wraps and **consumes** the original Python iterator; it cannot be rewound or reset.
- Iteration is **one-time only**. If you iterate past the end, ``StopIteration`` is raised (just like any Python iterator).
- There is **no random access**: no support for ``[]`` or ``.get()`` on the iterator itself.
- Passing a non-iterator (e.g., an int, list, or dict) to :func:`jsify` does **not** create a jsified iterator; you must explicitly call ``iter()`` first.
- If you try to access attributes or indexes on the jsified iterator itself (not on its items), you'll get normal Python errors.

Error Handling
--------------

- **StopIteration:** As with all Python iterators, iterating past the end raises ``StopIteration``.

Examples
--------

.. code-block:: python

   # Reusing an exhausted jsified iterator:
   obj = jsify(iter([1, 2]))
   print(list(obj))  # [1, 2]
   print(list(obj))  # []

   # Attempting random access:
   obj = jsify(iter([{"a": 1}, {"b": 2}]))
   try:
       print(obj[0])
   except TypeError:
       print("No random access: Iterator does not support indexing.")

See Also
--------

- :doc:`list` for jsified lists
- :doc:`tuple` for jsified tuples
- :doc:`dict` for jsified dicts
- :func:`jsify` and :func:`unjsify` for conversion and reference rules
- :func:`jsified_copy`, :func:`jsified_deepcopy` for copying jsified objects

