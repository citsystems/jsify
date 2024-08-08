.. _using_iterators:

Jsified Iteration Over Native Python Objects
=============================================

The `Iterator` class in the Jsify library is a powerful tool that can be used not only with jsified data structures but also with native Python objects like dictionaries, lists, and tuples. When iterating over native Python objects using `Iterator`, the elements returned are automatically converted into jsified objects (`Object`, `Dict`, `List`, `Tuple`). This means that you can take advantage of property-style access and other JSON-like behaviors even when starting with standard Python types.

**Example:**

.. code-block:: python

    from jsify import jsify, Iterator

    # Native Python dictionary
    native_list = jsify([
        {
            'name': 'Bob',
            'details': {
                'age': 25,
                'city': 'Metropolis'
            }
        },
        {
            'name': 'Alice',
            'details': {
                'age': 30,
                'city': 'Warsaw'
            }
        }
    ])

    # Accessing nested values during iteration
    for value in Iterator(native_list):
        print(f'{value.name} of age {value.details.age}')
    # Outputs: 'Bob of age 25', 'Alice of age 30'
