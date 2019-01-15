from model.ImagePalette import ImagePalette


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

    def get_palette(self, n_colors):
        """
        Returns an instance of the palette class
        """
        return ImagePalette(self.image, n_colors)
