#include <Python.h>

int binColor(PyObject *c, float quality)
{
    // PyObject *c is a python long
    int color = (int) PyLong_AsLong(c);
    int qThreshold = 100 - (int)(quality * quality * quality);
    int newColor = (color / qThreshold) * qThreshold + qThreshold / 3;
    if (newColor > 255)
        newColor = 255;
    return newColor;
}

static PyObject *ProcessPixels_organize(PyObject *self, PyObject *args)
{
    // https://docs.python.org/3/c-api/concrete.html#sequence-objects

    // Args: organize(int quality, PyListObject pixels)

    // VS2010 sucks
    PyObject *pixelData;    //PyListObject
    PyObject *band_r;       //PyListObject
    PyObject *band_g;
    PyObject *band_b;
    PyObject *pixelsDict;   //PyDictObject
    PyObject *pixelTmp;     //PyTupleObject
    int quality;
    int i, countTmp;
    int r, g, b;

    if (!PyArg_ParseTuple(args, "iO!", &quality, &PyList_Type, &pixelData))
        return NULL;

    // Other list functions: PyList_GetItem(listObj, i)
    band_r = PyList_GetItem(pixelData, 0);
    band_g = PyList_GetItem(pixelData, 1);
    band_b = PyList_GetItem(pixelData, 2);

    pixelsDict = PyDict_New();
    //pixelTmp = PyTuple_New(3);
    for (i = 0; i < PyList_Size(band_r); i++){
        r = binColor(PyList_GetItem(band_r, i), quality);
        g = binColor(PyList_GetItem(band_g, i), quality);
        b = binColor(PyList_GetItem(band_b, i), quality);
        pixelTmp = PyTuple_New(3);
        PyTuple_SetItem(pixelTmp, 0, Py_BuildValue("i", r));
        PyTuple_SetItem(pixelTmp, 1, Py_BuildValue("i", g));
        PyTuple_SetItem(pixelTmp, 2, Py_BuildValue("i", b));

        // if (PyDict_Contains(pixelsDict, pixelTmp) == 1)
        if (PyDict_GetItem(pixelsDict, pixelTmp) == NULL){
            countTmp = 1;
        } else{
            countTmp = PyLong_AsLong(PyDict_GetItem(pixelsDict, pixelTmp)) + 1;
        }
        PyDict_SetItem(pixelsDict, pixelTmp, Py_BuildValue("i", countTmp));
    }
    return pixelsDict;
}

static PyMethodDef ProcessPixelsMethods[] = {
    {"organize", ProcessPixels_organize, METH_VARARGS,
    "organize(quality, band_data)\nAccepts a list of pixels [[R, R...], [G, G...], [B, B...]] and returns a dict with the count for each"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef ProcessPixelsModule = {
    PyModuleDef_HEAD_INIT, "ProcessPixels", "This module does things", -1, ProcessPixelsMethods};

PyMODINIT_FUNC PyInit_ProcessPixels(void){
    PyObject *m = PyModule_Create(&ProcessPixelsModule);
    if (m == NULL)
        return;
}