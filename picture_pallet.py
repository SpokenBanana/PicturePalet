from PIL import Image
import math
import random


def get_similarity(color1, color2):
    return math.fabs(color1[0] - color2[0]) + math.fabs(color1[1] - color2[1]) + math.fabs(color1[2] - color2[2])


class Palette():
    def __init__(self, first, second):
        self.palette = {'image': first}
        self.dest = {'image': second}

        # need the original image for reference
        self.original = Image.new('RGB', second.size, 'white')
        self.original.paste(second, (0, 0))

        # getcolors returns tuples which are immutable we want to be able to change the values, so convert them to lists
        self.palette['colors'] = [[x[0], x[1]] for x in first.getcolors(1000000)]
        self.dest['colors'] = [[x[0], x[1]] for x in second.getcolors(1000000)]

    # return the color most close to the color given
    def get_similar_color(self, color):
        ranks = [get_similarity(color, x[1]) for x in self.palette['colors']]
        index = ranks.index(min(ranks))

        self.palette['colors'][index][0] -= 1
        if self.palette['colors'][index][0] <= 0:
            return self.palette['colors'].pop(index)[1]

        return self.palette['colors'][index][1]

    def generate_picture(self, file_name="image.png"):
        # need to fit the pallet to the destination image to make sure we have enough pixels
        self.palette['image'] = self.palette['image'].resize((self.dest['image'].size[0], self.dest['image'].size[1]),
                                                             Image.NEAREST)
        self.dest['image'].paste(self.palette['image'], (0, 0))

        # each iteration we will randomly switch two pixels if they bring us closer to the destination image
        for i in xrange(2000000):
            first = (random.randrange(0, self.dest['image'].size[0]),
                     random.randrange(0, self.dest['image'].size[1]))
            second = (random.randrange(0, self.dest['image'].size[0]),
                      random.randrange(0, self.dest['image'].size[1]))
            original_first = self.original.getpixel(first)
            original_second = self.original.getpixel(second)
            dest_first = self.dest['image'].getpixel(first)
            dest_second = self.dest['image'].getpixel(second)

            if get_similarity(original_first, dest_first) + get_similarity(original_second, dest_second) > \
                            get_similarity(original_first, dest_second) + get_similarity(original_second, dest_first):
                temp_color = self.dest['image'].getpixel(first)
                self.dest['image'].putpixel(first, self.dest['image'].getpixel(second))
                self.dest['image'].putpixel(second, temp_color)

        self.dest['image'].save(file_name)
        return file_name
