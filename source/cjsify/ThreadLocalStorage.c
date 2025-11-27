/* ThreadLocalStorage.c */
#include <Python.h>
#include "ThreadLocalStorage.h"

TLS_VAR PyObject *tls_root = NULL;
TLS_VAR PyObject *tls_path = NULL;

void tls_clear_path(void)
{
    Py_XDECREF(tls_root);
    Py_XDECREF(tls_path);
    tls_root = NULL;
    tls_path = NULL;
}

void tls_reset_path(PyObject *root)
{
    tls_clear_path();

    Py_INCREF(root);
    tls_root = root;

    tls_path = PyList_New(0);
}

void tls_add_segment(PyObject *segment)
{
    if (!tls_path)
        return;

    PyList_Append(tls_path, segment);
}
