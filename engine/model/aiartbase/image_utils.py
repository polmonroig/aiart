import cv2
import numpy as np


def string_to_image(file_stream):
    image_string = np.fromstring(file_stream, np.uint8)
    image = cv2.imdecode(image_string, cv2.IMREAD_COLOR)
    return image


def image_to_string(image, file_extension):
    return cv2.imencode(file_extension, image)[1].tostring()
