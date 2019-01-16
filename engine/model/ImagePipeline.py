from skimage import segmentation, color
from skimage.future import graph
from engine.model.aiartbase.segmentation import Segment, Box
from engine.model.ImagePalette import ImagePalette


class ImagePipeline:
    """
    This is the image class representation
    """
    def __init__(self, image):
        """
        This is the class constructor
        """
        # Image to save
        self.image = image

        # Segments
        self.segments = None

    def get_palette(self, n_colors):
        """
        Returns an instance of the palette class
        """
        return ImagePalette(self.image, n_colors)

    def segment(self, compactness=40, n_segments=450,
                connectivity=1, sigma=20, num_cuts=10):

        """
        Function responable of image segmentation
        """

        # Make segmentation slice
        labels1 = segmentation.slic(self.image,
                                    compactness=compactness,
                                    n_segments=n_segments)

        # Convert slice into rgb image based on avg
        out1 = color.label2rgb(labels1, self.image, kind='avg')

        # Complete segmentation using graph cut
        g = graph.rag_mean_color(self.image, labels1, mode='similarity', connectivity=connectivity, sigma=sigma)
        # labels = graph.cut_normalized(labels1, g,
        # thresh=thresh, num_cuts=num_cuts, in_place=in_place, max_edge=max_edge)
        labels = graph.cut_normalized(labels1, g, num_cuts=num_cuts)
        self._set_boxes(labels)

    def _set_boxes(self, labels):
        """
        Calculates every bounding box
        """

        boxes = {}

        # Calculates the edge of every box
        for i in range(0, labels.shape[0]):
            for j in range(0, labels.shape[1]):
                c = labels[i][j]
                if boxes.get(c) is None:
                    boxes[c] = (Box(self.image.shape[0], self.image.shape[1]))
                    boxes[c].add([j, i])

        self.segments = []
        for b in boxes:
            if boxes[b].max != [self.image.shape[0], self.image.shape[1]] and boxes[b].min != [0, 0]:
                self.segments.append(Segment(boxes[b]))

    def get_segments(self):
        return self.segments
