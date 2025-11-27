/* literals.c */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "Undefined.h"
#include "Macro.h"
#include "Literals.h"

extern PyObject *Undefined;

DEFINE_LITERAL_TYPE(PyLong_Type,      "Int",    IntType)
DEFINE_LITERAL_TYPE(PyFloat_Type,     "Float",  FloatType)
DEFINE_LITERAL_TYPE(PyUnicode_Type,   "Str",    StrType)
DEFINE_LITERAL_TYPE(PyBool_Type,      "Bool",   BoolType)
