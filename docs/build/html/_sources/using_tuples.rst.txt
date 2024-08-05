.. _using_tuples:

Using Jsified Tuples
====================

In the Jsify library, tuples can be converted into `JsonTuple` instances, which are enhanced versions of standard Python tuples with JSON-like behavior. These jsified tuples allow for more intuitive manipulation of tuple data, including attribute-style access to elements, dynamic nesting, and integration with the broader `JsonObject` ecosystem.

**Creating and Using Jsified Tuples:**

To create a jsified tuple, you can use the `jsify` function, which converts a standard Python tuple into a `JsonTuple`. This allows you to interact with tuple elements using JSON-like methods, while still preserving the immutable characteristics of tuples.

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

**Using `json_keys` with Jsified Tuples:**

The `json_keys` function can be used with `JsonTuple` to retrieve the indices of the tuple elements as keys, represented in string format.

**Example:**

.. code-block:: python

    from jsify import json_keys

    # Get a view of the indices as keys
    keys_view = json_keys(json_tuple)
    for key in keys_view:
        print(key)
        # Outputs: '0', '1', '2'

**Using `json_items` with Jsified Tuples:**

The `json_items` function allows you to retrieve the elements of a `JsonTuple` as key-value pairs, where the keys are the indices of the elements in string format.

**Example:**

.. code-block:: python

    from jsify import json_items

    # Get a view of the items with indices as keys
    items_view = json_items(json_tuple)
    for key, value in items_view:
        print(f"{key}: {value.name}, {value.age}")
        # Outputs:
        # 0: Alice, 30
        # 1: Bob, 25
        # 2: Charlie, 35

**Advanced Usage:**

Jsified tuples support nesting, which allows you to work with deeply nested data structures seamlessly. You can access and manipulate nested elements using the same intuitive interface.

**Example:**

.. code-block:: python

    nested_tuple = (
        {'name': 'Alice', 'details': {'city': 'Wonderland', 'age': 30}},
        {'name': 'Bob', 'details': {'city': 'Metropolis', 'age': 25}},
    )

    json_nested_tuple = jsify(nested_tuple)

    # Accessing nested elements
    print(json_nested_tuple[0].details.city)  # Outputs: Wonderland
    print(json_nested_tuple[1].details.age)   # Outputs: 25

    # Using json_items with nested data
    items_view = json_items(json_nested_tuple)
    for key, value in items_view:
        print(f"{key}: {value.details.city}")
        # Outputs:
        # 0: Wonderland
        # 1: Metropolis

By using jsified tuples and the `json_keys` and `json_items` functions, you can gain the flexibility of dynamic JSON-like data manipulation combined with the power of Python's immutable tuples. This makes `JsonTuple` an excellent choice for working with complex and nested tuple data in a more intuitive and accessible way.
