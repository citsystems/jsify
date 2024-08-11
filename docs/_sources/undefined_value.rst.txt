.. _undefined_value:

.. meta::
   :keywords: Jsify, Python, Undefined value, JSON-like data, error prevention, singleton, JavaScript, data structures, optional fields, data handling
   :description: Learn about the Undefined value in the Jsify library, which mimics JavaScript's undefined. This guide explains how to use Undefined as a placeholder for missing or optional data, its behavior in data structures, and how it helps prevent errors when accessing non-existent properties.

`Undefined` Value
===================================

The Jsify library introduces a special `Undefined` value, which behaves similarly to the `undefined` value in JavaScript. This is particularly useful in scenarios where you need a placeholder for "no value" or when dealing with optional data in JSON-like structures.

The `Undefined` Class
---------------------

The `Undefined` value is an instance of the `UndefinedClass`, a singleton class designed to mimic the behavior of JavaScript's `undefined`. It ensures that only one instance of `Undefined` exists throughout your application, providing a consistent and reliable way to represent the absence of a value.

**Key Characteristics:**

- **Singleton Instance:** There is only one instance of `Undefined`, ensuring consistency across your codebase.
- **JavaScript-like Behavior:** `Undefined` returns itself for any attribute or item access, evaluates to `False` in a boolean context, and is considered equal to `None` and other `Undefined` instances.
- **Safe Usage:** It allows you to safely check for "no value" scenarios without the risk of raising exceptions or encountering unexpected behavior.

**Basic Usage of `Undefined`**

The `Undefined` value can be used as a placeholder when you want to explicitly indicate that a value is not defined, similar to how `None` is used in Python but with behavior more aligned to JavaScript's `undefined`.

**Example:**

.. code-block:: python

    from jsify import Undefined

    # Assigning Undefined to a variable
    value = Undefined

    # Checking if the value is Undefined
    if value is Undefined:
        print("The value is Undefined.")
        # Outputs: The value is Undefined.

    # Undefined is considered False in boolean context
    if not value:
        print("Undefined evaluates to False.")
        # Outputs: Undefined evaluates to False.

**Returning `Undefined` for Missing Properties**

In standard Python, accessing a non-existent attribute on an object typically raises an `AttributeError`, and accessing a non-existent key in a dictionary raises a `KeyError`. However, jsified objects are designed to mimic the behavior of JavaScript objects, where accessing a missing property simply returns `undefined`.

**Advantages of This Behavior:**

- **Error Prevention:** Avoids runtime errors that would normally occur when trying to access missing attributes or keys, making your code more robust.
- **Flexible Data Access:** Allows you to safely navigate through deeply nested data structures without worrying about missing intermediate properties.
- **Consistent Handling:** Provides a consistent mechanism for dealing with optional or dynamically structured data, where some fields may not always be present.

**Example:**

.. code-block:: python

    from jsify import jsify, Undefined

    # Example data
    data = {
        'name': 'Alice',
        'details': {
            'age': 30,
            'city': 'Wonderland'
        }
    }

    # Convert to a jsified object
    json_obj = jsify(data)

    # Accessing an existing property
    print(json_obj.name)  # Outputs: Alice

    # Accessing a non-existent property
    print(json_obj.non_existent_property)  # Outputs: Undefined

    # Checking if the returned value is Undefined
    if json_obj.non_existent_property is Undefined:
        print("The property is not defined.")
        # Outputs: The property is not defined.

**Interacting with `Undefined`**

`Undefined` is designed to safely return itself when accessed via attributes or indexing, making it useful in nested data structures where some values might be intentionally left undefined.

**Example:**

.. code-block:: python

    # Accessing attributes on Undefined
    print(Undefined.some_attribute)  # Outputs: Undefined
    print(Undefined['some_key'])     # Outputs: Undefined

    # Undefined always returns itself
    result = Undefined.some_method().another_attribute
    print(result)  # Outputs: Undefined

**Navigating Nested Undefined Properties**

This behavior is particularly useful when dealing with nested data structures. You can safely navigate through multiple levels of nested objects without worrying about whether each intermediate property exists.

**Example:**

.. code-block:: python

    # Accessing a deeply nested property
    print(json_obj.details.country)  # Outputs: Undefined

    # Combining nested access with property-style access
    result = json_obj.details.country.code
    print(result)  # Outputs: Undefined

    # Checking if a deeply nested property is Undefined
    if json_obj.details.country.code is Undefined:
        print("The nested property is not defined.")
        # Outputs: The nested property is not defined.

**Implications for Data Processing**

This behavior means that when processing data with jsified objects, you do not need to perform repeated checks for the existence of properties. Instead, you can directly access the properties, and if any are missing, `Undefined` is returned without causing an error.

**Example:**

.. code-block:: python

    # Example processing function
    def process_user_info(user):
        # Safely accessing nested properties
        age = user.details.age if user.details.age is not Undefined else "Unknown"
        city = user.details.city if user.details.city is not Undefined else "Unknown"
        country = user.details.country if user.details.country is not Undefined else "Unknown"

        print(f"User is {age} years old, lives in {city}, {country}.")

    # Processing the jsified object
    process_user_info(json_obj)
    # Outputs: User is 30 years old, lives in Wonderland, Unknown.

**Comparing `Undefined`**

The `Undefined` value is equal to `None` and to any other instance of `Undefined`. This allows for flexible comparison operations when checking for the presence or absence of values.

**Example:**

.. code-block:: python

    # Undefined is equal to None
    print(Undefined == None)  # Outputs: True

    # Undefined is not None
    print(Undefined is None)  # Outputs: False

**Handling `Undefined` in JSON-like Structures**

When working with JSON-like data structures, `Undefined` can be used to represent fields that are not set or to handle optional fields that may or may not be present. This can be particularly useful when parsing or manipulating data where some fields are optional.

**Example:**

.. code-block:: python

    from jsify import jsify, Undefined

    data = {
        'name': 'Alice',
        'optional_field': Undefined
    }

    json_obj = jsify(data)

    # Accessing an undefined field
    print(json_obj.optional_field)  # Outputs: Undefined

    # Checking if a field is Undefined
    if json_obj.optional_field is Undefined:
        print("The optional field is not set.")
        # Outputs: The optional field is not set.

**Serialization Considerations**

When serializing `Object` instances that contain `Undefined`, the `Undefined` value is typically ignored.

**Example:**

.. code-block:: python

    import json
    from jsify import jsify, Undefined

    data = {
        'name': 'Alice',
        'optional_field': Undefined
    }

    json_obj = jsify(data)

    # Serializing to JSON
    json_string = json.dumps(json_obj)
    print(json_string)
    # Outputs: {"name": "Alice"}  (optional_field is omitted or treated as null)

