#!/usr/bin/python3

import sys
import struct


def decode(filename):
    with open(filename, 'rb') as in_file:
        data = in_file.read()

    if data[:2] != b'ig':
        print('Invalid file!')
        return

    width = struct.unpack_from('>H', data, 2)
    heigh = struct.unpack_from('>H', data, 4)
    palette_count = struct.unpack_from('>G', data, 6)

    index = 7

    while palette_count != 0:
        palette_count -= 1


def main():
    if len(sys.argv) < 2:
        print('Usage: ./Decode [file]]')
        return
    if len(sys.argv) < 3:
        decode(sys.argv[1])
    else:
        decode(sys.argv[1])


if __name__ == '__main__':
    main()
