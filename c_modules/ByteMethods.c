#include <Python.h>
#include <limits.h>

static unsigned long long value = 0;
static int index = -1;

static PyObject *ByteMethods_init(PyObject *self, PyObject *args)
{
    value = 0;
    index = -1;
    Py_RETURN_NONE;
}

static PyObject *ByteMethods_int(PyObject *self, PyObject *args)
{
    return Py_BuildValue("K", value);
}

static PyObject *ByteMethods_size(PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", index+1);
}

static PyObject *ByteMethods_append(PyObject *self, PyObject *args)
{
    int new_value, bits;

    if (!PyArg_ParseTuple(args, "ii", &new_value, &bits))
        return NULL;

    value = value << bits;
    value += new_value;
    index += bits;

    Py_RETURN_NONE;
}

static PyObject *ByteMethods_hasbits(PyObject *self, PyObject *args)
{
    int number;

    if (!PyArg_ParseTuple(args, "i", &number))
        return NULL;

    if (index >= number-1)
        return Py_BuildValue("i", 1);
    return Py_BuildValue("i", 0);
}

static PyObject *ByteMethods_popbits(PyObject *self, PyObject *args)
{
    int number;
    unsigned long result;

    if (!PyArg_ParseTuple(args, "i", &number))
        return NULL;

    while (index < (number - 1)){
        number -= 1;
    }

    result = value >> (index - number + 1);
    value = value ^ (result << (index - number + 1));
    index -= number;

    return Py_BuildValue("k", result);
}

static PyMethodDef ByteMethodsMethods[] = {
    {"init", ByteMethods_init, METH_VARARGS,
    "Initialize object for managing bytes"},
    {"int", ByteMethods_int, METH_VARARGS,
    "Get integer form of current value"},
    {"size", ByteMethods_size, METH_VARARGS,
    "Get bit length of value"},
    {"append", ByteMethods_append, METH_VARARGS,
    "append(value, bits)\nAppend value with given number of bits buffered"},
    {"hasbits", ByteMethods_hasbits, METH_VARARGS,
    "hasbits(number)\nCheck if number of bits is available."},
    {"popbits", ByteMethods_popbits, METH_VARARGS,
    "popbits(number)\nRemove and return the requested number of bits"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef ByteMethodsModule = {
    PyModuleDef_HEAD_INIT, "ByteMethods", "Module docstring", -1, ByteMethodsMethods
};

PyMODINIT_FUNC PyInit_ByteMethods(void)
{
    PyObject *m = PyModule_Create(&ByteMethodsModule);
    if (m == NULL)
        return;
}