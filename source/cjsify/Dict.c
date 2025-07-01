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

static PyObject *Dict_dir(PyObject *self, PyObject *Py_UNUSED(args)) {
    static const char *attrs[] = {
        "__class__",
        "__name__",
        "__module__",
        "__doc__",
        NULL
    };
    PyObject *list = PyList_New(0);
    if (!list) return NULL;

    for (const char **p = attrs; *p; p++) {
        PyObject *name = PyUnicode_FromString(*p);
        if (!name) {
            Py_DECREF(list);
            return NULL;
        }
        if (PyList_Append(list, name) < 0) {
            Py_DECREF(name);
            Py_DECREF(list);
            return NULL;
        }
        Py_DECREF(name);
    }
    return list;
}

// ============================
// === Method tables ==========
// ============================

static PyMethodDef Dict_methods[] = {
    {"__dir__", (PyCFunction)Dict_dir, METH_NOARGS, NULL},
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

    .tp_as_mapping = &Object_as_mapping,

    .tp_getattro = (getattrofunc)Object_getattr
};
