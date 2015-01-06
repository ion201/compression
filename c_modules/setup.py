from distutils.core import setup, Extension
import shutil
import os

setup(
    ext_modules=[Extension("ProcessPixels", ["ProcessPixels.c"])]
)

try:
    shutil.copy('build/lib.win32-3.3/ProcessPixels.pyd', '../')
except PermissionError:
    print('Error copying the new .pyd file. Is the old file open in a python terminal?')