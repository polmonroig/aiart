import cv2
import numpy as np


def string_to_image(file_stream):
    image_string = np.fromstring(file_stream, np.uint8)
    image = cv2.imdecode(image_string, cv2.IMREAD_COLOR)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def image_to_string(image, file_extension):
    return cv2.imencode(file_extension, image)[1].tostring()


def hsv_palette(palette):
    return cv2.cvtColor(palette.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_RGB2HSV).reshape(-1, 3)


def image_resize(self, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size

    (h, w) = self.shape[:2]
    if not (width is None and height is None):
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)

        else:
            r = width / float(w)
            dim = (width, int(h * r))

        self = cv2.resize(self, dim, interpolation=inter)
    return self


def is_monochromatic(pal):
    tmp = hsv_palette(pal)
    hue_margin = 35
    low_sat = True
    low_hue = True
    sat_margin = 5
    for i, palette_color in enumerate(tmp):
        if palette_color[1] > sat_margin:
            low_sat = False
        for j, cmp_palette_color in enumerate(tmp):
            if i != j:
                if palette_color[0] > cmp_palette_color[0]:
                    if hue_margin <= palette_color[0] - cmp_palette_color[0]:
                        low_hue = False
                else:
                    if hue_margin <= cmp_palette_color[0] - palette_color[0]:
                        low_hue = False

    return low_sat or low_hue
