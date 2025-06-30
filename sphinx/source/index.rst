Welcome to jsify's documentation!
=================================

**Jsify** is a blazing-fast Python library for handling JSON-like data with JavaScript-style convenience.

With Jsify you can:
- Use dot notation for dictionaries, lists, and tuples—`obj.key` instead of `obj['key']`, even for nested structures.
- Access missing keys safely using `Undefined`, just like in JavaScript—no more `KeyError`.
- Enjoy performance: C TypeExtension, only ~2× slower than SimpleNamespace (but much more powerful), 10× faster than dotmap, and up to 50× faster than Box.
- Work seamlessly with JSON data—perfect for APIs, web applications, and dynamic or unknown schemas.
- Write code that feels natural to JavaScript developers, but in pure Python.

Jsify is the perfect tool whenever you need readable, robust, and error-tolerant access to dynamic data—especially with APIs, web payloads, or any JSON-centric workflow.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   installation
   simplify
   jsify
   json

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
