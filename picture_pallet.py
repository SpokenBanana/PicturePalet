from PIL import Image
import math
import random


def color_diff(color1, color2):
    return math.fabs(color1[0] - color2[0]) + math.fabs(color1[1] - color2[1]) + math.fabs(color1[2] - color2[2])


class Palette:
    def __init__(self, first, second):
        self.palette = first
        self.dest = second

        # need the original image for reference
        self.original = Image.new('RGB', second.size, 'white')
        self.original.paste(second, (0, 0))

    def generate_picture(self, file_name="image.png"):
        # need to fit the pallet to the destination image to make sure we have enough pixels
        self.palette = self.palette.resize((self.dest.size[0], self.dest.size[1]),
                                           Image.NEAREST)
        self.dest.paste(self.palette, (0, 0))

        # each iteration we will randomly switch two pixels if they bring us closer to the destination image
        for i in xrange(500000):
            first = (random.randrange(0, self.dest.size[0]),
                     random.randrange(0, self.dest.size[1]))
            second = (random.randrange(0, self.dest.size[0]),
                      random.randrange(0, self.dest.size[1]))

            original_first = self.original.getpixel(first)
            original_second = self.original.getpixel(second)

            dest_first = self.dest.getpixel(first)
            dest_second = self.dest.getpixel(second)

            if color_diff(original_first, dest_first) + color_diff(original_second, dest_second) > \
                            color_diff(original_first, dest_second) + color_diff(original_second, dest_first):
                self.dest.putpixel(first, dest_second)
                self.dest.putpixel(second, dest_first)

        self.dest.save(file_name)
        return file_name
