#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "Undefined.h"
#include "Object.h"

static PyObject *Undefined_repr(UndefinedObject *self) {
    (void) self;
    return PyUnicode_FromString("Undefined");
}

static PyObject *Undefined_call(UndefinedObject *self, PyObject *args, PyObject *kwargs) {
    (void) args;
    (void) kwargs;
    Py_INCREF(self);
    return (PyObject *)self;
}

static PyObject *Undefined_getattr(UndefinedObject *self, PyObject *name) {
    if (PyUnicode_Check(name)) {
        const char *attr = PyUnicode_AsUTF8(name);
        if (attr == NULL) return NULL;
        if (attr && attr[0] == '_' && attr[1] == '_' &&
            attr[strlen(attr) - 2] == '_' && attr[strlen(attr) - 1] == '_') {

            if (strcmp(attr, "__class__") == 0) {
                Py_INCREF(Py_TYPE(self));
                return (PyObject *)Py_TYPE(self);
            }
            if (strcmp(attr, "__dir__") == 0 ||
                strcmp(attr, "__repr__") == 0 ||
                strcmp(attr, "__str__") == 0 ||
                strcmp(attr, "__bool__") == 0 ||
                strcmp(attr, "__name__") == 0 ||
                strcmp(attr, "__module__") == 0 ||
                strcmp(attr, "__doc__") == 0) {
                return PyObject_GenericGetAttr((PyObject *)Py_TYPE(self), name);
            }
        }
    }
    Py_INCREF(self);
    return (PyObject *)self;
}

static PyObject *Undefined_getitem(UndefinedObject *self, PyObject *key) {
    (void) key;
    Py_INCREF(self);
    return (PyObject *)self;
}

static PyObject *Undefined_eq(UndefinedObject *self, PyObject *other, int op) {
    (void) self;
    int is_equal = (other == Py_None || PyObject_TypeCheck(other, &UndefinedType));

    if (op == Py_EQ) {
        if (is_equal)
            Py_RETURN_TRUE;
        else
            Py_RETURN_FALSE;
    } else if (op == Py_NE) {
        if (is_equal)
            Py_RETURN_FALSE;
        else
            Py_RETURN_TRUE;
    }

    Py_RETURN_NOTIMPLEMENTED;
}

static int Undefined_bool(UndefinedObject *self) {
    (void) self;
    return 0;
}


static PyNumberMethods Undefined_as_number = {
    .nb_bool = (inquiry)Undefined_bool,
};


static Py_hash_t Undefined_hash(UndefinedObject *self) {
    return (Py_hash_t)(uintptr_t)self;
}


static PyObject* Undefined_dir(PyObject *self, PyObject *noargs) {
    static PyObject *result = NULL;
    if (!result) {
        result = PyList_New(0);
        if (!result) return NULL;
        const char *names[] = {"__class__", "__str__", "__repr__", "__bool__",
                               "__module__", "__name__", "__eq__", "__dir__"};
        for (int i = 0; i < 8; i++) {
            PyObject *s = PyUnicode_FromString(names[i]);
            PyList_Append(result, s);
            Py_DECREF(s);
        }
        Py_INCREF(result);
    }
    Py_INCREF(result);
    return result;
}


static PyMappingMethods Undefined_as_mapping = {
    .mp_subscript = (binaryfunc)Undefined_getitem,
    // inne mogą być NULL
};


static PyMethodDef Undefined_methods[] = {
    {"__dir__", (PyCFunction)Undefined_dir, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}
};


PyTypeObject UndefinedType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Undefined",
    .tp_basicsize = sizeof(UndefinedObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Singleton representing JavaScript-like 'undefined'",
    .tp_repr = (reprfunc)Undefined_repr,
    .tp_str = (reprfunc)Undefined_repr,
    .tp_call = (ternaryfunc)Undefined_call,
    .tp_getattro = (getattrofunc)Undefined_getattr,
    .tp_richcompare = (richcmpfunc)Undefined_eq,
    .tp_as_number = &Undefined_as_number,
    .tp_hash = (hashfunc)Undefined_hash,

    .tp_methods = Undefined_methods,

    .tp_as_mapping = &Undefined_as_mapping
};

static UndefinedObject _Undefined;
PyObject *Undefined = (PyObject *)&_Undefined;

