import numpy as np
from .quantization import VBox, boxes_iterator, templates, get_closest_hue
from .sorting import MaxHeap
from .image_utils import hsv_palette, rgb_palette, harmony_level
from math import degrees, radians
from .shared_variables import hue_margin


class ColorGenerator:
    """
    Modified color transformer class
    """
    def __init__(self, colors, n_colors, fraction=0.75):
        if not isinstance(colors, list) or not colors:
            raise Exception('`colors` MUST be a list '
                            'that contains items not %s'.format(colors))

        if n_colors < 2 or n_colors > 256:
            raise Exception('`max_color` MUST be an integer value between '
                            '2 and 256. not %s'.format(n_colors))

        # Image color list
        self.colors = colors

        # Image n_colors to calculate
        self.n_colors = n_colors

        # Color palettes
        self.palette_colors = None

        self.harmonized_palette = None

        self.FRACTION = fraction

        self.harmony = 0

    def generate(self):
        if self.palette_colors is None:
            # Quantization
            self.palette_colors = np.array([])
            vbox = VBox(self.colors, cmp_type='fraction')
            pq_1 = MaxHeap()
            pq_1.push(vbox)
            boxes_iterator(pq_1, self.n_colors * self.FRACTION, cmp_type='fraction')
            pq_2 = MaxHeap()
            while not pq_1.empty():
                tmp = pq_1.top()
                tmp.cmp_type = 'other'
                pq_2.push(tmp)
                pq_1.pop()

            boxes_iterator(pq_2, self.n_colors * (1 - self.FRACTION), cmp_type='other')

            while not pq_2.empty():
                self.palette_colors = np.append(self.palette_colors, pq_2.top().average)
                pq_2.pop()
            # Harmonization
            self.palette_colors = self.palette_colors.reshape(-1, 3)
            harmonizer = ColorHarmonizer(self.palette_colors.reshape(1, -1, 3))
            self.palette_colors = self.palette_colors.reshape(-1, 3)
            self.harmonized_palette = harmonizer.harmonize().reshape(-1, 3)
            self.harmony = harmony_level(harmonizer.harmony)

    def get_palette(self):
        return self.palette_colors

    def get_harmonized_palette(self):
        return self.harmonized_palette


class ColorHarmonizer:
    """
    Harmonizes colors
    """
    def __init__(self, colors):
        if colors.ndim != 3:
            raise Exception("Number of dimensions is incorrect")
        self.colors = colors.copy()
        self.harmonized_colors = None
        self.best_template = None
        self.harmony = 0

    def harmonize(self):
        if self.harmonized_colors is None:
            self.color_harmony()
            self.harmonized_colors = hsv_palette(self.colors)
            for it, col in enumerate(self.harmonized_colors):
                if self.best_template[3][it] != -1:
                    col[0] = (degrees(self.best_template[3][it]) / 2)
            self.harmonized_colors = rgb_palette(self.harmonized_colors)
        return self.harmonized_colors

    def color_harmony(self):
        total_harmony = [float(-1), 0, 0, np.zeros(self.colors.shape[1])]
        for template in templates:
            degree_harmony = [-1, 0, template]
            for degree in range(360):
                current_harmony = [0, np.zeros(self.colors.shape[1])]
                for it, col in enumerate(hsv_palette(self.colors)):
                    sat = radians((col[1] * 255) / 100)
                    hue = radians((col[0])*2)
                    closest_hue = get_closest_hue(template, degree, hue)
                    current_harmony[0] += sat * closest_hue[0]
                    current_harmony[1][it] = closest_hue[1]
                if degree_harmony[0] > current_harmony[0] or degree_harmony[0] == -1:
                    degree_harmony = [current_harmony[0], degree, template, current_harmony[1]]
            if total_harmony[0] > degree_harmony[0] or total_harmony[0] == -1:
                total_harmony = degree_harmony
        self.best_template = total_harmony
        print("tmp: ", self.best_template)
        self.harmony = self.best_template[0]

