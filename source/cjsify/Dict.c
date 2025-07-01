#define PY_SSIZE_T_CLEAN
#include <stddef.h>
#include <Python.h>

#include "cjsify.h"
#include "Object.h"
#include "Dict.h"
#include "List.h"
#include "Tuple.h"

// ============================
// === Basic object methods ===
// ============================

// Initialization
static int Dict_init(Dict *self, PyObject *args, PyObject *kwargs) {
    if (Object_init((Object *) self, args, kwargs) == 0) {
        if (kwargs) {
            if (PyDict_Update(self->orig, kwargs) < 0)
                return -1;
        }
        return 0;
    } else return -1;
}

// ============================
// === Type definition ========
// ============================

#ifdef _MSC_VER
    #ifndef __attribute__
        #define __attribute__(x)
    #endif
#endif

PySequenceMethods Dict_as_sequence = {};

static PyObject* Dict_dir(PyObject *self, PyObject *noargs) {
    static PyObject *static_attrs = NULL;
    if (!static_attrs) {
        static_attrs = PyList_New(0);
        if (!static_attrs) return NULL;

        const char *names[] = {
            "__class__", "__str__", "__repr__", "__bool__",
            "__module__", "__name__", "__eq__"
        };
        for (int i = 0; i < (int)(sizeof(names)/sizeof(names[0])); i++) {
            PyObject *s = PyUnicode_InternFromString(names[i]);
            if (!s) return NULL;
            PyList_Append(static_attrs, s);
            Py_DECREF(s);
        }
        Py_INCREF(static_attrs);
    }

    PyObject *result = PyList_GetSlice(static_attrs, 0, PyList_Size(static_attrs));
    if (!result) return NULL;

    PyObject *orig = ((Dict *)self)->orig;
    if (PyDict_Check(orig)) {
        PyObject *keys = PyDict_Keys(orig);
        if (!keys) {
            Py_DECREF(result);
            return NULL;
        }

        Py_ssize_t len = PyList_Size(keys);
        for (Py_ssize_t i = 0; i < len; i++) {
            PyObject *key = PyList_GetItem(keys, i);
            if (PyUnicode_Check(key)) {
                PyList_Append(result, key);
            } else {
                PyObject *strkey = PyObject_Str(key);
                if (strkey) {
                    PyList_Append(result, strkey);
                    Py_DECREF(strkey);
                }
            }
        }
        Py_DECREF(keys);
    }

    return result;
}



static PyMethodDef Dict_methods[] = {
    {"__dir__", (PyCFunction)Dict_dir, METH_NOARGS, NULL},
    // inne metody
    {NULL, NULL, 0, NULL}
};

PyTypeObject DictType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_base = &ObjectType,
    .tp_name = "Dict",
    .tp_basicsize = sizeof(Dict),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "JSON-like dictionary with attribute access",
    .tp_init = (initproc)Dict_init,

    .tp_methods = Dict_methods,

    .tp_as_mapping = &Object_as_mapping
};
