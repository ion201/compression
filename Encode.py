#!/usr/bin/python3

from PIL import Image
import struct
import sys


import ProcessPixels


def stripalpha(img):
    # This a convience function for ProcessPixels.stripalpha()
    pixel_array = img.load()
    new_img = img.convert('RGB')
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            color = list(pixel_array[x, y])
            new_color = []
            if color[3] > 245:
                continue
            for i in range(3):
                new_color.append(int(255 + color[3]*(color[i] / 255 - 1)))
            pixel_array[x, y] = tuple(new_color)

    return new_img


def _genheader(img):
    # Header reserves the first 6 bytes
    header = b'\x69\x67'  # file type identifier. 'ig' ascii encoding

    header += struct.pack('>H', img.size[0])  # Format to unsigned short: 2 bytes
    header += struct.pack('>H', img.size[1])
    return header


def _genpalette(palette):
    # Format: ((r, g, b), count)

    data = struct.pack('>B', len(palette))
    for color, count in palette:
        for c in color:
            data += struct.pack('>B', c)

    return data


def encode(in_file, quality=4):
    orig_img = Image.open(in_file)
    if orig_img.mode == 'RGBA':
        # Bake alpha layer into RGB
        orig_img = stripalpha(orig_img)
    encoded_img = Image.new('RGB', orig_img.size)

    band_data = []
    for i in range(3):
        band_data.append(list(orig_img.getdata(i)))
    color_map = ProcessPixels.organize(quality, band_data)

    # Format: ((r, g, b), count)
    color_priority = sorted(color_map.items(), key=lambda item: item[1],
                            reverse=True)[:2**(quality+4)-2]  # -2 because the max value (eg 1111) is treated seperately
    # Possible optimizations at this point (will probably move into c again for speed):
    # Reserve values 0xf..ff and 0xf..fe (or more) for grouped colors
    # 0xf..ff will be folloed by 5 bits indicating how many times the next color should be repeated (inclusive)
    # and one bit indicating if the color should flow down or right

    b_header = _genheader(encoded_img)
    b_palette = _genpalette(color_priority)

    with open('out.ig', 'wb') as f:
        f.write(b_header + b_palette)


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
