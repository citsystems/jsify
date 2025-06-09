.. jsify documentation master file, created by
   sphinx-quickstart on Sun Jul 28 19:34:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
   :description: Jsify is a blazing-fast Python library for attribute-style (dot notation) access to any JSON-like data, with automatic Undefined support and JavaScript-inspired convenience.
   :keywords: python, access, dictionary, library, json, javascript, objects, jsify, dot notation, attributes, access, serialization, undefined

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
   :maxdepth: 1
   :caption: Contents:

   intro
   installation
   downloading
   jsify_vs_simple
   jsifying_unjsifying
   using_dictionaries
   using_lists
   using_tuples
   using_iterators
   undefined_value
   json_serialization
   camelized_functions
   reference/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
