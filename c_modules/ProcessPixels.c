#include <Python.h>

static PyObject *ProcessPixels_organize(PyObject *self, PyObject *args)
{
    // https://docs.python.org/3/c-api/arg.html
    //Args: organize(int quality, PythonList pixels)
    //What this file needs to do:
    //1. Accept a list of pixels in the format: [(r1, r2, ...), (g1, g2, ...), (b1, b2, ...)]
    //2. Iterate through the list. For every RGB pixel, so this python op:
    //   pixel = tuple(min(pixel_data[band][i] // (100-math.floor(scan_quality**3))
    //                 * (100-math.floor(scan_quality**3))
    //                 + (100-math.floor(scan_quality**3)) // 3, 255)
    //                 for band in range(3))
    //3. Return a dictionary for every calculated pixel and it's count

    int quality;
    PyObject *pixelData;

    if (!PyArg_ParseTuple(args, "iO", &quality, pixelData))
        return NULL;

    return Py_BuildValue("i", 3);
}

static PyMethodDef ProcessPixelsMethods[] = {
    {"organize", ProcessPixels_organize, METH_VARARGS,
    "Accepts a list of pixels [(R, R...), (G, G...), (B, B...)] and returns a dict with the count for each"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef ProcessPixelsModule = {
    PyModuleDef_HEAD_INIT, "ProcessPixels", "This module does things", -1, ProcessPixelsMethods};

PyMODINIT_FUNC PyInit_ProcessPixels(void){
    PyObject *m = PyModule_Create(&ProcessPixelsModule);
    if (m == NULL)
        return;
}