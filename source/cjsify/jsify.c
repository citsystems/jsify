#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#include "Undefined.h"
#include "Object.h"
#include "Tuple.h"
#include "Dict.h"
#include "List.h"
#include "Iterator.h"
#include "Macro.h"

PyObject *copy_module = NULL;
PyObject *deepcopy_func = NULL;
PyObject *copy_func = NULL;

/**
 * @brief Wraps a Python object in a "jsify" wrapper if needed.
 *
 * This function returns a new reference to the object, wrapping it in a custom type
 * (DictType, ListType, or TupleType) if the object is a dict, list, or tuple.
 * For basic types (None, int, float, complex, str, bool) and objects already
 * wrapped (ObjectType), it simply returns a new reference to the original object.
 *
 * @param obj Pointer to the PyObject to be wrapped.
 * @return New reference to a PyObject* (wrapper or original); NULL on error.
 *
 * @note
 * - The returned object is always a new reference and must be decref'd by the caller.
 * - The function does not wrap types other than dict, list, or tuple.
 * - Returns Py_None (new reference) for NULL input.
 */
PyObject *jsify(PyObject *obj) {
    if (!obj)
        Py_RETURN_NONE;

    if (obj == Py_None || PyLong_Check(obj) || PyFloat_Check(obj) || PyComplex_Check(obj) ||
        PyUnicode_Check(obj) || PyBool_Check(obj) || PyObject_TypeCheck(obj, &ObjectType)) {
        Py_INCREF(obj);
        return obj;
    }

    PyObject *res = NULL;
    PyObject *args = PyTuple_Pack(1, obj);
    if (args) {
        if (PyDict_Check(obj)) {
            res = PyObject_CallObject((PyObject *)&DictType, args);
        } else if (PyList_Check(obj)) {
            res = PyObject_CallObject((PyObject *)&ListType, args);
        } else if (PyTuple_Check(obj)) {
            res = PyObject_CallObject((PyObject *)&TupleType, args);
        } else PyErr_SetString(PyExc_TypeError, "Unsupported object type for jsify");
        Py_DECREF(args);
    }
    return res;
}

/**
 * @brief Converts a Python object to a custom wrapped type, optionally passing keyword arguments.
 *
 * See jsify() function for more details.
 *
 * @param obj    Python object to wrap.
 * @param kwargs Optional keyword arguments dict (can be NULL).
 * @return New reference to wrapped object or NULL on error.
 */
PyObject *jsify_kwargs(PyObject *obj, PyObject *kwargs) {
    if (!obj)
        Py_RETURN_NONE;

    if (obj == Py_None || PyLong_Check(obj) || PyFloat_Check(obj) || PyComplex_Check(obj) ||
        PyUnicode_Check(obj) || PyBool_Check(obj) || PyObject_TypeCheck(obj, &ObjectType)) {
        Py_INCREF(obj);
        return obj;
    }
    PyObject *res = NULL;
    PyObject *args = PyTuple_Pack(1, obj);
    if (args) {
        if (PyDict_Check(obj)) {
            res = PyObject_Call((PyObject *)&DictType, args, kwargs);
        } else if (PyList_Check(obj)) {
            res = PyObject_Call((PyObject *)&ListType, args, kwargs);
        } else if (PyTuple_Check(obj)) {
            res = PyObject_Call((PyObject *)&TupleType, args, kwargs);
        } else PyErr_SetString(PyExc_TypeError, "Unsupported object type for jsify");
        Py_DECREF(args);
    }
    return res;
}

// Python-exposed function
PyObject *Py_jsify(PyObject *Py_UNUSED(self), PyObject *args, PyObject *kwargs) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args, "O", &obj))
        return NULL;
    return jsify_kwargs(obj, kwargs);
}

/**
 * @brief Returns the original object from an ObjectType wrapper, or the object itself, always with a new reference.
 *
 * If @p obj is of ObjectType, returns its 'orig' field with an incremented reference count.
 * Otherwise, returns @p obj with its reference count incremented.
 *
 * @param obj Any PyObject.
 * @return New reference to the original object or @p obj.
 */
PyObject *unjsify(PyObject *obj) {
    PyObject *orig;
    if (PyObject_TypeCheck(obj, &ObjectType)) orig = ((Object *)obj)->orig;
    else orig = obj;
    Py_INCREF(orig);
    return orig;
}

// Python-exposed function
PY_FUNCTION_O_ARGS(unjsify)

/**
 * @brief Creates a jsified copy of the given object.
 *
 * Calls the global copy_func on the original object (unjsified from @p obj),
 * decrements the temporary reference, and wraps the result with jsify.
 *
 * @param obj Any jsified or plain PyObject.
 * @return New reference to a jsified copy, or NULL on error (with Python exception set).
 */
PyObject *jsified_copy(PyObject *obj) {
    PyObject *copied;
    PyObject *orig = unjsify(obj);
    copied = PyObject_CallFunctionObjArgs(copy_func, orig, NULL);
    Py_DECREF(orig);
    RETURN_JSIFIED(copied);
}

PY_FUNCTION_O_ARGS(jsified_copy)

/**
 * @brief Creates a jsified deep copy of the given object.
 *
 * Calls the global deepcopy_func on the original object (unjsified from @p obj),
 * decrements the temporary reference, and wraps the result with jsify.
 *
 * @param obj Any jsified or plain PyObject.
 * @return New reference to a jsified deep copy, or NULL on error (with Python exception set).
 */
PyObject *jsified_deepcopy(PyObject *obj) {
    PyObject *copied;
    PyObject *orig = unjsify(obj);
    copied = PyObject_CallFunctionObjArgs(deepcopy_func, orig, NULL);
    Py_DECREF(orig);
    RETURN_JSIFIED(copied)
}

PY_FUNCTION_O_ARGS(jsified_deepcopy)

/**
 * @brief Returns a deeply unjsified copy of the given object.
 *
 * The purpose of this function is to obtain a new object tree where all references
 * to jsified wrapper objects are recursively replaced by their original Python objects.
 * This is achieved by creating a deep copy of @p obj using jsified_deepcopy(),
 * then extracting and returning the underlying original object from the copied structure.
 *
 * @param obj Any jsified or plain PyObject.
 * @return New reference to a deep-copied original object, or NULL on error (with Python exception set).
 */
PyObject *unjsify_deepcopy(PyObject *obj) {
    PyObject *copied = jsified_deepcopy(obj);
    RETURN_ORIG(copied)
}

PY_FUNCTION_O_ARGS(unjsify_deepcopy)

/**
 * @brief Retrieve a value from a dictionary-like object with support for a default value and jsify wrapping.
 *
 * This function unwraps the object (e.g., an Object type) to its original dictionary (dict),
 * then calls the `get(key, default_value)` method on it. The result is automatically
 * wrapped back as a jsified object (e.g., Object). If the given object is not a dictionary,
 * a TypeError is raised.
 *
 * @param obj           The object to search (dict or Object type).
 * @param key           The key to retrieve from the dictionary.
 * @param default_value The default value returned if the key does not exist (optional, can be NULL).
 *
 * @return The value associated with the key (jsified), the default_value, or NULL on error.
 */
PyObject *jsified_get(PyObject *obj, PyObject *key, PyObject *default_value) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result;
        if (default_value)
            result = PyObject_CallMethod(orig, "get", "OO", key, default_value);
        else
            result = PyObject_CallMethod(orig, "get", "O", key);

        Py_DECREF(orig);
        if (!result)
            return NULL;
        RETURN_JSIFIED(result)
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PyObject *Py_jsified_get(PyObject *Py_UNUSED(self), PyObject *args, PyObject *kwargs) {
    static char *kwlist[] = {"obj", "item", "default", NULL};
    PyObject *obj;
    PyObject *item;
    PyObject *default_value = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|O", kwlist, &obj, &item, &default_value))
        return NULL;

    return jsified_get(obj, item, default_value);
}

/**
 * @brief Remove and return a value from a dictionary-like object with support for a default value and jsify wrapping.
 *
 * This function unwraps the object (e.g., an Object type) to its original dictionary (dict),
 * then calls the `pop(key, default_value)` method on it. The result is automatically
 * wrapped back as a jsified object (e.g., Object). If the given object is not a dictionary,
 * a TypeError is raised.
 *
 * @param obj           The object to operate on (dict or Object type).
 * @param key           The key to remove from the dictionary.
 * @param default_value The default value returned if the key does not exist (optional, can be NULL).
 *
 * @return The removed value associated with the key (jsified), the default_value, or NULL on error.
 */
PyObject *jsified_pop(PyObject *obj, PyObject *key, PyObject *default_value) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result;
        if (default_value)
            result = PyObject_CallMethod(orig, "pop", "OO", key, default_value);
        else
            result = PyObject_CallMethod(orig, "pop", "O", key);
        Py_DECREF(orig);
        if (!result)
            return NULL;
        RETURN_JSIFIED(result)
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PyObject *Py_jsified_pop(PyObject *Py_UNUSED(self), PyObject *args, PyObject *kwargs) {
    static char *kwlist[] = {"obj", "key", "default", NULL};
    PyObject *obj;
    PyObject *key;
    PyObject *default_value = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|O", kwlist, &obj, &key, &default_value))
        return NULL;

    return jsified_pop(obj, key, default_value);
}

/**
 * @brief Remove and return an arbitrary key-value pair from a dictionary-like object (jsified).
 *
 * Unwraps the object to its original dict, calls `popitem()`, and returns the result jsified.
 * Raises TypeError if the object is not a dictionary.
 *
 * @param obj The object to operate on (dict or Object).
 * @return The removed (key, value) tuple (jsified), or NULL on error.
 */
PyObject *jsified_popitem(PyObject *obj) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result = PyObject_CallMethod(orig, "popitem", NULL);
        Py_DECREF(orig);
        if (!result)
            return NULL;
        RETURN_JSIFIED(result)
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PY_FUNCTION_O_ARGS(jsified_popitem)

/**
 * @brief Insert a key with a default value if not present, and return the value (jsified).
 *
 * Unwraps the object to its original dict, calls `setdefault(key, default_value)`, and returns the result jsified.
 * Raises TypeError if the object is not a dictionary.
 *
 * @param obj           The object to operate on (dict or Object).
 * @param key           The key to insert/check.
 * @param default_value The default value to set if the key is missing.
 * @return The value for the key (jsified), or NULL on error.
 */
PyObject *jsified_setdefault(PyObject *obj, PyObject *key, PyObject *default_value) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result = PyDict_SetDefault(orig, key, default_value);
        Py_DECREF(orig);
        if (!result)
            return NULL;
        RETURN_JSIFIED(result)
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PY_FUNCTION_OOO_ARGS(jsified_setdefault)

/**
 * @brief Update a dictionary-like object with another mapping or iterable of key-value pairs.
 *
 * Unwraps the object to its original dict, calls `update(update)`.
 * Raises TypeError if the object is not a dictionary.
 *
 * @param obj    The object to update (dict or Object).
 * @param update The mapping or iterable with new key-value pairs.
 * @return None on success, or NULL on error.
 */
PyObject *jsified_update(PyObject *obj, PyObject *update) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        int res = PyDict_Update(orig, update);
        Py_DECREF(orig);
        if (res < 0)
            return NULL;
        Py_RETURN_NONE;
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Updated object must be a dictionary.");
    return NULL;
}

PY_FUNCTION_OO_ARGS(jsified_update)


/**
 * @brief Return a list of the dictionary’s key-value pairs.
 *
 * Unwraps the object to its original dict and returns result of `items()`.
 * Raises TypeError if the object is not a dictionary.
 *
 * @param obj The object to query (dict or Object).
 * @return List of (key, value) pairs, or NULL on error.
 */
PyObject *jsified_items(PyObject *obj) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result = PyDict_Items(orig);
        Py_DECREF(orig);
        return result;
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PY_FUNCTION_O_ARGS(jsified_items)


/**
 * @brief Return a list of the dictionary’s keys.
 *
 * Unwraps the object to its original dict and returns result of `keys()`.
 * Raises TypeError if the object is not a dictionary.
 *
 * @param obj The object to query (dict or Object).
 * @return List of keys, or NULL on error.
 */
PyObject *jsified_keys(PyObject *obj) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result = PyDict_Keys(orig);
        Py_DECREF(orig);
        return result;
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PY_FUNCTION_O_ARGS(jsified_keys)

/**
 * @brief Return a list of the dictionary’s values.
 *
 * Unwraps the object to its original dict and returns result of `values()`.
 * Raises TypeError if the object is not a dictionary.
 *
 * @param obj The object to query (dict or Object).
 * @return List of values, or NULL on error.
 */
PyObject *jsified_values(PyObject *obj) {
    PyObject *orig = unjsify(obj);

    if (PyDict_Check(orig)) {
        PyObject *result = PyDict_Values(orig);
        Py_DECREF(orig);
        return result;
    }
    Py_DECREF(orig);
    PyErr_SetString(PyExc_TypeError, "Object must be a dictionary.");
    return NULL;
}

PY_FUNCTION_O_ARGS(jsified_values)

static PyMethodDef jsify_methods[] = {
    {"jsify", (PyCFunction)(void *)Py_jsify, METH_VARARGS | METH_KEYWORDS, "Convert dict, list, or tuple to Object."},
    {"unjsify", (PyCFunction)Py_unjsify, METH_VARARGS, "Convert Object back to its original representation."},
    {"jsified_copy", (PyCFunction)(void *)Py_jsified_copy, METH_VARARGS, "Create a jsified shallow copy of object."},
    {"jsified_deepcopy", (PyCFunction)(void *)Py_jsified_deepcopy, METH_VARARGS, "Create a jsified deep copy of object."},
    {"unjsify_deepcopy", (PyCFunction)Py_unjsify_deepcopy, METH_VARARGS, "Deeply convert Object back to original."},
    {"jsified_get", (PyCFunction)(void *)Py_jsified_get, METH_VARARGS | METH_KEYWORDS, "Get item from object safely."},
    {"jsified_pop", (PyCFunction)(void *)Py_jsified_pop, METH_VARARGS | METH_KEYWORDS, "Pop item from object, wrapping result."},
    {"jsified_popitem", (PyCFunction)Py_jsified_popitem, METH_VARARGS, "Pop (key, value) pair from object, wrapping result."},
    {"jsified_setdefault", (PyCFunction)Py_jsified_setdefault, METH_VARARGS, "Set default value for key, wrapping result."},
    {"jsified_update", (PyCFunction)Py_jsified_update, METH_VARARGS, "Update object with dict, wrapping result."},
    {"jsified_values", (PyCFunction)Py_jsified_values, METH_VARARGS, "Return view of values from object."},
    {"jsified_keys", (PyCFunction)Py_jsified_keys, METH_VARARGS, "Return view of keys from object."},
    {"jsified_items", (PyCFunction)Py_jsified_items, METH_VARARGS, "Return view of items from object."},
    {NULL, NULL, 0, NULL}
};

// Module definition
static PyModuleDef jsifymodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "jsify",
    .m_doc = "Module providing JSON-like objects",
    .m_size = -1,
    .m_methods = jsify_methods
};

// Register type in module
int registerType(PyObject *module, PyTypeObject *type, char *name) {
    if ((PyType_Ready(type) < 0)) return -1;
    Py_INCREF(type);
    int result = PyModule_AddObject(module, name, (PyObject *)type);
    if (result < 0) Py_DECREF(type);
    return result;
}

// Register object in module
int registerObject(PyObject *module, PyObject *object, char *name) {
    Py_INCREF(object);
    int result = PyModule_AddObject(module, name, object);
    if (result < 0) Py_DECREF(object);
    return result;
}

// Module initialization
PyMODINIT_FUNC PyInit_jsify(void) {

    copy_module = PyImport_ImportModule("copy");
    if (!copy_module)
        return NULL;

    deepcopy_func = PyObject_GetAttrString(copy_module, "deepcopy");
    copy_func = PyObject_GetAttrString(copy_module, "copy");

    Py_DECREF(copy_module);
    copy_module = NULL;

    if (!deepcopy_func || !copy_func)
        return NULL;

    PyObject *m;

    m = PyModule_Create(&jsifymodule);
    if (!m) return NULL;

    PyObject_INIT(Undefined, &UndefinedType);

    if (registerType(m, &UndefinedType, "UndefinedType") < 0) return NULL;
    if (registerObject(m, Undefined, "Undefined") < 0) return NULL;
    if (registerType(m, &ObjectType, "Object") < 0) return NULL;
    if (registerType(m, &TupleType, "Tuple") < 0) return NULL;
    if (registerType(m, &ListType, "List") < 0) return NULL;
    if (registerType(m, &DictType, "Dict") < 0) return NULL;
    if (registerType(m, &IteratorType, "Iterator") < 0) return NULL;

    return m;
}