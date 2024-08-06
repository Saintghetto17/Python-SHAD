#include "concat.h"

#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* py_concat(PyObject* /* self */, PyObject* args) {
    const char *l, *r;
    if (!PyArg_ParseTuple(args, "ss", &l, &r)) {
        return NULL;
    }
    PyObject* result = NULL;

    try {
        auto concatenated = cpp_concat({l}, {r});
        result = Py_BuildValue("s", concatenated.data());
        if (result == NULL) {
            return result;
        }
    } catch (const EmptyArgumentException& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
    }

    return result;
}

static PyObject* py_concat_list(PyObject* self, PyObject* args) {
    PyObject* list;
    if (!PyArg_ParseTuple(args, "O", &list)) {
        return NULL;
    }
    int n = PyList_Size(list);
    if (n < 2) {
        Py_DECREF(list);
        PyErr_SetString(PyExc_RuntimeError, "Sequence of len >= 2 required");
        return NULL;
    }
    PyObject *item = NULL;
    PyObject *result = NULL;

    for (int i = 0; i < n; ++i) {
        item = PyList_GetItem(list, i);
        if (result == NULL) {
            result = item;
            Py_INCREF(result);
            continue;
        }
        PyObject* subcall_args = Py_BuildValue("OO", result, item);
        PyObject* subcall_res = py_concat(self, subcall_args);
        Py_DECREF(subcall_args);

        Py_XDECREF(result);
        if (subcall_res == NULL) {
            Py_DECREF(list);
            return NULL;
        }
        result = subcall_res;
    }
    Py_DECREF(list);
    return result;
}

// py module definition

static PyMethodDef methods[] = {
    {"concat", py_concat, METH_VARARGS, "Concat two non-empty strings"},
    {"concat_list", py_concat_list, METH_VARARGS, "Concat list of non-empty strings"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "concat module",    /* name of module */
    NULL,               /* module documentation, may be NULL */
    -1,                 /* size of per-interpreter state of the module,
                         * or -1 if the module keeps state in global variables.
                         */
    methods
};


PyMODINIT_FUNC
PyInit_libconcat() {
    return PyModule_Create(&module);
}
