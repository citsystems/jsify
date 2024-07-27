import re


def camel_case_json_function(replace=None):
    """
    A decorator to convert the keys of JSON-like dictionaries from camelCase to snake_case before passing them to the function.

    Parameters
    ----------
    replace : dict, optional
        A dictionary to specify replacements for certain keys after conversion to snake_case.

    Returns
    -------
    function
        A decorator that applies the conversion to the decorated function's keyword arguments.
    """
    def wrapper_with_parameters(func):
        def wrapper(**kwargs):
            return func(**json_camel_to_snake(kwargs, replace=replace))
        return wrapper
    return wrapper_with_parameters


camel_to_snake_regex = re.compile(r'(?<!^)(?=[A-Z])')


def text_camel_to_snake(text, replace=None):
    """
    Converts a camelCase string to snake_case.

    Parameters
    ----------
    text : str
        The camelCase string to be converted.
    replace : dict, optional
        A dictionary to specify replacements for certain keys after conversion to snake_case.

    Returns
    -------
    str
        The converted snake_case string.
    """
    snake_case = camel_to_snake_regex.sub('_', text).lower()
    return snake_case if replace is None or snake_case not in replace else replace[snake_case]


def json_camel_to_snake(json, replace=None):
    """
    Converts the keys of a JSON-like dictionary from camelCase to snake_case.

    Parameters
    ----------
    json : dict
        The JSON-like dictionary with camelCase keys to be converted.
    replace : dict, optional
        A dictionary to specify replacements for certain keys after conversion to snake_case.

    Returns
    -------
    dict
        The JSON-like dictionary with keys converted to snake_case.
    """
    snake_case_json = {}
    for key, value in json.items():
        snake_case_json[text_camel_to_snake(key, replace)] = value
    return snake_case_json


def text_snake_to_lower_camel(text, replace=None):
    """
    Converts a snake_case string to lowerCamelCase.

    Parameters
    ----------
    text : str
        The snake_case string to be converted.
    replace : dict, optional
        A dictionary to specify replacements for certain keys after conversion to lowerCamelCase.

    Returns
    -------
    str
        The converted lowerCamelCase string.
    """
    components = text.split('_')
    lower_camel_case = components[0] + ''.join(x.title() for x in components[1:])
    return lower_camel_case if replace is None or lower_camel_case not in replace else replace[lower_camel_case]
