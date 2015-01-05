#!/usr/bin/python3

from PIL import Image
import sys


def stripalpha(img):
    new_img = img.convert('RGB')
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            color = list(img.getpixel((x, y)))
            new_color = []
            for i in range(3):
                # new_color.append(int(color[i] + (255 - color[i]) * (255 - color[3]) / 255))
                new_color.append(int(255 + color[3]*(color[0] / 255 - 1)))
            if new_color != color[:3]:
                new_img.putpixel((x, y), tuple(new_color))
                # putpixel is kinda slow so I also tried using a bytestring with the pixel data to read it all
                # into the image at once. It took almost exactly the same amount to time to run.

    return new_img


def encode(in_file, quality=7):
    orig_img = Image.open(in_file)
    if orig_img.mode == 'RGBA':
        # Bake alpha layer into RGB
        orig_img = stripalpha(orig_img)
    encoded_img = Image.new('RGB', orig_img.size)


def main():
    if len(sys.argv) < 2:
        print('Usage: ./Encode [file] [quality 0-9]')
        return
    if len(sys.argv) < 3:
        encode(sys.argv[1])
    else:
        encode(sys.argv[1], int(sys.argv[2]))

if __name__ == '__main__':
    main()