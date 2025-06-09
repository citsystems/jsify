.. _intro:

.. meta::
   :keywords: Jsify, Python, JSON, Object, data structures, attribute access, performance efficiency, API development, web development, data transformation
   :description: Explore the Jsify library, which provides tools for working with JSON-like data structures in Python. Learn about the Object class, jsify and unjsify functions, decorators, and other utilities that make JSON handling more intuitive and efficient.

Introduction
============

Jsify is a **blazing-fast Python library** for JSON-like data with JavaScript-style dot notation and automatic `Undefined` support.
It is written as a C TypeExtension—10× faster than dotmap and up to 50× faster than Box—while offering much more power and safety than SimpleNamespace.

**Key Concept: Wrapping the Original Object**

Unlike libraries that copy or deeply convert your data, Jsify’s `Object` class wraps the original Python object directly.
This brings several major advantages:

- **Performance Efficiency:** No deep copies—minimal memory use, maximum speed.
- **Data Integrity:** All changes via the `Object` interface instantly affect the original data and vice versa.
- **Seamless Integration:** Instantly adds JSON-like, attribute-style access to your data structures, without breaking compatibility.
- **Flexibility:** Apply Jsify’s features exactly where you need them, on any Python object.

In addition to `Object`, Jsify includes tools for converting between native Python structures and their Jsify-wrapped forms:
- Use `jsify` to wrap any object (dict, list, tuple) with dot-access and JavaScript-like features.
- Use `unjsify` to revert to standard Python objects.
- Use `unjsify_deepcopy` for a deeply unjsified copy, converting all nested Jsify objects back to Python built-ins.

Key Components:
---------------

- **Object Class:** The cornerstone for JavaScript-like, dynamic interaction with Python data.
- **Dict, List, Tuple:** Specialized subclasses with methods tailored for each type.
- **jsify and unjsify Functions:** Easy conversion between Python and Jsify world.
- **Decorators and Encoders:** Automate jsify/unjsify logic and serialization (e.g., `ObjectEncoder`).
- **Exception Handling:** The `AnyError` exception for consistent error handling.
- **String Conversion Tools:** For naming conventions like `camelCase` and `snake_case`.

Use Cases:
----------

Jsify is perfect for:
- **API Development:** Intuitive, safe access to JSON from APIs.
- **Data Transformation:** Manipulating deeply nested or changing data.
- **Web Development:** Write Python code with the speed and style of JavaScript.
- **Configuration Management:** Attribute-style, dynamic config access.

Getting Started:
----------------

Install Jsify and explore the `Object` class, plus its handy conversion tools.
Full details are in this documentation—start making your data work like JavaScript, but in Python!

