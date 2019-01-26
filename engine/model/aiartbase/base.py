from skimage import segmentation, color
from skimage.future import graph
import numpy as np
from .segmentation import Segment, Box
from .color_mod import ColorGenerator
from .image_utils import image_resize, composition_level
from math import sqrt, pi, atan, cos, sin
from .shared_variables import MAX_SEGMENT_RATIO, GRAVITY


class BaseTransformer:
    """
    This is the image class representation
    """

    INFINITY = float('inf')

    def __init__(self, image):
        """
        This is the class constructor
        """

        if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
            raise Exception('`image` MUST be a numpy array '
                            'with 3 dimensions %s'.format(image))

        # Image to save
        self.image = image

        # Set height and width
        self.height = image.shape[0]
        self.width = image.shape[1]

        # Segments
        self.segments = None

        # image Palette
        self.palette = None

        self.n_segments = 0

        self.balance = 0

        self.segment_ratio = 0

        self.force = {}

    def calculate_colors(self, n_colors):
        """
        Returns an instance of the palette class
        """
        if self.palette is None:
            colors = []
            for i in range(self.height):
                for j in range(self.width):
                    colors.append(self.image[i][j])
            self.palette = ColorGenerator(colors, n_colors)
            self.palette.generate()
        else:
            raise Exception('Palette has already been calculated '
                            'please refer to get_palette instead')

    def get_palette(self):
        if self.palette is None:
            raise Exception('Palette is not set '
                            'please refer to calculate_colors instead')

        return self.palette.get_palette()

    def get_harmonized_palette(self):
        if self.palette is None:
            raise Exception('Palette is not set '
                            'please refer to calculate_colors instead')

        return self.palette.get_harmonized_palette()

    @staticmethod
    def _eucledian_diff(arr_a, arr_b):
        if len(arr_a) != len(arr_b):
            raise Exception("Arrays have different lengths")
        diff = 0.0
        for a, b in zip(arr_a, arr_b):
            diff += (b - a) ** 2

        return sqrt(diff)

    def get_color_positions(self):
        resize_value = 2
        reduced_image = image_resize(self.image, width=int(self.width / resize_value))
        positions = []
        differences = []
        for i in range(0, self.palette.n_colors):
            positions.append([0, 0])
            differences.append(self.INFINITY)
        tmp_colors = self.palette.palette_colors.astype(np.float32).reshape(-1, 3).tolist()
        i = 0
        while i < reduced_image.shape[0]:
            j = 0
            while j < reduced_image.shape[1]:
                im_color = reduced_image[i][j]
                for k in range(len(tmp_colors)):
                    diff = self._eucledian_diff(im_color, tmp_colors[k])
                    if diff < differences[k]:
                        positions[k][1] = (i * resize_value) / self.height
                        positions[k][0] = (j * resize_value) / self.width
                        differences[k] = diff
                j += 1
            i += 1

        return positions

    def segment(self, compactness=50, n_segments=100,
                connectivity=1, sigma=500, num_cuts=200):

        """
        Function responable of image segmentation
        """
        if self.segments is None:
            # Make segmentation slice
            labels1 = segmentation.slic(self.image,
                                        compactness=compactness,
                                        n_segments=n_segments)

            # Convert slice into rgb image based on avg
            out1 = color.label2rgb(labels1, self.image, kind='avg')

            # Complete segmentation using graph cut
            g = graph.rag_mean_color(self.image, labels1, mode='similarity', connectivity=connectivity, sigma=sigma)
            labels = graph.cut_normalized(labels1, g, num_cuts=num_cuts)

            image_segmentation = color.label2rgb(labels, self.image, kind='avg')
            self._set_boxes(labels)

    def _set_boxes(self, labels):
        """
        Calculates every bounding box
        """
        # Calculates the edge of every box

        boxes = {}
        segments_size = 0
        for i in range(0, labels.shape[0]):
            for j in range(0, labels.shape[1]):
                c = labels[i][j]
                if boxes.get(c) is None:
                    boxes[c] = (Box(self.height, self.width))
                boxes[c].add([j, i], self.image[i, j])

        self.segments = []
        self.force = {'x': 0, 'y': 0, 'mod': 0}
        for b in boxes:
            if boxes[b].max != [self.height, self.width] and boxes[b].min != [0, 0]:
                w = boxes[b].weight
                relative_weight = sqrt(w['x'] ** 2 + w['y'] ** 2) / (((self.width * self.height) / 4) * 0.001 * (
                            int(sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)) / 2) * 1.2)
                self.segments.append(Segment(boxes[b], int(relative_weight)))
                segments_size += boxes[b].size
                self.segments.append(Segment(boxes[b]))
                self.force['x'] += w['x']
                self.force['y'] += w['y']
        self.segment_ratio = (segments_size / (self.width * self.height)) * 100
        self.n_segments = len(self.segments)
        self.force['mod'] = sqrt(self.force['x'] ** 2 + self.force['y'] ** 2)
        if self.segment_ratio < MAX_SEGMENT_RATIO:
            self.force['x'] = -self.force['x']
            self.force['y'] = -self.force['y']
        self.balance = composition_level(self.force['mod'])

    def get_balance_attributes(self):
        # Generates sample image with bounding boxes
        div = 2
        f = int(sqrt((self.width / div) ** 2 + (self.height / div) ** 2)) / 2
        weight_dir = {"x": 0, "y": 0}
        angle_x = angle_y = 0
        if self.force['x'] == 0:
            angle_x = 0
            angle_y = 1
        elif not (self.force['x'] == self.force['y'] == 0):
            angle = atan(self.force['y'] / float(self.force['x']))
            angle_x = cos(angle)
            angle_y = sin(angle)
            # print("Angle: ", degrees(angle))
        weight_dir['x'] = f * angle_x
        weight_dir['y'] = f * angle_y
        if (self.force['x'] < 0 and weight_dir['x'] > 0) or (self.force['x'] > 0 and weight_dir['x'] < 0):
            weight_dir['x'] = -weight_dir['x']
        if (self.force['y'] < 0 and weight_dir['y'] > 0) or (self.force['y'] > 0 and weight_dir['y'] < 0):
            weight_dir['y'] = -weight_dir['y']

        mass = self.force['mod'] / (f * GRAVITY)
        size = mass
        radius = sqrt(mass / pi)
        pos_x = weight_dir['x'] + self.width / 2
        pos_y = self.height / 2 - weight_dir['y']
        return radius, pos_x, pos_y, weight_dir

    def get_segments(self):
        if self.segments is None:
            raise Exception('Segments are not set '
                            'please refer to segment instead')
        a = []
        for seg in self.segments:
            a.append((seg.x / self.width, seg.y / self.height,
                      seg.get_weight(), seg.get_scale()[0] / self.width,
                      seg.get_scale()[1] / self.width))
        return a

    def get_balanced_segments(self):
        if self.segments is None:
            raise Exception('Segments are not set '
                            'please refer to segment instead')
        balanced = self.get_segments()
        radius, pos_x, pos_y, weight_dir = self.get_balance_attributes()
        weight_dir['mod'] = sqrt(weight_dir['x']**2 + weight_dir['y']**2)
        max_weight = (((self.width * self.height) / 4) * 0.001 * (
                            int(sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)) / 2) * 1.2)
        weight = weight_dir['mod'] / max_weight
        if self.segment_ratio >= MAX_SEGMENT_RATIO:
            weight = 0
        balanced.append((pos_x / self.width, pos_y / self.height,
                        weight, radius / self.width,
                        radius / self.width))
        return balanced

    def composition(self):
        return self.balance

    def harmony(self):
        return self.palette.harmony
