
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
        return self.radius

    def get_int(self):
        return self.intensity

    def get_ratio(self):
        return self.ratio_x, self.ratio_y
