.. _using_tuples:

.. meta::
   :keywords: Jsify, Python, jsified tuples, Tuple, JSON-like objects, attribute access, data manipulation, nested data, jsified_keys, jsified_items
   :description: Learn how to use jsified tuples in the Jsify library for Python. This guide covers creating jsified tuples, accessing elements with attribute-style access, working with nested data, and using utility functions like jsified_keys and jsified_items.

Using Jsified Tuples
====================

In the Jsify library, tuples can be converted into ``Tuple`` instances, which are enhanced versions of standard Python tuples with JSON-like behavior. These jsified tuples allow for more intuitive manipulation of tuple data, including attribute-style access to elements, dynamic nesting, and integration with the broader ``Object`` ecosystem.

**Creating and Using Jsified Tuples:**

To create a jsified tuple, you can use the ``jsify`` function, which converts a standard Python tuple into a ``Tuple``. This allows you to interact with tuple elements using JSON-like methods, while still preserving the immutable characteristics of tuples.

**Example:**

.. code-block:: python

    from jsify import jsify

    # Standard Python tuple
    data = (
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35}
    )

    # Convert to a jsified tuple
    json_tuple = jsify(data)

    # Accessing tuple elements using indexing
    print(json_tuple[0].name)  # Outputs: Alice
    print(json_tuple[1].age)   # Outputs: 25

    # Iterating over the jsified tuple
    for item in json_tuple:
        print(f"{item.name} is {item.age} years old")
        # Outputs:
        # Alice is 30 years old
        # Bob is 25 years old
        # Charlie is 35 years old

**Tuple Methods:**

Jsified tuples provide additional methods similar to standard Python tuples:

- ``count(value)``
  Returns the number of times ``value`` appears in the tuple.

  .. code-block:: python

      t = jsify((1, 2, 2, 3))
      print(t.count(2))  # Outputs: 2

- ``index(value)``
  Returns the index of the first occurrence of ``value`` in the tuple.

  .. code-block:: python

      t = jsify(('a', 'b', 'c'))
      print(t.index('b'))  # Outputs: 1

**Result of ``dir()``**

- ``dir(jsified_tuple)``
  Returns a tuple of stringified integer indices representing valid keys.

  .. code-block:: python

      t = jsify(('x', 'y'))
      print(dir(t))  # Outputs: ('0', '1')


**Advanced Usage:**

Jsified tuples support nesting, which allows you to work with deeply nested data structures seamlessly. You can access and manipulate nested elements using the same intuitive interface.

.. code-block:: python

    nested_tuple = (
        {'name': 'Alice', 'details': {'city': 'Wonderland', 'age': 30}},
        {'name': 'Bob', 'details': {'city': 'Metropolis', 'age': 25}},
    )

    json_nested_tuple = jsify(nested_tuple)

    # Accessing nested elements
    print(json_nested_tuple[0].details.city)  # Outputs: Wonderland
    print(json_nested_tuple[1].details.age)   # Outputs: 25

    # Using jsified_items with nested data
    items_view = jsified_items(json_nested_tuple)
    for key, value in items_view:
        print(f"{key}: {value.details.city}")
        # Outputs:
        # 0: Wonderland
        # 1: Metropolis

By using jsified tuples and the ``jsified_keys`` and ``jsified_items`` functions, you can gain the flexibility of dynamic JSON-like data manipulation combined with the power of Python's immutable tuples. This makes ``Tuple`` an excellent choice for working with complex and nested tuple data in a more intuitive and accessible way.
