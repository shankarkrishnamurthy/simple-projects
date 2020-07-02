#include <Python.h>

static PyObject* helloworld(PyObject* self) {
   return Py_BuildValue("s", "Hello, Python extensions!!");
}

static char helloworld_docs[] =
   "helloworld( ): Any message you want to put here!!\n";

static PyMethodDef helloworld_funcs[] = {
   {"helloworld", (PyCFunction)helloworld, 
      METH_NOARGS, helloworld_docs},
      {NULL}
};

/* DEPRECATED: Use Other means
void inithelloworld(void) {
   Py_InitModule3("hworld", helloworld_funcs,
                  "Extension module example!");
}
*/

static struct PyModuleDef Combinations =
{
    PyModuleDef_HEAD_INIT,
    "hworld", /* name of module */
    "usage:  print h.helloworld() ", /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    helloworld_funcs
};

PyMODINIT_FUNC PyInit_hworld(void)
{
    return PyModule_Create(&Combinations);
}
