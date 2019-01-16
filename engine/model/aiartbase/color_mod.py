import numpy as np

class ColorGenerator:
    """
    Modified color transformer class
    """
    def __init__(self, colors, n_colors):
        if not isinstance(colors, list) or not colors:
            raise Exception('`colors` MUST be a list '
                            'that contains items not %s'.format(colors))

        if n_colors < 2 or n_colors > 256:
            raise Exception('`max_color` MUST be an integer value between '
                            '2 and 256. not %s'.format(n_colors))

        self.colors = colors
        self.n_colors = n_colors

        self.palette_colors = None

        self.harmonized_palette = None

    def generate(self):
        if self.palette_colors is None:
            n_iter = 0
            while n_iter < self.n_colors:

                n_iter += 1
            self.palette_colors = [[25, 25, 25], [65, 65, 65],
                                   [90, 90, 90], [200, 65, 200]]
            harmonizer = ColorHarmonizer(self.palette_colors)
            self.harmonized_palette = harmonizer.harmonize()

    def get_palette(self):
        return np.append(self.palette_colors, self.harmonized_palette).reshape(-1, 3).tolist()

    def max_range(self):
        max_b = max_g = max_r = -1
        min_b = min_g = min_r = 256
        for color in self.colors:
            if min_r > color[0]:
                min_r = color[0]
            if max_r < color[0]:
                max_r = color[0]
            if min_b > color[2]:
                min_b = color[2]
            if max_b < color[2]:
                max_b = color[2]
            if min_g > color[1]:
                min_g = color[1]
            if max_g < color[1]:
                max_g = color[1]

        ranges = [max_r - min_r,
                  max_g - min_g,
                  max_b - min_b]
        return max(ranges)


class ColorHarmonizer:
    """
    Harmonizes colors
    """
    def __init__(self, colors):
        self.colors = colors
        self.harmonized_colors = None

    def harmonize(self):
        if self.harmonized_colors is None:
            self.harmonized_colors = self.colors
        return self.harmonized_colors
