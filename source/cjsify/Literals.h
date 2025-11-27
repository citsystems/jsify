#pragma once
#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* Int literal type (subclass of PyLong_Type) */
extern PyTypeObject IntType;

/* Float literal type (subclass of PyFloat_Type) */
extern PyTypeObject FloatType;

/* Str literal type (subclass of PyUnicode_Type) */
extern PyTypeObject StrType;

/* Bool literal type (subclass of PyBool_Type) */
extern PyTypeObject BoolType;
