import inspect
import sys
from jsify import jsify, Undefined


def linux_pycharm_like_inspect(obj, max_depth=2, _depth=0, _visited=None):
    """
    Simulates PyCharm Debugger object inspection.
    The goal is to REPRODUCE debugger crashes on jsify objects.
    """

    if _visited is None:
        _visited = set()

    if id(obj) in _visited:
        return "<recursion>"
    _visited.add(id(obj))

    if _depth >= max_depth:
        return f"<depth {max_depth} reached>"

    result = {}

    # 1. TYPE
    result["type"] = str(type(obj))

    # 2. DIR()  ← PyCharm always calls this first
    try:
        attrs = dir(obj)
        result["dir"] = attrs
    except Exception as e:
        result["dir_error"] = repr(e)
        attrs = []

    # 3. REPR  ← PyCharm tries to show preview of value
    try:
        result["repr"] = repr(obj)
    except Exception as e:
        result["repr_error"] = repr(e)

    # 4. ITERATOR CHECK  ← a lot of internal pycharm code relies on this
    try:
        it = iter(obj)
        # test first element (PyCharm does this!)
        try:
            first = next(it)
            result["iter_first"] = linux_pycharm_like_inspect(first, max_depth, _depth + 1, _visited)
        except Exception as e:
            result["iter_first_error"] = repr(e)
    except Exception as e:
        result["iter_error"] = repr(e)

    # 5. GETATTR on all names from dir()  ← the real killer for jsify
    getattr_results = {}
    for name in attrs:
        if name.startswith("__") and name.endswith("__"):
            # PyCharm also reads magic attributes
            pass

        try:
            val = getattr(obj, name)
            getattr_results[name] = linux_pycharm_like_inspect(val, max_depth, _depth + 1, _visited)
        except Exception as e:
            getattr_results[name] = f"<error {repr(e)}>"

    result["getattr"] = getattr_results

    # 6. MAPPING PROTOCOL TESTS  (__getitem__ with sample keys)
    test_keys = ["a", "test", "_pydevd", 0, 1]
    getitem_results = {}
    for key in test_keys:
        try:
            val = obj[key]
            getitem_results[key] = linux_pycharm_like_inspect(val, max_depth, _depth + 1, _visited)
        except Exception as e:
            getitem_results[key] = f"<error {repr(e)}>"

    result["getitem"] = getitem_results

    return result

from jsify import jsify, Dict, List, Tuple, Iterator, Undefined


def build_jsify_debug_test_objects():
    # Base plain literals
    plain_literals = {
        "int": 42,
        "float": 3.14,
        "str": "hello",
        "bool": True,
        "none": None,
        "undefined": Undefined,
    }

    # Plain containers
    plain_dict = {
        "a": 1,
        "b": "text",
        "c": None,
        "d": Undefined,
        "nested_list": [1, 2, 3],
        "nested_dict": {"x": 10, "y": 20},
    }

    plain_list = [
        1,
        "two",
        None,
        Undefined,
        {"k": "v"},
        [7, 8, 9],
        (1, 2, 3),
    ]

    plain_tuple = (
        1,
        "two",
        None,
        Undefined,
        {"k": "v"},
        [7, 8, 9],
    )

    plain_iter = iter([
        1,
        "two",
        None,
        {"nested": [1, 2, 3]},
        Undefined,
    ])

    # Jsified top-level containers
    j_dict = jsify(plain_dict)      # jsify.Dict
    j_list = jsify(plain_list)      # jsify.List
    j_tuple = jsify(plain_tuple)    # jsify.Tuple
    j_iter = jsify(plain_iter)      # jsify.Iterator

    # Mixed / nested structures
    mixed_dict = {
        "plain_literals": plain_literals,
        "plain_dict": plain_dict,
        "plain_list": plain_list,
        "plain_tuple": plain_tuple,
        "j_dict": j_dict,
        "j_list": j_list,
        "j_tuple": j_tuple,
        "j_iter": j_iter,
        "deep_nested": {
            "dict_in_list": [plain_dict, j_dict, 123, Undefined],
            "list_in_dict": {"l1": plain_list, "l2": j_list},
            "tuple_mix": (plain_tuple, j_tuple, "end"),
        },
    }

    mixed_list = [
        plain_literals,
        plain_dict,
        plain_list,
        plain_tuple,
        j_dict,
        j_list,
        j_tuple,
        j_iter,
        {"wrap_mixed_dict": mixed_dict},
    ]

    j_mixed_dict = jsify(mixed_dict)
    j_mixed_list = jsify(mixed_list)

    all_objects = jsify({
        # Plain
        "plain_literals": plain_literals,
        "plain_dict": plain_dict,
        "plain_list": plain_list,
        "plain_tuple": plain_tuple,
        "plain_iter": iter([
            1,
            "two",
            None,
            {"nested": [1, 2, 3]},
            Undefined,
        ]),

        # Simple jsified containers
        "j_dict": j_dict,
        "j_list": j_list,
        "j_tuple": j_tuple,
        "j_iter": jsify(iter([
            1,
            "two",
            None,
            {"nested": [1, 2, 3]},
            Undefined,
        ])),

        # Mixed / nested jsified structures
        "j_mixed_dict": j_mixed_dict,
        "j_mixed_list": j_mixed_list,
    })

    return all_objects


def simulate_pydevd_windows(obj, max_depth=4, _depth=0, seen=None):
    """
    Simulates Windows pydevd debugger object inspection.
    This is intentionally dangerous and may loop/hang/crash exactly
    like Windows debugger does on jsify objects.

    Behaviour reproduced:
    - deep dir() scanning
    - getattr on *ALL* names returned by dir()
    - getattr on pydevd synthetic names (_pydevd_*)
    - item access tests (["0"], ["1"], ["a"], ["_pydevd_id"], etc.)
    - repr() preview
    - iter() + next()
    - fallback recursion (value-of-value)
    """

    if seen is None:
        seen = set()

    oid = id(obj)
    if oid in seen:
        return "<recursion>"
    seen.add(oid)

    if _depth >= max_depth:
        return "<max_depth>"

    out = {}

    # 1. TYPE
    out["type"] = str(type(obj))

    # 2. repr() — Windows debugger ALWAYS tries preview
    try:
        out["repr"] = repr(obj)
    except Exception as e:
        out["repr_error"] = repr(e)

    # 3. dir() — Windows version reads EVERYTHING
    try:
        names = dir(obj)
    except Exception as e:
        out["dir_error"] = repr(e)
        names = []

    out["dir"] = names

    # 4. pydevd synthetic attribute checks
    pydevd_names = [
        "_pydevd_id",
        "_pydevd_frame_eval",
        "_pydevd_internal",
        "_pydevd_resolver",
        "_pydevd_xml",
        "_pydevd_tmp",
        "__getattribute__",
        "__getattr__",
        "__setattr__",
        "__getitem__",
        "__iter__",
    ]

    # merge the two lists - Windows debugger does this too
    synthetic = list(dict.fromkeys(names + pydevd_names))

    # 5. getattr on each name
    getattr_results = {}
    for name in synthetic:
        try:
            val = getattr(obj, name)
            # Windows debugger INSPECTS THE VALUE TOO:
            getattr_results[name] = simulate_pydevd_windows(
                val, max_depth, _depth + 1, seen
            )
        except Exception as e:
            getattr_results[name] = f"<error {repr(e)}>"

    out["getattr"] = getattr_results

    # 6. getitem tests — Windows debugger does this blindly
    #    It tries indexes and string keys, including _pydevd_* keys.
    test_keys = [
        0, 1, 2,
        "0", "1", "2",
        "a", "b", "c",
        "_pydevd_id", "_pydevd_frame_eval",
        "__dict__", "__class__",
    ]

    getitem_results = {}
    for key in test_keys:
        try:
            val = obj[key]
            getitem_results[key] = simulate_pydevd_windows(
                val, max_depth, _depth + 1, seen
            )
        except Exception as e:
            getitem_results[key] = f"<error {repr(e)}>"

    out["getitem"] = getitem_results

    # 7. iter(obj) and next()
    try:
        it = iter(obj)
        out["iter"] = str(type(it))
        try:
            first = next(it)
            out["iter_first"] = simulate_pydevd_windows(
                first, max_depth, _depth + 1, seen
            )
        except Exception as e:
            out["iter_first_error"] = repr(e)
    except Exception as e:
        out["iter_error"] = repr(e)

    return out


import jsify as jsify_mod

obj = build_jsify_debug_test_objects()

linux_pycharm_like_inspect(obj)

simulate_pydevd_windows(obj, max_depth=10)

pass