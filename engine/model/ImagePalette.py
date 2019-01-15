import numpy as np


class ImagePalette:
    """
    This is the image palette class responsible
    of storing the color palette of an image
    """

    def __init__(self, image, n_colors):
        self.palette = image.copy()
        self.n_colors = n_colors

    @staticmethod
    def _get_pos(arr, left, right, x, c):
        """
        Finds mid pos using dicotomic search
        """
        m = int((left + right) / 2)
        if left < right:
            if arr[m][0][c] == x:
                return m
            elif arr[m][0][c] > x:
                return ImagePalette._get_pos(arr, left, m - 1, x, c)
            else:
                return ImagePalette._get_pos(arr, m + 1, right, x, c)

        return left

    @staticmethod
    def _max_range(image):
        maxb = maxg = maxr = -1
        minb = ming = minr = 256
        for a in image:
            for color in a:
                if minb > color[0]: minb = color[0]
                if maxb < color[0]: maxb = color[0]
                if ming > color[1]: ming = color[1]
                if maxg < color[1]: maxg = color[1]
                if minr > color[2]: minr = color[2]
                if maxr < color[2]: maxr = color[2]
        rangeb = maxb - minb
        rangeg = maxg - ming
        ranger = maxr - minr
        if rangeb > ranger:
            if rangeb > rangeg:
                maxrange = "blue"
                limit = (rangeb / 2) + minb
            else:
                maxrange = "green"
                limit = (rangeg / 2) + ming
        elif ranger > rangeg:
            maxrange = "red"
            limit = (ranger / 2) + minr
        else:
            maxrange = "green"
            limit = (rangeg / 2) + ming

        return maxrange, limit

    @staticmethod
    def _get_buckets(image, src=False):
        bucket_range, limit = ImagePalette._max_range(image)
        if src:
            image = image.copy().reshape(-1, 3)

        b_view = image.view(dtype=[("blue", np.uint8),("green", np.uint8), ("red", np.uint8)])
        sorted_bucket = np.sort(b_view, order=[bucket_range], axis=0)
        channel = 0
        if bucket_range == "red":
            channel = 2
        elif bucket_range == "green":
            channel = 1

        size = ImagePalette._get_pos(sorted_bucket, 0, sorted_bucket.shape[0], limit, channel)

        return sorted_bucket[:size], sorted_bucket[size:]

    @staticmethod
    def _get_average(bucket):
        p_color = np.array([[[0, 0, 0]]])

        for color in bucket:
            p_color[0][0][2] += color[0][0]
            p_color[0][0][1] += color[0][1]
            p_color[0][0][0] += color[0][2]
        size = bucket.shape[0]
        if p_color[0][0][2] > 0: p_color[0][0][2] /= size
        if p_color[0][0][1] > 0: p_color[0][0][1] /= size
        if p_color[0][0][0] > 0: p_color[0][0][0] /= size
        return p_color[0][0]

    @staticmethod
    def _generate_i(image, colors, src=True):
        a, b = ImagePalette._get_buckets(image, src)
        if colors == 2:
            avg_left = ImagePalette._get_average(a)
            avg_right = ImagePalette._get_average(b)
            return np.array([avg_left, avg_right])
        elif colors > 2:
            left = ImagePalette._generate_i(a, colors / 2, False)
            right = ImagePalette._generate_i(b, colors / 2, False)
            return np.append(left, right)

    def _get_harmonized(self):
        """
        Image palette harmonization
        :return: a harmonized palette
        """
        return self.palette * 1.2

    def generate(self):
        self.palette = self._generate_i(self.palette, self.n_colors)
        harmonized_palette = self._get_harmonized()
        self.palette = np.append(self.palette, harmonized_palette)
        self.palette = self.palette.reshape(1, int(self.palette.shape[0] / 3), 3).astype(np.uint8)
        return self.palette.tolist()
