.. _assertions_usage:

Using Assertions in Jsify
=========================

The Jsify library includes a powerful assertion framework through the `Assert` class, which allows you to verify the structure and content of JSON-like objects. This is particularly useful in testing scenarios where you need to ensure that your data matches expected formats or values.

**Key Concept: Assert**

The `Assert` class provides various assertion methods to check the presence or absence of keys, as well as to verify that values within a `Object` match expected values. These assertions help ensure data integrity and correctness, especially when working with complex or nested data structures.

### Basic Assertion Methods

1. **IsIn Assertion:**
   - Checks whether a specific key exists in a `Object`.
   - Raises an `AssertionError` if the key is not found.

2. **NotIn Assertion:**
   - Checks whether a specific key does not exist in a `Object`.
   - Raises an `AssertionError` if the key is found.

### Using `IsIn` and `NotIn` Assertions

The `IsIn` and `NotIn` assertions are used to verify the presence or absence of keys in your JSON-like data structures.

**Example:**

.. code-block:: python

    from jsify import jsify, Assert

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

    # Using the IsIn assertion to check for key presence
    assert_key_present = Assert.IsIn()
    assert_key_present.assertion(json_obj, 'name', 'root')  # No error

    # Using the NotIn assertion to check for key absence
    assert_key_absent = Assert.NotIn()
    assert_key_absent.assertion(json_obj, 'nonexistent', 'root')  # No error

    # This will raise an AssertionError because 'name' exists
    try:
        assert_key_absent.assertion(json_obj, 'name', 'root')
    except AssertionError as e:
        print(e)  # Outputs: root.name shouldn't be in JTO object.

### Asserting Values with `values_equal`

The `values_equal` method allows you to perform deep comparisons between a `Object` and a dictionary or list of expected values. It ensures that the structure and content of the `Object` match the expected format.

**Example:**

.. code-block:: python

    # Expected values
    expected_values = {
        'name': 'Alice',
        'details': {
            'age': 30,
            'city': 'Wonderland'
        }
    }

    # Using values_equal to assert that the values match
    try:
        Assert.values_equal(json_obj, expected_values)
        print("Assertion passed: Values match expected data.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")

    # Modifying the json_obj to introduce an error
    json_obj.details.city = 'Metropolis'

    # This will raise an AssertionError because 'city' does not match
    try:
        Assert.values_equal(json_obj, expected_values)
    except AssertionError as e:
        print(f"Assertion failed: {e}")
        # Outputs: root.details.city not equal to Metropolis

### Handling Complex Assertions

The `Assert` class is designed to handle complex data structures, including nested dictionaries and lists. You can use the provided assertions to validate that every part of your JSON-like structure adheres to the expected format.

**Example:**

.. code-block:: python

    # Complex data structure
    complex_data = {
        'user': {
            'name': 'Alice',
            'details': {
                'age': 30,
                'preferences': {
                    'colors': ['red', 'green'],
                    'languages': ['Python', 'JavaScript']
                }
            }
        }
    }

    json_obj = jsify(complex_data)

    # Expected structure
    expected_structure = {
        'user': {
            'name': 'Alice',
            'details': {
                'age': 30,
                'preferences': {
                    'colors': ['red', 'green'],
                    'languages': ['Python', 'JavaScript']
                }
            }
        }
    }

    # Using values_equal to assert the entire structure matches
    try:
        Assert.values_equal(json_obj, expected_structure)
        print("Assertion passed: Complex structure matches expected data.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
