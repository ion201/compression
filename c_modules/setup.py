from distutils.core import setup, Extension
import shutil
import os
import platform

setup(
    ext_modules=[Extension("ProcessPixels", ["ProcessPixels.c"])]
)

try:
    if platform.system() == 'Linux':
        os.system('cp build/lib.linux-x86_64-3.*/ProcessPixels.cpython-*.so ../')
    else:
        shutil.copy('build/lib.win32-3.3/ProcessPixels.pyd', '../')
except PermissionError:
    print('Error copying the new .pyd file. Is the old file open in a python terminal?')
