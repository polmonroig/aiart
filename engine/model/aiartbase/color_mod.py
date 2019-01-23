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

        self.harmony = 0

    @staticmethod
    def _merge_colors(arr, left, right):
        if left < right:
            mid = int(left + (right - left) / 2)
            ColorGenerator._merge_colors(arr, left, mid)
            ColorGenerator._merge_colors(arr, mid + 1, right)
            ColorGenerator._merge(arr, left, right, mid)

    @staticmethod
    def _merge(arr, left, right, mid):
        copy_arr = []
        i, j = left, mid + 1
        while i <= mid and j <= right:
            if abs(arr[i][0] - arr[j][0]) <= int(hue_margin / 2):
                arr[i] = arr[j].copy()
            if arr[i][0] <= arr[j][0]:
                copy_arr.append(arr[i].copy())
                i += 1
            else:
                copy_arr.append(arr[j].copy())
                j += 1
        while i <= mid:
            copy_arr.append(arr[i].copy())
            i += 1
        while j <= right:
            copy_arr.append(arr[j].copy())
            j += 1
        for k in range(right - left + 1):
            arr[left + k] = copy_arr[k]

        return arr

    def merge_similar(self):
        hsv_colors = hsv_palette(self.palette_colors).astype(np.int16)
        self._merge_colors(hsv_colors, 0, self.n_colors - 1)
        self.palette_colors = np.array([hsv_colors[0]])
        j = 0
        for i in range(1, len(hsv_colors)):
            if (self.palette_colors[j][0] != hsv_colors[i][0] and
                    self.palette_colors[j][1] != hsv_colors[i][1] and
                    self.palette_colors[j][2] != hsv_colors[i][2]):
                self.palette_colors = np.append(self.palette_colors, hsv_colors[i]).reshape(-1, 3)
                j += 1
        self.palette_colors = rgb_palette(self.palette_colors).reshape(1, -1, 3)

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
            self.merge_similar()
            harmonizer = ColorHarmonizer(self.palette_colors.reshape(1, -1, 3))
            self.palette_colors = self.palette_colors.reshape(-1, 3)
            self.harmonized_palette = harmonizer.harmonize().reshape(1, 3)
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
            print(self.best_template)
            for it, col in enumerate(self.harmonized_colors):
                col[0] = col[0] + degrees(self.best_template[3][it])
            self.harmonized_colors = rgb_palette(self.harmonized_colors)
        return self.harmonized_colors

    def color_harmony(self):
        total_harmony = [float(-1), 0, 0, np.zeros(self.colors.shape[1])]
        for template in templates:
            degree_harmony = [-1, 0, template]
            for degree in range(360):
                current_harmony = [0, np.zeros(self.colors.shape[1])]
                for it, col in enumerate(hsv_palette(self.colors)):
                    sat = radians((col[1] * 100) / 255)
                    hue = radians((col[0] * 360) / 255)
                    closest_hue = get_closest_hue(template, degree, hue)
                    current_harmony[0] += sat * closest_hue[0]
                    current_harmony[1][it] = closest_hue[1]
                if degree_harmony[0] > current_harmony[0] or degree_harmony[0] == -1:
                    degree_harmony = [current_harmony[0], degree, template, current_harmony[1]]
            if total_harmony[0] > degree_harmony[0] or total_harmony[0] == -1:
                total_harmony = degree_harmony
        self.best_template = total_harmony
        self.harmony = self.best_template[0]

