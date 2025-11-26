#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

#include "cjsify.h"
#include "Object.h"
#include "Tuple.h"
#include "Dict.h"
#include "List.h"
#include "Undefined.h"

// ============================
// === Helper macros ==========
// ============================

#include "Macro.h"

// ============================
// === Main Tuple methods =====
// ============================

// count(value)
static PyObject *Tuple_count(PyObject *self, PyObject *args) {
    PyObject *value;
    if (!PyArg_ParseTuple(args, "O", &value))
        return NULL;

    return PyObject_CallMethod(((Tuple *)self)->orig, "count", "O", value);
}

// index(value)
static PyObject *Tuple_index(PyObject *self, PyObject *value) {
    Py_ssize_t idx = PySequence_Index(((Tuple *)self)->orig, value);
    if (idx == -1 && PyErr_Occurred())
        return NULL;
    return PyLong_FromSsize_t(idx);
}

static PyObject *Tuple_getitem(PyObject *self, PyObject *key) {
    if (PyLong_Check(key)) {
        Py_ssize_t idx = PyLong_AsSsize_t(key);
        PyObject *orig = ((Tuple *)self)->orig;
        Py_ssize_t size = PySequence_Size(orig);
        if (idx < 0)
            idx += size;
        if (idx < 0 || idx >= size) {
            Py_INCREF(Undefined);
            return Undefined;
        }
        PyObject *value = PySequence_GetItem(orig, idx);
        RETURN_JSIFIED(value);
    }

    if (PySlice_Check(key)) {
        PyObject *value = PyObject_GetItem(((Tuple *)self)->orig, key);
        RETURN_JSIFIED(value);
    }

    if (PyUnicode_Check(key)) {
        const char *str = PyUnicode_AsUTF8(key);
        if (str == NULL) return NULL;
        char *endptr;
        long index = strtol(str, &endptr, 10);
        if (*endptr == '\0') {
            Py_ssize_t tuple_size = PyTuple_Size(((Tuple *)self)->orig);
            if (index < 0)
                index += tuple_size;
            if (index < 0 || index >= tuple_size) {
                Py_INCREF(Undefined);
                return Undefined;
            }
            PyObject *value = PyTuple_GetItem(((Tuple *)self)->orig, index);
            return jsify(value);
        }
    }

    // fallback to attribute lookup
    PyObject *value = PyObject_GenericGetAttr(((Tuple *)self)->orig, key);
    SET_MISSING_EXCEPTION_IF_NULL(value, PyExc_AttributeError, "Attribute not found");
    RETURN_JSIFIED(value);
}

static PyObject* Tuple_dir(PyObject *self, PyObject *noargs) {
    // Stała lista wspólnych atrybutów — zainicjalizowana tylko raz
    static PyObject *static_attrs = NULL;
    if (!static_attrs) {
        static_attrs = PyList_New(0);
        if (!static_attrs) return NULL;

        const char *names[] = {
            "__class__", "__name__", "__doc__", "__module__",
            "__class__", "__str__", "__repr__", "__dir__"
        };
        for (int i = 0; i < (int)(sizeof(names)/sizeof(names[0])); i++) {
            PyObject *s = PyUnicode_InternFromString(names[i]);
            if (!s) return NULL;
            PyList_Append(static_attrs, s);
            Py_DECREF(s);
        }
        Py_INCREF(static_attrs);
    }

    // Utwórz kopię statycznej listy atrybutów
    PyObject *result = PyList_GetSlice(static_attrs, 0, PyList_Size(static_attrs));
    if (!result) return NULL;

    // Dodaj indeksy tupla
    PyObject *orig = ((Object *)self)->orig;
    if (PyTuple_Check(orig)) {
        Py_ssize_t n = PyTuple_Size(orig);
        for (Py_ssize_t i = 0; i < n; ++i) {
            char buf[32];
            snprintf(buf, sizeof(buf), "%zd", i);
            PyObject *index_str = PyUnicode_FromString(buf);
            if (!index_str) {
                Py_DECREF(result);
                return NULL;
            }
            PyList_Append(result, index_str);
            Py_DECREF(index_str);
        }
    }

    return result;
}


// ============================
// === Method tables ==========
// ============================

static PyMethodDef Tuple_methods[] = {
    {"count", (PyCFunction)Tuple_count, METH_VARARGS, NULL},
    {"index", (PyCFunction)Tuple_index, METH_O, NULL},
    {"copy",(PyCFunction)Object_copy, METH_NOARGS, NULL},
    {"__dir__", (PyCFunction)Tuple_dir, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static PyMappingMethods Tuple_as_mapping = {
    .mp_length = (lenfunc)Object_len,
    .mp_subscript = (binaryfunc)Tuple_getitem,
};

// ============================
// === Type definition ========
// ============================

#ifdef _MSC_VER
    #ifndef __attribute__
        #define __attribute__(x)
    #endif
#endif

PyTypeObject TupleType __attribute__((used)) = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_base = &ObjectType,
    .tp_name = "Tuple",
    .tp_basicsize = sizeof(Tuple),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "JSON-like tuple object with attribute access",

    .tp_methods = Tuple_methods,
    .tp_as_mapping = &Tuple_as_mapping,
    .tp_as_sequence = &Object_as_sequence,
};
