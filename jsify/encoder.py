"""
The `encoder` module provides custom JSON serialization functionality specifically designed to handle `Object`
instances. This module extends Python's built-in `json` module to ensure that `Object` instances are correctly
converted into their original dictionary representation during the serialization process.

The module features the `ObjectEncoder` class, which overrides the default JSON encoding behavior to accommodate
`Object` instances. Additionally, it provides custom `dump` and `dumps` functions that leverage this encoder,
allowing seamless integration with standard JSON serialization workflows.

You must import this module if you want to use serialization done by the `json` module.
"""

import json
from types import SimpleNamespace
from typing import Any

from .jsify import Undefined, unjsify
from .jsify import Object


class ObjectEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for `Object` instances.

    This encoder converts `Object` instances to their original dictionary representation
    for JSON serialization. It also provides an option to omit fields with the `Undefined` value
    during serialization.

    Parameters
    ----------
    omit_undefined : bool
        If True, fields with the `Undefined` value are omitted from the serialized output.
    *args : tuple
        Additional positional arguments passed to `JSONEncoder`.
    **kwargs : dict
        Additional keyword arguments passed to `JSONEncoder`.

    Methods
    -------
    iterencode(o: Any, _one_shot: bool = False) -> Iterator[str]
        Encodes the object into a JSON string, applying custom logic to handle `Object`
        instances and optionally omitting `Undefined` values.
    default(o: Any) -> Any
        Overrides the default method of `JSONEncoder` to handle `Object` instances and
        `Undefined` values.
    """

    def __init__(self, omit_undefined, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.omit_undefined = omit_undefined

    def iterencode(self, o, _one_shot=False):
        if isinstance(o, Object):
            o = unjsify(o)
        if self.omit_undefined:
            if isinstance(o, tuple):
                o = o.__class__(value for value in o if value is not Undefined)
            elif isinstance(o, list):
                o = o.__class__(value for value in o if value is not Undefined)
            elif isinstance(o, dict):
                o = o.__class__({key: value for key, value in o.items() if value is not Undefined})
        return super().iterencode(o, _one_shot)

    def default(self, o: Any) -> Any:
        if o is Undefined:
            return None
        elif isinstance(o, Object):
            return o.__jsify_orig__
        elif isinstance(o, SimpleNamespace):
            return o.__dict__
        else:
            return super().default(o)


_orig_dump = json.dump
_orig_dumps = json.dumps
_orig_load = json.load
_orig_loads = json.loads


def dumps(o, *args, omit_undefined=True, **kwargs):
    """
    Serialize `o` to a JSON formatted `str` using `ObjectEncoder`.

    This function wraps `json.dumps`, providing custom serialization for `Object` instances
    and optionally omitting fields with the `Undefined` value.

    Parameters
    ----------
    o : Any
        The object to serialize.
    omit_undefined : bool, optional
        If True, fields with the `Undefined` value are omitted from the serialized output. Default is True.
    **kwargs : dict
        Additional keyword arguments passed to `json.dumps`.

    Returns
    -------
    str
        The JSON formatted string.
    """
    return _orig_dumps(o, *args, cls=ObjectEncoder, omit_undefined=omit_undefined, **kwargs)


def dump(o, *args, omit_undefined=True, **kwargs):
    """
    Serialize `o` as a JSON formatted stream to `fp` using `ObjectEncoder`.

    This function wraps `json.dump`, providing custom serialization for `Object` instances
    and optionally omitting fields with the `Undefined` value.

    Parameters
    ----------
    o : Any
        The object to serialize.
    fp : file-like object
        The file-like object to which the JSON formatted stream is written.
    omit_undefined : bool, optional
        If True, fields with the `Undefined` value are omitted from the serialized output. Default is True.
    **kwargs : dict
        Additional keyword arguments passed to `json.dump`.

    Returns
    -------
    None
    """
    return _orig_dump(o, *args, cls=ObjectEncoder, omit_undefined=omit_undefined, **kwargs)


# Override the default json.dump and json.dumps with the custom implementations
json.dump = dump
json.dumps = dumps


# Set the default method of JSONEncoder to handle Object instances
json.JSONEncoder.default = ObjectEncoder.default
