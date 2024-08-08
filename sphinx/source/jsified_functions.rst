.. _jsified_functions:

Creating Jsified Functions
==========================

The Jsify library provides decorators and utilities in the `calls` module that help you automatically convert function arguments to `Object` instances, as well as process the results of these functions based on specific criteria. This module is particularly useful when you need to ensure that your functions can handle JSON-like data seamlessly, providing a consistent and predictable interface.

The primary utility provided by the `calls` module is the `jsified_function` decorator. This decorator automatically converts function arguments that are dictionaries, lists, or tuples into their corresponding jsified objects (`Dict`, `List`, `Tuple`). Additionally, it offers options to control how the function's result is processed, either by returning the original object, deeply unjsified data, or a jsified version.

**Decorator Signature:**

.. code-block:: python

    def jsified_function(*args, result_original=False, result_deep_original=False)

- **`result_original` (bool, optional):** If set to `True`, the function's result will be unjsified using `unjsify`. This means that any `Object` instances in the result will be converted back to their original Python forms (e.g., dictionaries, lists, tuples).

- **`result_deep_original` (bool, optional):** If set to `True`, the function's result will be deeply unjsified using `deep_unjsify`. This recursively converts all nested `Object` instances within the result back to their original Python forms.

**Basic Usage of `jsified_function`**

To use `jsified_function`, simply apply the decorator to your function. When the function is called, any arguments that are dictionaries, lists, or tuples will be automatically converted to their jsified counterparts.

**Example:**

.. code-block:: python

    from jsify import Object
    from jsify.calls import jsified_function

    @jsified_function
    def process_data(data):
        # Accessing keys with attribute-style access
        return data.key1 + data.key2

    # Native Python dictionary
    data = {'key1': 10, 'key2': 20}

    # Call the decorated function
    result = process_data(data)
    print(result)  # Outputs: 30

In this example, the `process_data` function receives a dictionary as input. The `jsified_function` decorator converts this dictionary into a `Dict`, allowing you to access the keys using attribute-style access.

**Customizing the Function's Return Value**

You can control how the function's return value is processed by using the `result_original` and `result_deep_original` parameters.

**Example:**

.. code-block:: python

    @jsified_function(result_original=True)
    def get_data():
        return {'key1': 'value1', 'key2': 'value2'}

    result = get_data()
    print(result)  # Outputs: {'key1': 'value1', 'key2': 'value2'} (original dict)

    @jsified_function(result_deep_original=True)
    def get_nested_data():
        return {'outer': {'inner': {'key': 'value'}}}

    result = get_nested_data()
    print(result)
    # Outputs: {'outer': {'inner': {'key': 'value'}}} (deeply unjsified)

In the first example, `result_original=True` ensures that the function returns the original dictionary instead of a `Dict`. In the second example, `result_deep_original=True` ensures that the entire nested structure is deeply unjsified, converting all `Object` instances back to their original forms.
