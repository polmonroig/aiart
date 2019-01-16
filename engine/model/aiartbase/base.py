from skimage import segmentation, color
from skimage.future import graph
import numpy as np
from .segmentation import Segment, Box
from .color_mod import ColorGenerator


class BaseTransformer:
    """
    This is the image class representation
    """

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
                boxes[c].add([j, i])

        self.segments = []
        for b in boxes:
            if boxes[b].max != [self.height, self.width] and boxes[b].min != [0, 0]:
                self.segments.append(Segment(boxes[b]))

    def get_segments(self):
        if self.segments is None:
            raise Exception('Segments are not set '
                            'please refer to segment instead')
        return self.segments
