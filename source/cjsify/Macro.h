#define REDIRECT_TO_ORIG_METHOD(type_name, name, func) \
type_name##name(PyObject *self) { \
    return func(((type_name *)self)->orig); \
}

#define REDIRECT_TO_ORIG_METHOD_O_ARGS(ret_type, type_name, name, func) \
type_name##name(PyObject *self, PyObject *arg) { \
    PyObject *orig = unjsify(arg); \
    ret_type result = func(((type_name *)self)->orig, orig); \
    Py_DECREF(orig); \
    return result; \
}

#define REDIRECT_TO_ORIG_METHOD_CALL(type_name, name, method) \
type_name##name(PyObject *self, PyObject *Py_UNUSED(args)) { \
    return PyObject_CallMethod(((type_name *)self)->orig, method, NULL); \
}

#define REDIRECT_TO_ORIG_METHOD_CALL_O_ARGS(ret_type, type_name, name, method) \
ret_type type_name##name(PyObject *self, PyObject *arg) { \
    PyObject *orig = unjsify(arg); \
    ret_type result = PyObject_CallMethod(((type_name *)self)->orig, method, "O", orig); \
    Py_DECREF(orig); \
    return result; \
}

#define REDIRECT_TO_ORIG_BINARY(ret_type, type_name, name, func) \
ret_type type_name##name(PyObject *self, PyObject *other) { \
    PyObject *other_orig = unjsify(other); \
    PyObject *self_orig = unjsify(self); \
    ret_type result = func(self_orig, other_orig); \
    Py_DECREF(other_orig); \
    Py_DECREF(self_orig); \
    RETURN_JSIFIED(result); \
}

#define REDIRECT_TO_ORIG_TERNARY(ret_type, type_name, name, func) \
ret_type type_name##name(PyObject *self, PyObject *arg1, PyObject *arg2) { \
    PyObject *orig1 = unjsify(arg1); \
    PyObject *orig2 = unjsify(arg2); \
    ret_type result = func(((type_name *)self)->orig, orig1, orig2); \
    Py_DECREF(orig1); \
    Py_DECREF(orig2); \
    RETURN_JSIFIED(result); \
}

#define REDIRECT_TO_ORIG_METHOD_1_ARG(ret_type, type_name, name, func) \
ret_type type_name##name(PyObject *self, PyObject *arg) { \
    PyObject *orig = unjsify(arg); \
    ret_type result = func(((type_name *)self)->orig, orig); \
    Py_DECREF(orig); \
    return result; \
}

#define RETURN_ORIG(obj) \
PyObject *orig = unjsify(obj); \
Py_DECREF(obj); \
return orig;

#define RETURN_JSIFIED(obj) \
if (!obj) return NULL; \
PyObject *jsified = jsify(obj); \
Py_DECREF(obj); \
return jsified;

#define PY_FUNCTION_O_ARGS(name) \
PyObject *Py_##name(PyObject *Py_UNUSED(self), PyObject *args) { \
    PyObject *obj; \
    if (!PyArg_ParseTuple(args, "O", &obj)) \
        return NULL; \
    return name(obj); \
}

#define PY_FUNCTION_OO_ARGS(name) \
PyObject *Py_##name(PyObject *Py_UNUSED(self), PyObject *args) { \
    PyObject *obj1, *obj2; \
    if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) \
        return NULL; \
    return name(obj1, obj2); \
}

#define PY_FUNCTION_OOO_ARGS(name) \
PyObject *Py_##name(PyObject *Py_UNUSED(self), PyObject *args) { \
    PyObject *obj1, *obj2, *obj3; \
    if (!PyArg_ParseTuple(args, "OOO", &obj1, &obj2, &obj3)) \
        return NULL; \
    return name(obj1, obj2, obj3); \
}

#define RETURN_EXCEPTION(exc_type, msg)  \
    PyErr_SetString((exc_type), (msg));  \
    return NULL;

#define SET_MISSING_EXCEPTION_IF_NULL(val, exc_type, msg)   \
    if ((val) == NULL)                          \
        if (!PyErr_Occurred())                  \
            PyErr_SetString((exc_type), (msg));

#define DEFINE_LITERAL_TYPE(BaseType, NameStr, TypeVar)          \
static PyObject *TypeVar##_getattro(PyObject *self, PyObject *name) {        \
    PyObject *res = PyObject_GenericGetAttr(self, name);                     \
    if (res) return res;                                                     \
    PyErr_Clear();                                                           \
    Py_INCREF(Undefined);                                                    \
    return Undefined;                                                        \
}                                                                            \
                                                                             \
PyTypeObject TypeVar = {                                                     \
    PyVarObject_HEAD_INIT(NULL, 0)                                           \
    .tp_name = NameStr,                                                      \
    .tp_basicsize = sizeof(BaseType),                                        \
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                    \
    .tp_base = (PyTypeObject *)&BaseType,                                    \
    .tp_getattro = TypeVar##_getattro                                        \
};

