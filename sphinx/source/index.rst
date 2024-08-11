.. jsify documentation master file, created by
   sphinx-quickstart on Sun Jul 28 19:34:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
   :description: Jsify is a Python library designed to bridge the gap between Python's data structures and JSON-like
      objects, offering seamless integration and manipulation of data in a JavaScript-like manner
      With Jsify, you can effortlessly convert Python dictionaries, lists, and tuples into JSON-like
      objects that support attribute-style access (dot notation), automatic handling of undefined
      properties, and easy serialization.
   :keywords: json javascript objects jsify dot notation attributes serialization


Welcome to jsify's documentation!
=================================

The Jsify library provides a powerful suite of tools for working with JSON-like data structures in Python. At its core, the library introduces the `Object` class, which allows for attribute-style access (using dot notation) and dynamic manipulation of data, closely mimicking the behavior of JavaScript objects. This makes it particularly well-suited for developers working in environments where JSON data is prevalent, such as in web development, API integrations, and data processing tasks.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   intro
   jsify_vs_simple
   installation
   downloading
   jsifying_unjsifying
   using_dictionaries
   using_lists
   using_tuples
   using_iterators
   undefined_value
   json_serialization
   using_assertions
   jsified_functions
   camelized_functions
   properties_exist
   aiohttp
   reference/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
