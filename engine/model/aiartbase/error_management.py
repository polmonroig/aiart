# Constants
MAX_IMAGE_SIZE = 2000
MIN_IMAGE_SIZE = 50
# Error messages
MONOCHROMATIC = 2
NO_SEGMENTS = 3
MANY_SEGMENTS = 4
ERROR_TYPE = 'error'
# Warnings
COMPOSITION_WARNING = 5
COLOR_WARNING = 6
WARNING_TYPE = 'warning'
# Success
COLOR_SUCCESS = 0
COMPOSITION_SUCCESS = 1
SUCCESS_TYPE = 'success'


def raise_incorrect_size():
    raise Exception("Error while parsing image: "
                    "image size must be between {} and {} pixels".format(MAX_IMAGE_SIZE, MIN_IMAGE_SIZE))


def rise_incorrect_file_extension():
    raise Exception("Error while parsing image: "
                    "image extension must be .jpg , .png or .jpeg")
