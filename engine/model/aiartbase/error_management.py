# Constants
MAX_IMAGE_SIZE = 200
MIN_IMAGE_SIZE = 10


def raise_incorrect_size(a, b):
    raise Exception("Error while parsing image: "
                    "image size must be between {} and {} pixels".format(a, b))


def rise_incorrect_file_extension():
    raise Exception("Error while parsing image: "
                    "image extension must be .jpg , .png or .jpeg")
