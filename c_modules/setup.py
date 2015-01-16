from distutils.core import setup, Extension

setup(
    ext_modules=[Extension("ProcessPixels", ["ProcessPixels.c"]),
                 Extension("ByteMethods", ["ByteMethods.c"])]
)