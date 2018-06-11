from PIL import Image
import random
import numba


@numba.jit(nopython=True)
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

    def generate_picture(self, file_name="/tmp/image.png", iterations=2000000):
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

        original = self.original.load()
        destination = self.destination.load()
        for _ in range(iterations):
            fx, fy = (random.randrange(self.destination.size[0]),
                      random.randrange(self.destination.size[1]))
            sx, sy = (random.randrange(self.destination.size[0]),
                      random.randrange(self.destination.size[1]))

            original_first = original[fx, fy]
            original_second = original[sx, sy]
            destination_first = destination[fx, fy]
            destination_second = destination[sx, sy]

            if color_diff(original_first, destination_first) + \
                    color_diff(original_second, destination_second) > \
                    color_diff(original_first, destination_second) + \
                    color_diff(original_second, destination_first):
                destination[fx, fy] = destination_second
                destination[sx, sy] = destination_first
        self.destination.save(file_name)
        return file_name
