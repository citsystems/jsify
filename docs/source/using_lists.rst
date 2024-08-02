.. _using_lists:

Using Jsified Lists
===================

In the Jsify library, lists can be converted into `JsonList` instances, which are enhanced versions of standard Python lists with JSON-like behavior. These jsified lists allow for more intuitive manipulation of list data, including attribute-style access to elements, dynamic nesting, and integration with the broader `JsonObject` ecosystem.

**Creating and Using Jsified Lists:**

To create a jsified list, you can use the `jsify` function, which converts a standard Python list into a `JsonList`. This allows you to interact with list elements using JSON-like methods, while still preserving the familiar list operations.

**Example:**

.. code-block:: python

    from jsify import jsify

    # Standard Python list
    data = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35}
    ]

    # Convert to a jsified list
    json_list = jsify(data)

    # Accessing list elements using indexing
    print(json_list[0].name)  # Outputs: Alice
    print(json_list[1].age)   # Outputs: 25

    # Iterating over the jsified list
    for item in json_list:
        print(f"{item.name} is {item.age} years old")
        # Outputs:
        # Alice is 30 years old
        # Bob is 25 years old
        # Charlie is 35 years old

**Manipulating Jsified Lists:**

Jsified lists behave similarly to regular Python lists, with the added benefit of JSON-like access to their elements. You can still perform standard list operations like appending, inserting, or removing elements, while also taking advantage of the dynamic behavior offered by `JsonObject`.

**Example:**

.. code-block:: python

    # Appending a new element to the jsified list
    json_list.append({'name': 'David', 'age': 40})
    print(json_list[3].name)  # Outputs: David

    # Removing an element from the jsified list
    json_list.pop(1)  # Removes Bob from the list

    # Accessing updated list
    for item in json_list:
        print(item.name)
        # Outputs:
        # Alice
        # Charlie
        # David

**Advanced Usage:**

Jsified lists support nesting, which allows you to work with deeply nested data structures seamlessly. You can access and manipulate nested elements using the same intuitive interface.

**Example:**

.. code-block:: python

    nested_data = [
        {'name': 'Alice', 'details': {'city': 'Wonderland', 'age': 30}},
        {'name': 'Bob', 'details': {'city': 'Metropolis', 'age': 25}},
    ]

    json_nested_list = jsify(nested_data)

    # Accessing nested elements
    print(json_nested_list[0].details.city)  # Outputs: Wonderland
    print(json_nested_list[1].details.age)   # Outputs: 25

    # Modifying nested elements
    json_nested_list[0].details.age = 31
    print(json_nested_list[0].details.age)  # Outputs: 31

**Using Native List Methods:**

Jsified lists retain all the native Python list methods, such as `append`, `remove`, `pop`, `insert`, and more. This means you can manipulate jsified lists just like you would with standard Python lists, while still benefiting from JSON-like behavior.

**Example:**

.. code-block:: python

    json_list = [
        {'name': 'Alice', 'details': {'city': 'Wonderland', 'age': 30}},
        {'name': 'Bob', 'details': {'city': 'Metropolis', 'age': 25}},
        {'name': 'Charlie', 'details': {'city': 'Metropolis', 'age': 35}},
    ]

    # Appending a new element to the jsified list
    json_list.append({'name': 'David', 'age': 40})
    print(json_list[3].name)  # Outputs: David

    # Removing an element from the jsified list
    json_list.remove(json_list[1])  # Removes Bob from the list

    # Accessing updated list
    for item in json_list:
        print(item.name)
        # Outputs:
        # Alice
        # Charlie
        # David

    # Inserting an element at a specific index
    json_list.insert(1, {'name': 'Eve', 'age': 28})
    print(json_list[1].name)  # Outputs: Eve

**Using `json_keys` with Jsified Lists:**

The `json_keys` function can be used with `JsonList` to retrieve the indices of the list elements as keys, represented in string format.

**Example:**

.. code-block:: python

    from jsify import json_keys

    json_list = [
        {'name': 'Alice', 'details': {'city': 'Wonderland', 'age': 30}},
        {'name': 'Bob', 'details': {'city': 'Metropolis', 'age': 25}},
        {'name': 'Charlie', 'details': {'city': 'Metropolis', 'age': 35}},
    ]

    # Get a view of the indices as keys
    keys_view = json_keys(json_list)
    for key in keys_view:
        print(key)
    # Outputs: '0', '1', '2'

**Using `json_items` with Jsified Lists:**

The `json_items` function allows you to retrieve the elements of a `JsonList` as key-value pairs, where the keys are the indices of the elements in string format.

**Example:**

.. code-block:: python

    from jsify import json_items

    # Get a view of the items with indices as keys
    items_view = json_items(json_list)
    for key, value in items_view:
        print(f"{key}: {value.name}, {value.age}")
    # Outputs:
    # 0: Alice, 30
    # 1: Bob, 25
    # 2: Charlie, 35

By using jsified lists, you gain the flexibility of dynamic JSON-like data manipulation combined with the power of Python's list operations. This makes `JsonList` an excellent choice for working with complex and nested list data in a more intuitive and accessible way.
