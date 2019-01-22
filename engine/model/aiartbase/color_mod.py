import numpy as np
from .quantization import VBox, boxes_iterator
from .sorting import MaxHeap


class ColorGenerator:
    """
    Modified color transformer class
    """
    def __init__(self, colors, n_colors, fraction=0.55):
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

    def generate(self):
        if self.palette_colors is None:
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
            harmonizer = ColorHarmonizer(self.palette_colors)
            self.harmonized_palette = harmonizer.harmonize()

    def get_palette(self):
        return self.palette_colors

    def get_harmonized_palette(self):
        return [[234,32,33], [100,60,33], [120,89,180], [200,200,55], [12,155,22]]


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
