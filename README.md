compression
===========
A poorly optimized compression/encoding algorithm designed to (inadequately) replace lossy compression formats like jpeg. Current benchmarks place the compression from .5x to 2x the size of the source image depending on it's content.

Dependencies:
- Linux/Windows (untested on osx, but should work with proper libs)
- python3
- (Linux) python3-dev
- (Windows) VS2010
- Pillow (> 1.0)

Included c modules must be compiled via setup.py file and moved to project root before running.

This is just a small project I've been working on in my spare time. It's not going to be big and professional like png
