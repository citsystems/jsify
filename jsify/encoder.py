"""
The `encoder` module provides custom JSON serialization functionality specifically designed to handle `JsonObject`
instances. This module extends Python's built-in `json` module to ensure that `JsonObject` instances are correctly
converted into their original dictionary representation during the serialization process.
The module features the `JsonObjectEncoder` class, which overrides the default JSON encoding behavior to accommodate
`JsonObject` instances. Additionally, it provides custom `dump` and `dumps` functions that leverage this encoder,
allowing seamless integration with standard JSON serialization workflows.
You must import this module if you want to use serialization done by json module.
"""

import json
from typing import Any

from .jsify import JsonObject


class JsonObjectEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for JsonObject instances.

    This encoder converts JsonObject instances to their original dictionary representation
    for JSON serialization.

    Methods
    -------
    default(o: Any) -> Any
        Overrides the default method of JSONEncoder to handle JsonObject instances.
    """
    def default(self, o: Any) -> Any:
        if isinstance(o, JsonObject):
            return o.__orig__
        else:
            return super().default(o)


_orig_dump = json.dump
_orig_dumps = json.dumps


def dumps(o, **kwargs):
    """
    Serialize `o` to a JSON formatted `str` using JsonObjectEncoder.

    Parameters
    ----------
    o : Any
        The object to serialize.
    **kwargs
        Additional keyword arguments passed to `json.dumps`.

    Returns
    -------
    str
        The JSON formatted string.
    """
    return _orig_dumps(o, cls=JsonObjectEncoder, **kwargs)


def dump(o, fp, **kwargs):
    """
    Serialize `o` as a JSON formatted stream to `fp` using JsonObjectEncoder.

    Parameters
    ----------
    o : Any
        The object to serialize.
    fp : file-like object
        The file-like object to which the JSON formatted stream is written.
    **kwargs
        Additional keyword arguments passed to `json.dump`.

    Returns
    -------
    None
    """
    return _orig_dump(o, fp, cls=JsonObjectEncoder, **kwargs)


# Override the default json.dump and json.dumps with the custom implementations
json.dump = dump
json.dumps = dumps

# Set the default method of JSONEncoder to handle JsonObject instances
json.JSONEncoder.default = JsonObjectEncoder.default
