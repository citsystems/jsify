/* ThreadLocalStorage.h */

#pragma once
#define PY_SSIZE_T_CLEAN

#if defined(_MSC_VER)
    #define TLS_VAR __declspec(thread)
#else
    #define TLS_VAR _Thread_local
#endif

/* per-thread state */
extern TLS_VAR PyObject *tls_root;
extern TLS_VAR PyObject *tls_path;

/* API */
void tls_reset_path(PyObject *root);
void tls_add_segment(PyObject *segment);
void tls_clear_path(void);
