.. _properties_exist_usage:

.. meta::
   :keywords: Jsify, Python, properties_exist, JSON, nested properties, data validation, Object, JSON-like data, robust code, data integrity
   :description: Learn how to use the properties_exist function in the Jsify library to check for the existence of nested properties within JSON-like objects. This guide provides examples and usage scenarios to help you ensure the integrity and reliability of your data access patterns.

Checking if Properties Path Exists
==================================

The `properties_exist` function in the Jsify library is a utility designed to check if a series of properties exist within a JSON-like object (`Object`). This function is particularly useful for validating the presence of nested properties in complex data structures, ensuring that your code can safely access deeply nested data without encountering errors.


The `properties_exist` function is a valuable tool for validating the presence of properties in JSON-like data structures, particularly when working with deeply nested objects. By using this function, you can avoid errors that might arise from accessing non-existent properties, making your code more reliable and easier to maintain. This utility is especially useful in scenarios where data structures are dynamic or partially defined, providing a simple and effective way to ensure the integrity of your data access patterns.

Usage of `properties_exist`
---------------------------

The `properties_exist` function allows you to verify the existence of a sequence of nested properties within a `Object`. If all the properties in the given path exist, the function returns `True`; otherwise, it returns `False`.

**Example:**

.. code-block:: python

    from jsify import jsify, properties_exist

    # Example JSON-like data
    data = {
        'user': {
            'name': 'Alice',
            'details': {
                'age': 30,
                'address': {
                    'city': 'Wonderland',
                    'zipcode': '12345'
                }
            }
        }
    }

    # Convert to a jsified object
    json_obj = jsify(data)

    # Check if a series of properties exist
    result = properties_exist(json_obj, 'user', 'details', 'address', 'city')
    print(result)  # Outputs: True

    # Check for a non-existent property
    result = properties_exist(json_obj, 'user', 'details', 'address', 'country')
    print(result)  # Outputs: False

Using the Result of `properties_exist`
--------------------------------------

The result of the `properties_exist` function can be directly used in conditional statements to make your code more robust, especially when dealing with optional or dynamically structured data.

**Example:**

.. code-block:: python

    exists = properties_exist(json_obj, 'user', 'details', 'address', 'city')
    if exists:
        # The result contains both jsified and unjsified value of target element
        # if the element exists
        print(f"User's city unjsified: {exists.unjsified}")
        print(f"User's city jsified: {exists.jsified}")
    else:
        print("City information is not available.")
