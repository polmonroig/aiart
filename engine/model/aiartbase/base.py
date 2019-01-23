from skimage import segmentation, color
from skimage.future import graph
import numpy as np
from .segmentation import Segment, Box
from .color_mod import ColorGenerator
from .image_utils import image_resize
from math import sqrt
from .image_utils import composition_level


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

        for i in range(0, labels.shape[0]):
            for j in range(0, labels.shape[1]):
                c = labels[i][j]
                if boxes.get(c) is None:
                    boxes[c] = (Box(self.height, self.width))
                boxes[c].add([j, i], self.image[i, j])

        self.segments = []
        force = {'x': 0, 'y': 0, 'mod': 0}
        for b in boxes:
            if boxes[b].max != [self.height, self.width] and boxes[b].min != [0, 0]:
                self.segments.append(Segment(boxes[b]))
                w = boxes[b].weight
                force['x'] += w['x']
                force['y'] += w['y']
        self.n_segments = len(self.segments)
        force['mod'] = sqrt(force['x'] ** 2 + force['y'] ** 2)
        self.balance = composition_level(force['mod'])

    def get_segments(self):
        if self.segments is None:
            raise Exception('Segments are not set '
                            'please refer to segment instead')
        return self.segments

    def composition(self):
        return self.balance

    def harmony(self):
        return self.palette.harmony
