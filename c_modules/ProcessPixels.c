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

static PyObject *ProcessPixels_stripalpha(PyObject *self, PyObject *args)
{
    PyObject *byteData = NULL;
    PyObject *bandData;
    PyObject *band_r;
    PyObject *band_g;
    PyObject *band_b;
    PyObject *band_a;
//    unsigned char pixelColor[4] = "000";
    unsigned char *byteDataArray;
    int a;
    int i, j;
    int arrayIndex = 0;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &bandData)){
        return NULL;
    }

    band_r = PyList_GetItem(bandData, 0);
    band_g = PyList_GetItem(bandData, 1);
    band_b = PyList_GetItem(bandData, 2);
    band_a = PyList_GetItem(bandData, 3);

    byteDataArray = malloc(sizeof(char) * (PyList_Size(band_r) * 3 + 1)); //
    byteDataArray[PyList_Size(band_r) * 3] = '\x00';

    for (i = 0; i < PyList_Size(band_r); i++){
        a = (int) PyLong_AsLong(PyList_GetItem(band_a, i));
        byteDataArray[arrayIndex] = (unsigned char) (255 + a * (PyLong_AsLong(PyList_GetItem(band_r, i)) / 255.0 - 1));
        byteDataArray[arrayIndex+1] = (unsigned char) (255 + a * (PyLong_AsLong(PyList_GetItem(band_g, i)) / 255.0 - 1));
        byteDataArray[arrayIndex+2] = (unsigned char) (255 + a * (PyLong_AsLong(PyList_GetItem(band_b, i)) / 255.0 - 1));
        for (j = 0; j < 3; j++){
            if (byteDataArray[arrayIndex+j] == 0)  //Don't want a \x00 in the middle of my null-terminated string
                byteDataArray[arrayIndex+j] = 1;
        }
        arrayIndex += 3;
    }

    byteData = PyBytes_FromString(byteDataArray);
    free(byteDataArray);

    return byteData;
}

static PyMethodDef ProcessPixelsMethods[] = {
    {"organize", ProcessPixels_organize, METH_VARARGS,
    "organize(quality, band_data)\nAccepts a list of pixels [[R, R...], [G, G...], [B, B...]] and returns a dict with the count for each"},
    {"stripalpha", ProcessPixels_stripalpha, METH_VARARGS, "stripalpha(band_data)"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef ProcessPixelsModule = {
    PyModuleDef_HEAD_INIT, "ProcessPixels", "This module does things", -1, ProcessPixelsMethods};

PyMODINIT_FUNC PyInit_ProcessPixels(void){
    PyObject *m = PyModule_Create(&ProcessPixelsModule);
    if (m == NULL)
        return;
}