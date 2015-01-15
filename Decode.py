#!/usr/bin/python3

import sys
import struct
from BitObjects import ByteField
from PIL import Image


def decode(filename):
    with open(filename, 'rb') as in_file:
        data = in_file.read()

    if data[:2] != b'ig':
        print('Invalid file!')
        return

    width = struct.unpack_from('>H', data, 2)[0]
    height = struct.unpack_from('>H', data, 4)[0]
    quality = struct.unpack_from('>B', data, 6)[0]
    palette_count = struct.unpack_from('>B', data, 7)[0]

    decoded_img = Image.new('RGB', (width, height))
    pixel_array = decoded_img.load()
    x, y = 0, 0

    index = 8

    bf = ByteField()

    palette = []

    while palette_count > 0:
        palette_count -= 1
        palette.append(struct.unpack_from('>3B', data, index))
        index += 3

    while index < len(data):
        bf.append(struct.unpack_from('>B', data, index)[0], 8)
        # quality + 4 => BITS_PER_COLOR
        while bf.hasbits(quality + 4) and y < height:
            b = bf.popbits(quality + 4)
            if b == 2**(quality + 4) - 1:
                # Repeat the next color n times
                while not bf.hasbits(quality + 12):
                    bf.append(struct.unpack_from('>B', data, index+1)[0], 8)
                    index += 1

                n = bf.popbits(8)
                color_index = bf.popbits(quality + 4)
                for i in range(n):
                    pixel_array[x, y] = palette[color_index]
                    x += 1
                    if x >= width:
                        x, y = 0, y + 1
                    if y >= height:
                        break
            else:
                pixel_array[x, y] = palette[b]
                x += 1
                if x >= width:
                    x, y = 0, y + 1
        index += 1

    decoded_img.show()


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
