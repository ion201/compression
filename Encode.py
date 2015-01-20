#!/usr/bin/python3

from PIL import Image
import struct
import sys
from BitObjects import ByteField
from os import path


import ProcessPixels


def advancexy(x, y, max_x):
    x += 1
    if x >= max_x:
        x, y = 0, y+1
    return x, y


def stripalpha(img):
    band_data = []
    for i in range(4):
        band_data.append(list(img.getdata(i)))

    new_img = Image.frombytes('RGB', img.size, ProcessPixels.stripalpha(band_data))

    return new_img


def getpixelindex(lookup_table, palette, color):

    lookup_value = lookup_table[color]
    try:
        index = palette.index(lookup_value)
    except ValueError:  # lookup_value is not in the palette
        index = ProcessPixels.getnearestindex(palette, color)

    return index


def _genheader(img, quality):
    # Header reserves the first 6 bytes
    header = b'\x69\x67'  # file type identifier. 'ig' ascii encoding

    header += struct.pack('>H', img.size[0])  # Format to unsigned short: 2 bytes
    header += struct.pack('>H', img.size[1])
    header += struct.pack('>B', quality)
    return header


def _genpalette(palette):
    # Format: ((i, (r, g, b)), ...)

    data = struct.pack('>B', len(palette))
    for color in palette:
        for c in color:
            data += struct.pack('>B', c)
    return data


def _genbody(img, palette, quality, lookup_table):
    color_array = img.load()
    bf = ByteField()

    img_bytes = []
    # img_bytes = b''

    x, y = 0, 0  # x, y should always point to the next unchecked pixel
    y_old = 0
    index_prev = -1

    while y < img.size[1] or x == 0:

        if index_prev != -1:  # First loop
            index = index_prev
        else:
            index = getpixelindex(lookup_table, palette, color_array[x, y])
            x, y = advancexy(x, y, img.size[0])

        # Check for at least 4 consecutive colors
        count = 1
        index_next = None
        while count < 255:  # Max for repeating single color is 255.
            if y < img.size[1]:
                index_next = getpixelindex(lookup_table, palette, color_array[x, y])
            else:
                x, y = advancexy(x, y, img.size[0])
                break
            x, y = advancexy(x, y, img.size[0])

            if index_next != index or count >= 254:
                break

            count += 1

        if count < 4:
            while count > 0:
                bf.append(index, quality + 4)
                count -= 1
        else:
            bf.append(2**(quality+4) - 1, quality + 4)  # 0b1...11
            bf.append(count, 8)
            bf.append(index, quality + 4)

        index_prev = index_next  # For use next round

        if y != y_old:
            y_old = y
            tmp = b''
            while bf.hasbits(8):
                b = bf.popbits(8)
                tmp += struct.pack('>B', b)
            img_bytes.append(tmp)

    tmp = b''
    while len(bf) != 0:
        while not bf.hasbits(8):
            bf.append(0, 1)
        tmp += struct.pack('>B', bf.popbits(8))
    img_bytes.append(tmp)

    return img_bytes


def encode(in_file, quality=4):
    orig_img = Image.open(in_file)
    if orig_img.mode == 'RGBA':
        # Bake alpha layer into RGB
        orig_img = stripalpha(orig_img)

    band_data = []
    for i in range(3):
        band_data.append(list(orig_img.getdata(i)))
    color_map, lookup_table = ProcessPixels.organize(quality, band_data)

    # Format: ((r, g, b), count)
    color_priority = [x[0] for x in sorted(color_map.items(), key=lambda item: item[1],
                      reverse=True)[:2**(quality+4)-2]]  # values 1..11 and 1..10 are reserved for compression
    palette = tuple(color_priority)

    b_header = _genheader(orig_img, quality)
    b_palette = _genpalette(palette)
    b_body = _genbody(orig_img, palette, quality, lookup_table)

    out_file = path.splitext(path.basename(in_file))[0] + '.ig'
    out_file = 'out.ig'
    with open(out_file, 'wb') as f:
        f.write(b_header)
        f.write(b_palette)
        for part in b_body:
            f.write(part)


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
