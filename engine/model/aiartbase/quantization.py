import numpy as np
from copy import deepcopy


class VBox:
    """
    VBox Class
    """

    def __init__(self, colors, cmp_type):
        self._ranges = None
        self.histogram = np.array(colors)
        self._average = None
        self._volume = None
        self.count = len(self.histogram)
        self.cmp_type = cmp_type
        self.min_ranges = None

    @property
    def ranges(self):
        if self._ranges is None:

            max_b = max_g = max_r = -1
            min_b = min_g = min_r = 256

            for current_color in self.histogram:
                if min_r > current_color[0]:
                    min_r = current_color[0]
                if max_r < current_color[0]:
                    max_r = current_color[0]
                if min_b > current_color[2]:
                    min_b = current_color[2]
                if max_b < current_color[2]:
                    max_b = current_color[2]
                if min_g > current_color[1]:
                    min_g = current_color[1]
                if max_g < current_color[1]:
                    max_g = current_color[1]

            self.min_ranges = [min_r, min_g, min_b]
            self._ranges = [max_r - min_r,
                            max_g - min_g,
                            max_b - min_b]
        return self._ranges

    @property
    def volume(self):
        if self._volume is None:
            self._volume = (self.ranges[0] + 1) \
                           * (self.ranges[1] + 1) \
                           * (self.ranges[2] + 1)
        return self._volume

    @property
    def copy(self):
        copied = deepcopy(self)
        copied._avg = None
        copied._volume = None
        copied.count = self.count
        copied._ranges = None
        return copied

    @property
    def average(self):
        if self._average is None:
            self._average = np.array([0, 0, 0])
            for color in self.histogram:
                self._average[0] += color[0]
                self._average[1] += color[1]
                self._average[2] += color[2]
            self._average[0] /= self.count
            self._average[1] /= self.count
            self._average[2] /= self.count
        return self._average

    def __lt__(self, other):
        if self.cmp_type == 'fraction':
            return self.count < other.count
        elif self.cmp_type == 'other':
            return (self.volume * self.count) < (other.volume * other.count)
        else:
            raise Exception('Unknown compare type')


def median_cut(box, cmp_type):
    max_channel = max(box.ranges)
    bucket_range = "blue"
    channel = 2
    limit = (box.ranges[2] / 2) + box.min_ranges[2]
    if max_channel == box.ranges[0]:
        bucket_range = 'red'
        limit = (box.ranges[0] / 2) + box.min_ranges[0]
        channel = 0
    elif max_channel == box.ranges[1]:
        bucket_range = 'green'
        limit = (box.ranges[1] / 2) + box.min_ranges[1]
        channel = 1

    b_view = box.histogram.view(dtype=[("red", np.uint8), ("green", np.uint8), ("blue", np.uint8)])
    sorted_bucket = np.sort(b_view, order=[bucket_range], axis=0)
    sorted_bucket = sorted_bucket.view(dtype=np.uint8)
    size = get_pos(sorted_bucket, 0, sorted_bucket.shape[0], int(limit), channel)

    return VBox(sorted_bucket.copy()[size:], cmp_type), VBox(sorted_bucket.copy()[:size], cmp_type)


def boxes_iterator(boxes, target, cmp_type):
    n_color = 1
    n_iter = 0
    while n_iter < 1000 and n_color < target:
        current_box = boxes.top().copy
        boxes.pop()
        if not current_box.count:
            boxes.push(current_box.copy)
            continue
        v_boxes = median_cut(current_box.copy, cmp_type)
        if not v_boxes:
            break
        boxes.push(v_boxes[0])
        if len(v_boxes) == 2:
            boxes.push(v_boxes[1])
            n_color += 1
        n_iter += 1


def get_pos(arr, left, right, x, c):
    m = int((left + right) / 2)
    if left < right:
        # print(arr[m][0])
        if arr[m][c] == x:
            return m
        elif arr[m][c] > x:
            return get_pos(arr, left, m - 1, x, c)
        else:
            return get_pos(arr, m + 1, right, x, c)

    return left
