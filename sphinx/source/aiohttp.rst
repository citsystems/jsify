.. _aiohttp:

.. meta::
   :keywords: Jsify, aiohttp, Python, API, JSON, web development, decorator, attribute access, dot notation
   :description: Learn how to create a flexible API using Jsify and aiohttp. This guide shows how to handle JSON data with Python, enabling dot notation access through decorators like json_function, camelized_function, and jsified_function.

Creating flexible API with `Jsify` and `aiohttp`
================================================

This example demonstrates how to create an API function using `jsify` that can be called either from a standard Python program or through an HTTP request using `aiohttp`.

**Defining the API Function:**

.. code-block:: python

    from jsify.simple import loads
    from jsify.calls import json_function, camelized_function, jsified_function

    @json_function
    @camelized_function
    def api_simple_function(user_name, user_details, **kwargs):
        return f"Name: {user_name} " \
                f"Age: {user_details.age} " \
                f"City: {user_details.city} "

This function can be called in multiple ways, showcasing its flexibility:

1. **Standard Python Call:** The function can be called directly with Python objects:

   .. code-block:: python

       from types import SimpleNamespace as sn
       api_simple_function(user_name="Charlie", user_details=sn(age=32, city="Warsaw"))

   This direct call uses `SimpleNamespace` to pass the user details.

2. **HTTP Request Handling with Aiohttp:** The function can be connected to an `aiohttp` route and called through an HTTP POST request:

   .. code-block:: python

       from aiohttp import web
       from jsify.simple import loads

       def json_request(f):
           async def handler(request: web.Request):
               return web.Response(text=f(_json=loads(await request.text())))
           return handler

       app = web.Application()
       app.add_routes([web.post('/process_user_info', json_request(api_simple_function))])
       web.run_app(app)

   You can make a POST request to `/process_user_info` with a JSON body, such as:

   .. code-block:: json

      {
          "userName": "Charlie",
          "userDetails": {
              "age": 32,
              "city": "Warsaw"
          }
      }

3. **Using `jsified_function` Decorator:** To allow the function to accept regular Python dictionaries as input but work with dot notation inside the function, you can use the `jsified_function` decorator:

   .. code-block:: python

       from jsify.simple import loads, jsify
       from jsify.calls import jsified_function

       @json_function
       @camelized_function
       @jsified_function
       def api_simple_function(user_name, user_details, **kwargs):
           return f"Name: {user_name} " \
                  f"Age: {user_details.age} " \
                  f"City: {user_details.city} "

       # Using the function with a regular dictionaries
       result = api_simple_function(
            user_name="Charlie",
            user_details={"age":32, "city": "Warsaw"})
       print(result)

   In this case, the `jsified_function` decorator automatically converts the dictionary into a Jsified `Object` within the function, allowing dot notation access without manually converting the input.

**Explanation:**

- **Flexible API Usage:** The function `api_simple_function` is highly flexible, allowing it to be used directly in Python, integrated into a web service via `aiohttp`, or handling regular Python dictionaries with internal dot notation access.
- **Dot Notation with Jsify `Object`:** The `jsified_function` decorator ensures that even if dictionaries are passed, the function can work with them as if they were objects with dot notation, enhancing code readability and usability.

This setup allows for a versatile API function that can adapt to various usage scenarios, simplifying JSON handling and improving the overall developer experience.
