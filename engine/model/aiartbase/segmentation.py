

class Box:
    """
    This box class is a helper class
    useful to classify the bounding boxes
    """

    def __init__(self, i, j):
        self.min = [j, i]
        self.max = [0, 0]
        self.pixels = []
        self.size = 0

    def add(self, pixel):

        # Update max and min values for the bounding box
        if pixel[0] > self.max[0]: self.max[0] = pixel[0]
        if pixel[0] < self.min[0]: self.min[0] = pixel[0]
        if pixel[1] > self.max[1]: self.max[1] = pixel[1]
        if pixel[1] < self.min[1]: self.min[1] = pixel[1]

        # Add a new pixel inside this box
        self.pixels.append(pixel)
        self.size += 1


class Segment:
    """
    Segment class that represents a segment in an image
    """
    def __init__(self, b):
        self.x_diff = (b.max[0] - b.min[0]) / 2
        self.y_diff = (b.max[1] - b.min[1]) / 2
        self.x = int(self.x_diff) + b.min[0]
        self.y = int(self.y_diff) + b.min[1]
        self.weight = 100

    def get_x(self):
        """
        get x function
        :return: self.x
        """
        return self.x

    def get_y(self):
        """
        get y function
        :return: self.y
        """
        return self.y

    def get_weight(self):
        return self.weight

    def get_scale(self):
        return self.x_diff, self.y_diff
