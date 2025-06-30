import timeit
from jsify import Object  # Import Object class from jsify

# Setup code for both scratches (outside the timeit measurement)
setup_dict = """
data = {"name": "Alice", "age": 25}
"""

setup_jsify = """
from types import SimpleNamespace
data = SimpleNamespace(name= "Alice", age= 25)
"""

# Measure the time taken to access elements in a standard dictionary
dict_test = timeit.timeit(
    """
name = data["name"]
age = data["age"]
""",
    setup=setup_dict,
    number=1000000,
)

# Measure the time taken to access elements in a jsify Object
jsify_test = timeit.timeit(
    """
name = data.name
age = data.age
""",
    setup=setup_jsify,
    number=1000000,
)

# Output the results
print(f"Standard dictionary access: {dict_test:.6f} seconds")
print(f"Jsify object access: {jsify_test:.6f} seconds")
