"""
This module provides utilities for deserializing JSON content into Python objects with enhanced usability.
Specifically, it converts dictionaries from JSON data into `SimpleNamespace` objects, allowing for attribute-style
access to dictionary keys. This approach is particularly useful for developers who prefer dot notation
over traditional dictionary key access.

The module wraps the standard `json.load` and `json.loads` functions, integrating an `object_hook` that
automatically transforms dictionaries into `SimpleNamespace` instances during deserialization.
This makes the resulting objects easier to work with, especially in scenarios where readability and
code simplicity are important.
"""

from types import SimpleNamespace
from jsify.encoder import _orig_load, _orig_loads


def object_hook_convert_to_simple(obj):
    """
    Convert a dictionary to a SimpleNamespace object.

    This function is used as an object hook during JSON deserialization to convert
    dictionaries into SimpleNamespace objects, allowing for attribute-style access.

    :param obj: The dictionary object to be converted.
    :type obj: dict
    :return: A SimpleNamespace object with the dictionary's key-value pairs as attributes.
    :rtype: SimpleNamespace
    """
    if isinstance(obj, dict):
        return SimpleNamespace(**obj)


def load(fp, *args, **kwargs):
    """
    Deserialize JSON content from a file pointer, converting dictionaries to SimpleNamespace.

    This function wraps the original `json.load` function and uses `object_hook_convert_to_simple`
    to convert all dictionaries in the JSON data to SimpleNamespace objects.

    :param fp: The file pointer to read JSON data from.
    :type fp: file-like object
    :return: The deserialized JSON content with dictionaries converted to SimpleNamespace.
    :rtype: SimpleNamespace or other JSON-compatible data structures
    """
    return _orig_load(fp, *args, object_hook=object_hook_convert_to_simple, **kwargs)


def loads(s, *args, **kwargs):
    """
    Deserialize JSON content from a string, converting dictionaries to SimpleNamespace.

    This function wraps the original `json.loads` function and uses `object_hook_convert_to_simple`
    to convert all dictionaries in the JSON string to SimpleNamespace objects.

    :param s: The JSON string to deserialize.
    :type s: str
    :return: The deserialized JSON content with dictionaries converted to SimpleNamespace.
    :rtype: SimpleNamespace or other JSON-compatible data structures
    """
    return _orig_loads(s, *args, object_hook=object_hook_convert_to_simple, **kwargs)
