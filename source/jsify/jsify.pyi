from typing import Any, Iterator as Iter, Tuple as Tup


class Object:
    """
    JSON-like wrapper for any Python object with attribute and item access.

    This class provides a generic, dictionary-like wrapper for any Python object.
    It allows both attribute-style and item-style access to the wrapped object.
    Most operations are redirected to the original object.

    Parameters
    ----------
    obj : Any
        The Python object to wrap. Can be any type; most commonly dict, list, or tuple.

    Examples
    --------
    >>> o = Object({'a': 1, 'b': 2})
    >>> o.a
    1
    >>> o['b']
    2

    Notes
    -----
    - Arithmetic and comparison operators are forwarded to the wrapped object.
    - Attribute and item setting is supported if the underlying object allows it.
    - Use `unjsify(obj)` to extract the original object.
    """
    def __init__(self, obj):...

class Dict(Object):
    """
    JSON-like dictionary with attribute access.

    This class wraps a Python dictionary and allows both attribute-style and item-style
    access to its keys and values. It inherits all behavior from `Object` and adds special
    support for dictionary operations.

    Parameters
    ----------
    obj : dict or mapping
        The Python dictionary or mapping to wrap.
    **kwargs
        Additional key-value pairs to include in the wrapped dictionary.

    Examples
    --------
    >>> d = Dict(a=1, b=2)
    >>> d.a
    1
    >>> d['b']
    2
    >>> d.__dict__
    {'a': 1, 'b': 2}

    Notes
    -----
    - Accessing `__dict__` returns the underlying dictionary.
    - All standard mapping and attribute operations are supported.
    - Additional keyword arguments in the constructor are merged into the dictionary.
    """
    def __init__(self, obj: dict, **kwargs): ...

class Tuple:
    """
    JSON-like tuple object with attribute access.

    This class wraps a Python tuple and allows attribute-style and item-style
    access to its elements. It inherits from `Object` and provides tuple-specific
    methods and operations.

    Methods
    -------
    count(value)
        Return the number of occurrences of value.
    index(value)
        Return the index of the first occurrence of value.

    Examples
    --------
    >>> t = Tuple((1, 2, 3, 2))
    >>> t[1]
    2
    >>> t.count(2)
    2
    >>> t.index(3)
    2

    Notes
    -----
    - Supports all sequence operations provided by `Object`.
    - Can be used interchangeably with Python tuples in most contexts.
    - Attribute access is supported for custom fields, if present.
    """

    def count(self, value):
        """
        Return the number of occurrences of value.

        Parameters
        ----------
        value : Any
            The value to count.

        Returns
        -------
        int
            Number of occurrences of value.
        """
        ...

    def index(self, value):
        """
        Return the index of the first occurrence of value.

        Parameters
        ----------
        value : Any
            The value to find.

        Returns
        -------
        int
            Index of the first occurrence.

        Raises
        ------
        ValueError
            If the value is not present.
        """
        ...

    def __init__(self, obj: tuple): ...

class List:
    """
    JSON-like list with attribute access.

    This class wraps a Python list and allows both attribute-style and item-style access to its elements.
    It inherits from `Object` and adds standard mutable list operations.

    Methods
    -------
    append(obj)
        Append an object to the end of the list.
    clear()
        Remove all items from the list.
    count(value)
        Return the number of occurrences of value.
    extend(iterable)
        Extend the list by appending elements from the iterable.
    index(value)
        Return the index of the first occurrence of value.
    insert(index, obj)
        Insert an object at a given position.
    pop([index])
        Remove and return the item at the given position (default last).
    remove(value)
        Remove the first occurrence of value.
    reverse()
        Reverse the list in place.
    sort(...)
        Sort the list in place.
    copy()
        Return a shallow copy of the list.
    __dir__()
        Return a tuple of stringified integer indices.

    Parameters
    ----------
    obj : list or iterable
        The Python list or iterable to wrap.

    Examples
    --------
    >>> l = List([1, 2, 3])
    >>> l.append(4)
    >>> l[2]
    3
    >>> l.count(2)
    1
    >>> l.index(3)
    2
    >>> l.__dir__()
    ('0', '1', '2', '3')

    Notes
    -----
    - List indices can be accessed as attributes or items.
    - All mutable list operations are supported and forwarded to the underlying list.
    - Supports attribute-style access for custom fields, if present.
    """

    def append(self, obj):
        """Append an object to the end of the list."""
        ...

    def clear(self):
        """Remove all items from the list."""
        ...

    def count(self, value):
        """Return the number of occurrences of value."""
        ...

    def extend(self, iterable):
        """Extend the list by appending elements from the iterable."""
        ...

    def index(self, value):
        """Return the index of the first occurrence of value."""
        ...

    def insert(self, index, obj):
        """Insert an object at a given position."""
        ...

    def pop(self, index=-1):
        """Remove and return the item at the given position (default last)."""
        ...

    def remove(self, value):
        """Remove the first occurrence of value."""
        ...

    def reverse(self):
        """Reverse the list in place."""
        ...

    def sort(self, *args, **kwargs):
        """Sort the list in place."""
        ...

    def copy(self):
        """Return a shallow copy of the list."""
        ...

    def __init__(self, obj: list): ...


class Iterator:
    """
    Iterator with jsify wrapping.

    This class wraps a Python iterable or iterator and returns jsified objects on iteration.
    Each value produced by the underlying iterator is automatically wrapped as a jsified object.

    Parameters
    ----------
    obj : iterable or iterator
        The Python object to iterate over.

    Examples
    --------
    >>> it = Iterator([1, 2, 3])
    >>> next(it)
    1
    >>> list(it)
    [2, 3]

    Notes
    -----
    - This class implements the iterator protocol (`__iter__` and `__next__`).
    - All yielded values are wrapped with `jsify`.
    """
    def __init__(self, obj):
        ...


Undefined = Object(None)

def jsify(onj) -> Object:
    """
    Wrap a Python object in a jsify wrapper.

    This function returns a new jsified object. Dictionaries, lists, and tuples are wrapped in
    special jsified classes, while basic types (None, int, float, complex, str, bool) and objects
    already wrapped as Object are returned as-is.

    Parameters
    ----------
    onj : Any
        Python object to be wrapped.

    Returns
    -------
    Object
        Jsified object instance.

    Notes
    -----
    Unsupported types raise TypeError.
    """
    ...

def unjsify(obj: Object):
    """
    Return the original object from an Object wrapper.

    If the input is a jsified Object, its original Python value is extracted and returned.
    If the input is not a jsified object, it is returned as-is.

    Parameters
    ----------
    obj : Object or Any
        Jsified object or any Python object.

    Returns
    -------
    Any
        Original Python object (deeply unwrapped).
    """
    ...

def jsified_copy(obj) -> Object:
    """
    Create a shallow jsified copy of the given object.

    The copy is performed on the unjsified (original) object and the result is wrapped again
    as a jsified object.

    Parameters
    ----------
    obj : Object or Any
        Jsified or plain Python object.

    Returns
    -------
    Object
        Shallow copy, wrapped as jsified object.
    """
    ...

def jsified_deepcopy(obj) -> Object:
    """
    Create a deep jsified copy of the given object.

    The copy is performed on the unjsified (original) object and the result is wrapped again
    as a jsified object.

    Parameters
    ----------
    obj : Object or Any
        Jsified or plain Python object.

    Returns
    -------
    Object
        Deep copy, wrapped as jsified object.
    """
    ...

def jsified_get(ogj: dict, key: Any, default: Any = None) -> Object:
    """
    Get the value for a key from a jsified dictionary with optional default.

    The value is returned as a jsified object. If the key does not exist, the default is returned.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.
    key : Any
        The key to look up.
    default : Any, optional
        Value to return if key does not exist (default is None).

    Returns
    -------
    Object
        Value associated with the key, wrapped as jsified object.
    """
    ...

def jsified_pop(ogj: dict, key: Any, default: Any = None) -> Object:
    """
    Remove the specified key and return the corresponding value as a jsified object.

    If key is not found, default is returned if provided, otherwise KeyError is raised.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.
    key : Any
        The key to remove.
    default : Any, optional
        Value to return if key does not exist.

    Returns
    -------
    Object
        The removed value, wrapped as jsified object.
    """
    ...

def jsified_popitem(ogj: dict) -> Object:
    """
    Remove and return an arbitrary (key, value) pair from a jsified dictionary.

    The pair is returned as a jsified object. If the dictionary is empty, raises KeyError.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.

    Returns
    -------
    Object
        The removed (key, value) pair, wrapped as jsified object.
    """
    ...

def jsified_setdefault(ogj: dict, key: Any, default: Any = None) -> None:
    """
    Insert a key with a value of default if key is not in the dictionary.

    The value for the key is returned as a jsified object.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.
    key : Any
        The key to set.
    default : Any, optional
        Value to set if key does not exist.

    Returns
    -------
    None
    """
    ...

def jsified_update(ogj: dict, values: Any) -> None:
    """
    Update the dictionary with the key/value pairs from values.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.
    values : dict or iterable
        Dictionary or iterable of key/value pairs.

    Returns
    -------
    None
    """
    ...

def jsified_values(ogj: dict) -> Iter[Any]:
    """
    Return an iterator over the dictionary’s values.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.

    Returns
    -------
    Iterator[Any]
        Iterator over values.
    """
    ...

def jsified_keys(ogj: dict) -> Iter[str]:
    """
    Return an iterator over the dictionary’s keys.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.

    Returns
    -------
    Iterator[str]
        Iterator over keys.
    """
    ...

def jsified_items(ogj: dict) -> Iter[Tup[str, Any]]:
    """
    Return an iterator over the dictionary’s (key, value) pairs.

    Parameters
    ----------
    ogj : dict or Object
        Jsified dictionary or plain Python dict.

    Returns
    -------
    Iterator[Tuple[str, Any]]
        Iterator over (key, value) pairs.
    """
    ...

