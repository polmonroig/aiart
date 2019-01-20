import cv2
import numpy as np


def string_to_image(file_stream):
    image_string = np.fromstring(file_stream, np.uint8)
    image = cv2.imdecode(image_string, cv2.IMREAD_COLOR)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def image_to_string(image, file_extension):
    return cv2.imencode(file_extension, image)[1].tostring()


def is_monochromatic(palette):
    hue_margin = 35
    for i, palette_color in enumerate(palette):
        for j, cmp_palette_color in enumerate(palette):
            if i != j:
                if hue_margin > abs(palette_color[0] - cmp_palette_color[1]):
                    return True

    return False
