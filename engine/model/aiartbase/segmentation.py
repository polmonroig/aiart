from .image_utils import color_weight
from math import sqrt, atan, cos, sin, degrees


class Box:
    """
    This box class is a helper class
    useful to classify the bounding boxes
    """

    GRAVITY = 0.1

    def __init__(self, i, j):
        self.min = [j, i]
        self.max = [0, 0]
        self.pixels = []
        self.size = 0
        self._average_color = [0, 0, 0]
        self._weight = None
        self.image_width = j
        self.image_height = i
        self._x = None
        self._y = None
        self._mass = None

    def add(self, pixel, pixel_color):

        # Update max and min values for the bounding box
        if pixel[0] > self.max[0]: self.max[0] = pixel[0]
        if pixel[0] < self.min[0]: self.min[0] = pixel[0]
        if pixel[1] > self.max[1]: self.max[1] = pixel[1]
        if pixel[1] < self.min[1]: self.min[1] = pixel[1]

        # Add a new pixel inside this box
        self.pixels.append(pixel)
        self._average_color[0] += pixel_color[0]
        self._average_color[1] += pixel_color[1]
        self._average_color[2] += pixel_color[2]
        self.size += 1

    @property
    def average_color(self):
        if not self.empty():
            tmp_color = self._average_color.copy()
            tmp_color[0] /= self.size
            tmp_color[1] /= self.size
            tmp_color[2] /= self.size
        else:
            raise Exception("The box is empty")
        return tmp_color

    def get_dir(self):
        val_y = 0.8 + 0.4 * (self.y / self.image_height + 0.5)
        val_x = 0.8 + 0.4 * (self.x / self.image_width + 0.5)
        return val_x * val_y

    def set_weight_dir(self, f):
        weight_dir = {"x": 0, "y": 0}
        angle_x = angle_y = 0
        if self.x == 0:
            angle_x = 0
            angle_y = 1
        elif not (self.x == self.y == 0):
            angle = atan(self.y / float(self.x))
            angle_x = cos(angle)
            angle_y = sin(angle)
        weight_dir['x'] = f * angle_x
        weight_dir['y'] = f * angle_y
        if (self.x < 0 and weight_dir['x'] > 0) or (self.x > 0 and weight_dir['x'] < 0):
            weight_dir['x'] = -weight_dir['x']
        if (self.y < 0 and weight_dir['y'] > 0) or (self.y > 0 and weight_dir['y'] < 0):
            weight_dir['y'] = -weight_dir['y']
        return weight_dir

    @property
    def weight(self):
        """
        Calculate:
            1. Size = self.size
        :return: Box weight
        """
        if self.empty():
            raise Exception("The box is empty")
        if self._weight is None:
            f = sqrt(pow(self.x, 2) + pow(self.y, 2)) * self.mass * self.GRAVITY
            self._weight = self.set_weight_dir(f)
        return self._weight

    @property
    def x(self):
        if self._x is None:
            x_diff = (self.max[0] - self.min[0]) / 2
            x = int(x_diff) + self.min[0]
            self._x = x - (self.image_width / 2)
        return self._x

    @property
    def y(self):
        if self._y is None:
            y_diff = (self.max[1] - self.min[1]) / 2
            y = int(y_diff) + self.min[1]
            self._y = -y + (self.image_height / 2)
        return self._y

    def ratio(self):
        margin = 1
        x_diff = (self.max[0] - self.min[0]) / 2
        y_diff = (self.max[1] - self.min[1]) / 2
        # Calculate ratio
        ratio = 1
        if abs(x_diff - y_diff) > margin:
            if x_diff > y_diff:
                ratio = 0.8
            else:
                ratio = 1.2
        return ratio

    @property
    def mass(self):
        if self._mass is None:
            # Calculate Dir
            direction = self.get_dir()
            color_w = color_weight(self.average_color)
            r = self.ratio()
            self._mass = self.size * r * color_w * direction
        return self._mass

    def empty(self):
        return self.size == 0


class Segment:
    """
    Segment class saves the properties of a segment
    """

    def __init__(self, b):
        x_diff = (b.max[0] - b.min[0]) / 2
        y_diff = (b.max[1] - b.min[1]) / 2
        if x_diff < y_diff:
            self.radius = int(x_diff)
            self.ratio_x = 1
            self.ratio_y = y_diff / x_diff
        else:
            self.radius = int(y_diff)
            self.ratio_y = 1
            self.ratio_x = x_diff / y_diff
        self.x = int(x_diff) + b.min[0]
        self.y = int(y_diff) + b.min[1]
        self.weight = b.weight

    def get_weight(self):
        x = sqrt(self.weight['y'] ** 2 + self.weight['x'] ** 2) % 100
        return 100

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

    def get_ratio(self):
        return self.ratio_x, self.ratio_y
