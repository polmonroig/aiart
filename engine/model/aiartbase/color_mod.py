import cv2
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

    def generate(self):
        self.palette_colors = []
