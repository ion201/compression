#!/usr/bin/python3

from PIL import Image
import struct
import sys
import math

import ProcessPixels as PP


def stripalpha(img):
    pixel_array = img.load()
    new_img = img.convert('RGB')
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            color = list(pixel_array[x, y])
            new_color = []
            for i in range(3):
                # new_color.append(int(color[i] + (255 - color[i]) * (255 - color[3]) / 255))
                new_color.append(int(255 + color[3]*(color[i] / 255 - 1)))
            if new_color != color[:3]:
                pixel_array[x, y] = tuple(new_color)

    return new_img


def _genheader(img):
    #Header reserves the first 6 bytes
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

    # 16-256 colors (4-8 bits correspond to quality 0-4) Each color is encoded by 6 bytes (RRGGBB).
    # color_map = {}
    # scan_quality = quality
    # while len(color_map) < 2**(quality+4)-1 and scan_quality < 5:
    #     color_map = {}
    #     pix_array_orig = orig_img.load()
    #     for y in range(orig_img.size[1]):
    #         for x in range(orig_img.size[0]):
    #             pixel = tuple(min(c // (100-math.floor(scan_quality**3))
    #                           * (100-math.floor(scan_quality**3))
    #                           + (100-math.floor(scan_quality**3)) // 3, 255)
    #                           for c in pix_array_orig[x, y])
    #             try:
    #                 color_map[pixel] += 1
    #             except KeyError:
    #                 color_map[pixel] = 1
    #     scan_quality += 1
    #     if scan_quality == 5:  # past 5, the quality gets worse
    #         scan_quality = 4.3  # Magic numbers are fun! It's close to, but not quite, 100**(1/3)

    # while len(color_map) < 2**(quality+4)-1 and scan_quality < 5:
    #     color_map = {}
    #     band_data = []
    #     for i in range(3):
    #         band_data.append(list(orig_img.getdata(i)))
    #     for i in range(0, len(band_data[0]), 1):
    #         pixel = tuple(min(band_data[band][i] // (100-math.floor(scan_quality**3))
    #                           * (100 - math.floor(scan_quality ** 3))
    #                           + (100-math.floor(scan_quality**3)) // 3, 255)
    #                       for band in range(3))
    #         try:
    #             color_map[pixel] += 1
    #         except KeyError:
    #             color_map[pixel] = 1
    #     scan_quality += 1
    #     if scan_quality == 5:
    #         scan_quality = 4.3

    band_data = []
    for i in range(3):
        band_data.append(list(orig_img.getdata(i)))
    color_map = PP.organize(quality, band_data)

    # Format: ((r, g, b), count)
    color_priority = sorted(color_map.items(), key=lambda item: item[1],
                            reverse=True)[:2**(quality+4)-2]  # -2 because the max value (eg 1111) is treated seperately
    print(len(color_priority))
    print(color_priority[:10])

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
