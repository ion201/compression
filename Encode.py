#!/usr/bin/python3

from PIL import Image
import struct
import sys
from BitObject import ByteField


import ProcessPixels


def stripalpha(img):
    band_data = []
    for i in range(4):
        band_data.append(list(img.getdata(i)))

    new_img = Image.frombytes('RGB', img.size, ProcessPixels.stripalpha(band_data))

    return new_img


def getproximity(c1, c2):
    result = 0
    for i in range(3):
        result += (c1[i] - c2[i])**2

    return result**(1/2)


def _genheader(img):
    # Header reserves the first 6 bytes
    header = b'\x69\x67'  # file type identifier. 'ig' ascii encoding

    header += struct.pack('>H', img.size[0])  # Format to unsigned short: 2 bytes
    header += struct.pack('>H', img.size[1])
    return header


def _genpalette(palette):
    # Format: ((i, (r, g, b)), ...)

    data = struct.pack('>B', len(palette))
    for i, color in palette:
        for c in color:
            data += struct.pack('>B', c)

    return data


def _genbody(img, palette, quality):
    color_array = img.load()
    bf = ByteField()

    b = b''

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel_c = color_array[x, y]
            prox = []
            for i, palette_c in palette:
                prox.append((getproximity(pixel_c, palette_c), palette_c, i))
            prox.sort(key=lambda c: c[0])
            bf.append(prox[0][2], quality + 4)

        tmp = b''
        while bf.hasbyte():
            tmp += bf.popbyte()
        b += tmp

    return b


def encode(in_file, quality=4):
    orig_img = Image.open(in_file)
    if orig_img.mode == 'RGBA':
        # Bake alpha layer into RGB
        orig_img = stripalpha(orig_img)

    band_data = []
    for i in range(3):
        band_data.append(list(orig_img.getdata(i)))
    color_map = ProcessPixels.organize(quality, band_data)

    # Format: ((r, g, b), count)
    color_priority = [x[0] for x in sorted(color_map.items(), key=lambda item: item[1],
                      reverse=True)[:2**(quality+4)-3]]  # values 1..11 and 1..10 are reserved for compression
    palette = tuple(enumerate(color_priority))
    # Possible optimizations at this point (will probably move into c again for speed):
    # 0xf..ff will be folloed by 5 bits indicating how many times the next color should be repeated (inclusive)
    # and 1 bit to indicate vertical or horizontal
    # 0xf..fe followed by 2 - 4 bit blocks indicating LxW pixel block to fill

    b_header = _genheader(orig_img)
    b_palette = _genpalette(palette)
    b_body = _genbody(orig_img, palette, quality)

    with open('out.ig', 'wb') as f:
        f.write(b_header)
        f.write(b_palette)
        f.write(b_body)


def main():
    if len(sys.argv) < 2:
        print('Usage: ./Encode [file] [quality 0-4]')
        return
    if len(sys.argv) < 3:
        encode(sys.argv[1])
    else:
        encode(sys.argv[1], int(sys.argv[2]))

if __name__ == '__main__':
    main()
