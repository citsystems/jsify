.. _creating_camelized_functions:

.. meta::
   :keywords: Jsify, Python, camelCase, snake_case, camelized_function, decorator, JSON, API, key conversion
   :description: Learn how to use the Jsify library's camelized_function decorator to create Python functions that automatically convert camelCase keys in JSON-like dictionaries to snake_case before processing them. This guide provides examples and explanations on how to integrate camelCase to snake_case conversion into your Python code.

Creating Camelized Functions
============================

The Jsify library includes a `camelized_function` decorator that allows you to create functions that automatically convert camelCase keys in JSON-like dictionaries to snake_case before processing them. This is particularly useful in scenarios where you need to interface with systems or APIs that use camelCase naming conventions, while you prefer to work with snake_case in your Python code.

The `camelized_function` decorator converts the keys of incoming keyword arguments from camelCase to snake_case before they are passed to the function. This enables you to define functions that internally work with snake_case, while still accepting camelCase input.

**Decorator Signature:**

.. code-block:: python

    def camelized_function(replace=None)
    
- **`replace` (dict, optional):** A dictionary that specifies replacements for certain keys after they are converted to snake_case. This is useful for handling specific cases where a different key name is desired.

**Basic Usage of `camelized_function`**

To use `camelized_function`, simply apply the decorator to your function. The function will then accept camelCase keys, convert them to snake_case, and process them accordingly.

**Example:**

.. code-block:: python

    from jsify.calls import camelized_function

    @camelized_function
    def process_data(snake_case_key=None, another_key=None):
        # The function processes snake_case keys
        print(snake_case_key)
        print(another_key)

    # Calling the function with camelCase keys
    process_data(snakeCaseKey='value1', anotherKey='value2')

    # Outputs:
    # value1
    # value2

In this example, the `process_data` function expects `snake_case_key` and `another_key` as arguments. However, it can be called with camelCase keys (`snakeCaseKey` and `anotherKey`), which are automatically converted to the corresponding snake_case keys.

**Handling Specific Key Replacements**

The `replace` parameter allows you to define custom key replacements after the initial camelCase to snake_case conversion. This is useful when you need to map specific keys to custom names.

**Example:**

.. code-block:: python

    @camelized_function(replace={'some_specific_key': 'custom_key'})
    def process_data(custom_key=None):
        print(custom_key)

    # Calling the function with a camelCase key that matches the replacement rule
    process_data(someSpecificKey='value')

    # Outputs:
    # value

In this example, the `someSpecificKey` input is first converted to `some_specific_key`, and then it is replaced with `custom_key` according to the `replace` dictionary.

**Combining with Other Decorators**

You can combine `camelized_function` with other decorators, such as `jsified_function`, to create functions that are both camelized and jsified.

**Example:**

.. code-block:: python

    from jsify.calls import jsified_function, camelized_function

    @camelized_function
    @jsified_function
    def process_data(snake_case_key=None, another_key=None):
        # Now the function can also handle JSON-like objects
        print(snake_case_key)
        print(another_key)

    data = {'snakeCaseKey': 'value1', 'anotherKey': 'value2'}
    
    # Calling the function with camelCase keys and jsified input
    process_data(**data)

    # Outputs:
    # value1
    # value2
