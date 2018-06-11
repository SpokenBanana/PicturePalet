from PIL import Image
import random


def color_diff(color1, color2):
    mean = (color1[0] + color2[0]) // 2
    r = color1[0] - color2[0]
    g = color1[1] - color2[1]
    b = color1[2] - color2[2]
    return (((512 + mean) * r * r) >> 8) + 4 * g * g + (
           ((767 - mean) * b * b) >> 8)


class Palette:
    def __init__(self, first, second):
        self.palette = first
        self.destination = second

        # need the original image for reference
        self.original = Image.new('RGB', second.size, 'white')
        self.original.paste(second, (0, 0))

    def generate_picture(self, file_name="/tmp/image.png"):
        size = list(self.destination.size)
        if size[0] > 700:
            aspect = size[1] / float(size[0])
            size[0] = 600
            size[1] = int(600 * aspect)
            self.destination = self.destination.resize(
                size, Image.BILINEAR).convert('RGB')

            self.original = self.original.resize(
                size, Image.BILINEAR).convert('RGB')

        # fit the pallet to the destination image
        self.palette = self.palette.resize(size, Image.BILINEAR).convert('RGB')
        self.destination.paste(self.palette, (0, 0))

        # randomly switch two pixels if they bring us closer to the image
        for i in range(1000000):
            first = (random.randrange(0, self.destination.size[0]),
                     random.randrange(0, self.destination.size[1]))
            second = (random.randrange(0, self.destination.size[0]),
                      random.randrange(0, self.destination.size[1]))
            original_first = self.original.getpixel(first)
            original_second = self.original.getpixel(second)
            dest_first = self.destination.getpixel(first)
            dest_second = self.destination.getpixel(second)
            if color_diff(original_first, dest_first) + \
                    color_diff(original_second, dest_second) > \
                    color_diff(original_first, dest_second) + \
                    color_diff(original_second, dest_first):
                self.destination.putpixel(first, dest_second)
                self.destination.putpixel(second, dest_first)

        self.destination.save(file_name)
        return file_name
