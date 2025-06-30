Jsify Objects
=============

The **Jsify Object system** transforms Python dicts, lists, and (read-only) tuples into JavaScript-like objects
with blazing-fast dot notation, safe deep access, and reference-based, mutable structures.
All wrapped objects are powered by a high-performance C extension for maximum speed.

- **Dot access at any depth:** Use `obj.key` even on deeply nested structures—never worry about `'KeyError'` or `'AttributeError'`.
- **Reference-based:** Jsified objects reflect the original data; changes go both ways (for dicts and lists).
- **Safe undefined handling:** Missing keys/attributes return the special singleton `Undefined` object, not an exception. Any further access on `Undefined` always returns `Undefined` (like JavaScript).
- **Fully automatic:** Nesting and type detection are fully recursive; not just the top-level object is wrapped.
- **Supports all standard container operations:** Slicing and iteration for lists/tuples, in-place modification for dicts and lists, plus all standard dict methods (e.g., pop, setdefault, update, keys, values, items).

**Note:**
- *Tuples* are wrapped for read-only access and slicing, but are not mutable.
- Iterators can also be jsified for JavaScript-like iteration.
- For lightweight, pure-Python use-cases, see `SimplifiedObject` for a SimpleNamespace-based fallback (see: `simplify`).

The special `Undefined` singleton replaces exceptions for missing keys or attributes.
It is always returned when you access a non-existent property or index, and any further access on `Undefined` will also return `Undefined` (mimicking JavaScript's `undefined`).

For JSON support and details on serializing jsified objects (including omission or conversion of `Undefined`), see the [json](json) section.

.. toctree::
   :maxdepth: 2

   jsify_unjsify
   tuple
   list
   dict
   iter
   dict_functions
   json
