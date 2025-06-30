jsify / unjsify
==============

Overview
--------

The Jsify Object system allows you to convert Python dictionaries, lists, tuples, and iterators into JavaScript-like, dot-accessible containers, powered by a high-performance C extension.
All access is reference-based by default—mutations are visible in both directions.
You can also create *deeply independent* jsified copies or deeply convert back to pure Python structures using the `jsified_deepcopy` and `unjsify_deepcopy` helpers.

----

Jsify
-----

**jsify(obj)**

Wraps a Python dict, list, tuple, or iterator in a jsified container that allows:

- **Dot-style attribute access** at every depth
- **Reference-based mutation** (changes propagate instantly to the underlying Python object)
- **Safe deep attribute/item access** (missing keys or attributes always return `Undefined` instead of raising errors)
- **Automatic recursive wrapping** for all nested containers

**Return types:**
Depending on the type of input object, `jsify` returns a specific Jsify object type:

- **Dict** → :class:`jsify.Dict`
- **List** → :class:`jsify.List`
- **Tuple** → :class:`jsify.Tuple`
- **Iterator** → :class:`jsify.Iterator`
- All other types (int, float, str, None, bool, already-jsified objects, or `Undefined`) are returned unchanged

Each Jsify object type:
- Preserves all native Python behaviors (iteration, slicing, etc.)
- Adds fast, safe dot notation at every level

**Examples:**

.. code-block:: python

   from jsify import jsify

   print(type(jsify({"a": 1})))             # <class 'jsify.Dict'>
   print(type(jsify([1, 2, 3])))            # <class 'jsify.List'>
   print(type(jsify((1, 2, 3))))            # <class 'jsify.Tuple'>
   print(type(jsify(iter([1, 2]))))         # <class 'jsify.Iterator'>
   print(type(jsify((x for x in range(2)))))# <class 'jsify.Iterator'>
   print(jsify(123))                        # 123 (unchanged)
   print(jsify(None))                       # None (unchanged)

   obj = jsify({"foo": [1, {"bar": 2}]})
   print(type(obj.foo))                     # <class 'jsify.List'>
   print(type(obj.foo[1]))                  # <class 'jsify.Dict'>

   # All changes are by reference
   obj.foo[1].bar = 99

Scalars (numbers, strings, bools, None) and already-jsified objects are returned unchanged.

**Missing key or attribute:**
No error—always returns `Undefined`:

.. code-block:: python

   print(obj.not_present)      # Undefined
   print(obj.foo[99])          # Undefined (for out-of-bounds access)
   print(obj.foo[1].not_here)  # Undefined

---------------------

Jsified Deep Copy
-----------------

Normally, `jsify()` recursively wraps all dicts, lists, tuples, and iterators for dot access at every level.
All mutations are reference-based: changes to the jsified object are instantly reflected in the original.

If you want an *independent deep copy* of the whole structure (not referencing the original data), use `jsified_deepcopy`:

**Example:**

.. code-block:: python

   from jsify import jsify, jsified_deepcopy

   original = {"x": {"y": [1, 2, {"z": 3}]}}
   obj = jsify(original)
   obj2 = jsified_deepcopy(obj)  # deep, independent jsified copy

   obj.x.y[2].z = 99
   print(original["x"]["y"][2]["z"])  # 99 (reference)

   obj2.x.y[2].z = 100
   print(original["x"]["y"][2]["z"])  # 99 (deep copy: original not changed)

**Summary:**
- `jsify(obj)` — recursive, reference-based wrapping; correct Jsify type returned for each container
- `jsified_deepcopy(obj)` — deep-copied, jsified structure (no references to original data)

See:
- :class:`jsify.Tuple`
- :class:`jsify.List`
- :class:`jsify.Dict`
- :class:`jsify.Iterator`

----

Unjsify
-------

**unjsify(obj)**

Returns the *original*, underlying Python container from a jsified object—**shallow** by default.

- If given a jsified dict/list/tuple/iterator, returns the original Python object (top-level only).
- For other objects (scalars, non-jsified types), returns as-is.

**Examples:**

.. code-block:: python

   from jsify import jsify, unjsify

   d = {"foo": {"bar": 1}}
   obj = jsify(d)
   orig = unjsify(obj)
   print(orig is d)  # True

   # Only the top-level jsified object is unwrapped:
   print(type(unjsify(obj.foo)))  # <class 'list'>

---------------------

Unjsify Deep Copy
-----------------

**unjsify_deepcopy(obj)**

Recursively converts any jsified containers (Dict, List, Tuple, Iterator) into native Python objects (dict, list, tuple, etc.), returning a deep-copied, pure-Python structure.
This is important if you have ever nested jsified objects inside other Python containers and then wrapped the whole structure again, which can otherwise result in a mixed jsified/native structure.

**Example Scenario:**

.. code-block:: python

   from jsify import jsify, unjsify, unjsify_deepcopy

   # Create a jsified object and nest it in another dict
   profile = jsify({"name": "Alice"})
   data = {"profile": profile, "type": "admin"}

   # Now jsify the whole structure
   user = jsify(data)

   # .profile is STILL a jsified object, not a dict!
   print(type(user.profile))  # <class 'jsify.Dict'>

   # Shallow unjsify only unwraps the top-level
   shallow = unjsify(user)
   print(type(shallow["profile"]))  # <class 'jsify.Dict'>

   # Deep unjsify fully unwraps everything recursively
   deep = unjsify_deepcopy(user)
   print(type(deep["profile"]))     # <class 'dict'>

   # Now deep["profile"] is a plain dict, safe for vanilla Python code or export

**Summary:**
- Use `unjsify(obj)` to get the original, possibly mixed, structure (shallow unwrap)
- Use `unjsify_deepcopy(obj)` if you need a *fully native* structure (dicts/lists/tuples only),
  especially if you have ever nested jsified objects inside original data!

----

Quick Reference Table
---------------------

+-------------------------+-----------------------------------------------+
| Function                | Purpose                                       |
+=========================+===============================================+
| jsify(obj)              | Returns: Dict, List, Tuple, Iterator (with    |
|                         | recursive, reference-based, mutation-safe     |
|                         | dot/item access)                              |
+-------------------------+-----------------------------------------------+
| jsified_deepcopy(obj)   | Deep-copied jsified structure, independent    |
|                         | from original                                 |
+-------------------------+-----------------------------------------------+
| unjsify(obj)            | Shallow unwrapping (top-level original)       |
+-------------------------+-----------------------------------------------+
| unjsify_deepcopy(obj)   | Deep pure-Python copy (no jsified wrappers)   |
+-------------------------+-----------------------------------------------+

----

See Also
--------

- :class:`jsify.Dict` — Dict wrapper with dot access
- :class:`jsify.List` — List wrapper with dot access
- :class:`jsify.Tuple` — Tuple wrapper with dot access
- :class:`jsify.Iterator` — Iterator wrapper with dot access
- :class:`jsify.Undefined` — Singleton returned for all missing keys/attributes
- :func:`jsified_get` / :func:`jsified_pop` / :func:`jsified_setdefault` / :func:`jsified_update` — helpers for dictionary-style operations on jsified objects
