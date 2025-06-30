JSON dump / load
================

The :mod:`jsify.json` module provides all tools you need to **serialize (dump)** jsified objects to JSON—handling `Undefined` and all jsified container types.

Dumping Jsified Objects to JSON
-------------------------------

The two main functions for dumping jsified objects are:

**jsified_dumps(obj, omit_undefined=True, \*\*kwargs)**
:   Serialize a jsified object to a JSON-formatted string.
:
:   If `omit_undefined` is True (default), fields with value `Undefined` are omitted from output.
:   If False, `Undefined` values are serialized as `null`.
:   Additional keyword arguments (e.g., `indent=2`) are forwarded to the underlying `json.dumps`.
:
:   Note that `omit_undefined` is a custom argument handled by jsify, not a standard JSON argument.

.. code-block:: python

   from jsify import jsify, Undefined
   from jsify.json import jsified_dumps

   obj = jsify({"a": 1, "b": Undefined, "c": [1, {"x": Undefined}]})

   # Omit fields with Undefined (default)
   print(jsified_dumps(obj))   # {"a": 1, "c": [1, {}]}

   # Serialize Undefined as null
   print(jsified_dumps(obj, omit_undefined=False))  # {"a": 1, "b": null, "c": [1, {"x": null}]}

   # Use standard JSON kwargs (indent)
   print(jsified_dumps(obj, indent=2))


**jsified_dump(obj, fp, omit_undefined=True, \*\*kwargs)**
:   Serialize a jsified object and write JSON directly to an open file-like object `fp`.
:
:   Parameters order is `(object, file)`, matching Python’s standard `json.dump`.
:   `omit_undefined` works as in `jsified_dumps`.
:   Additional keyword arguments are forwarded to `json.dump`.

.. code-block:: python

   with open("out.json", "w") as f:
       jsified_dump(obj, f, indent=2)

Loading JSON Data
-----------------

To **load** JSON data, use Python’s standard :mod:`json` module, then wrap the result with :func:`jsify` to gain dot-access and `Undefined` support:

.. code-block:: python

   import json
   from jsify import jsify

   data = json.loads('{"a": 1, "b": {"c": 2}}')
   obj = jsify(data)
   print(obj.b.c)   # 2

   # Or from a file:
   with open("input.json") as f:
       data = json.load(f)
   obj = jsify(data)

.. note::

   The :func:`jsify` function wraps only the top-level object. Nested dictionaries or lists
   inside the loaded data remain plain Python types. For recursive wrapping of nested structures,
   you must apply a suitable function or custom recursive logic.

Encoder and Decoder Notes
-------------------------

- The :func:`jsified_dumps` and :func:`jsified_dump` functions always use the internal
  :class:`ObjectEncoder` which handles jsified types and `Undefined` properly.
- You **do not** need to specify a custom encoder manually when using these functions.
- If you use standard :func:`json.dumps` or :func:`json.dump` on jsified objects,
  you **must** specify `cls=ObjectEncoder` explicitly. Otherwise, serialization will fail
  for `Undefined` or jsified containers with a `TypeError`.
- The encoder also supports serializing :class:`types.SimpleNamespace` instances by converting
  them to dictionaries.
- Decoding (loading) always produces standard Python types; wrapping with :func:`jsify` enables dot-access and `Undefined`.

See Also
--------

- :doc:`dict` for jsified dict behaviors
- :doc:`jsify_unjsify` for conversions, reference rules, and copying
- Python’s standard :mod:`json` documentation
- :mod:`jsify.simplify` for alternative simplified object handling with automatic attribute fallback

