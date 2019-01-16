

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
        x_diff = (b.max[0] - b.min[0]) / 2
        y_diff = (b.max[1] - b.min[1]) / 2
        if x_diff < y_diff:
            self.radius = int(x_diff)
            self.ratio_x = 1
            self.ratio_y = int(y_diff / x_diff)
        else:
            self.radius = int(y_diff)
            self.ratio_y = 1
            self.ratio_x = int(x_diff / y_diff)
        self.x = int(x_diff) + b.min[0]
        self.y = int(y_diff) + b.min[1]
        self.intensity = 100

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

    def get_radius(self):
        """
        Segment radius
        :return: self.radius
        """
        return self.radius

    def get_int(self):
        return self.intensity

    def get_ratio(self):
        return self.ratio_x, self.ratio_y
