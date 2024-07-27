from .jsify import unjsify, JsonObject, deep_unjsify


def jsified_function(*args, result_original=False, result_deep_original=False):
    """
    A decorator to convert function arguments to `JsonObject` and process the results accordingly.

    This decorator can be applied to a function to ensure that its arguments are automatically
    converted to `JsonObject` instances if they are of types `dict`, `list`, or `tuple`. It also
    processes the function's result based on the provided flags.

    Parameters
    ----------
    *args : tuple
        Positional arguments that may include the function to be decorated.
    result_original : bool, optional
        If True, the function's result will be unjsified using `unjsify`. Default is False.
    result_deep_original : bool, optional
        If True, the function's result will be deeply unjsified using `deep_unjsify`. Default is False.

    Returns
    -------
    function
        The decorated function with arguments converted to `JsonObject` and results processed based on the flags.
    """
    def create_decorator():
        def decorator(function):
            def wrapper(*wrapper_args, **kwargs):
                def conditional_json_object(o):
                    return JsonObject(o) if isinstance(o, (dict, list, tuple)) else o
                json_args = list(map(lambda a: conditional_json_object(a), wrapper_args))
                json_kwargs = dict(map(lambda item: (item[0], conditional_json_object(item[1])), kwargs.items()))
                result = function(*json_args, **json_kwargs)
                return deep_unjsify(result) if result_deep_original \
                    else unjsify(result) if result_original \
                    else JsonObject(result)
            return wrapper
        return decorator
    if len(args):
        return create_decorator()(function=args[0])
    else:
        return create_decorator()
