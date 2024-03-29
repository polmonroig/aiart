# Load libraries
from google.cloud import vision
from google.cloud.vision import types
from model import storage, database
from flask import Blueprint, current_app, redirect, render_template, request, url_for, jsonify
from model.aiartbase.base import BaseTransformer
from model.aiartbase import image_utils
from .aiartbase import error_management as em
from numpy import append


# Global variables
crud = Blueprint('crud', __name__)


def get_vision_labels(content):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    image = types.Image(content=content)

    # Performs label detection on the image file
    objects = client.object_localization(
        image=image).localized_object_annotations

    response = client.face_detection(image=image)
    faces = response.face_annotations

    return faces


def process_image(file_stream, sigma, n_colors):

    messages = {"composition": {"type": em.SUCCESS_TYPE, "message": em.COMPOSITION_SUCCESS},
                "color": {"type": em.SUCCESS_TYPE, "message": em.COLOR_SUCCESS}}

    # Color Palette
    image = image_utils.string_to_image(file_stream)
    if image.shape[0] > em.MAX_IMAGE_SIZE or image.shape[1] > em.MAX_IMAGE_SIZE:
        em.raise_incorrect_size()
    if image.shape[0] <= em.MIN_IMAGE_SIZE or image.shape[1] <= em.MIN_IMAGE_SIZE:
        em.raise_incorrect_size()
    image_pipeline = BaseTransformer(image)
    image_pipeline.calculate_colors(n_colors)
    color_palette = image_pipeline.get_palette()
    harmonized_palette = image_pipeline.get_harmonized_palette()
    template = image_pipeline.palette.template

    if image_utils.is_monochromatic(color_palette):
        messages['color']['type'] = em.ERROR_TYPE
        messages['color']['message'] = em.MONOCHROMATIC

    color_positions = image_pipeline.get_color_positions()

    # Image segments
    image_pipeline.segment(sigma=sigma)
    segments = image_pipeline.get_segments()
    balanced_segments = image_pipeline.get_balanced_segments()

    color_palette = append(color_palette, harmonized_palette).reshape(-1, 3).tolist()

    # Error and warning management0
    if image_pipeline.n_segments == 0:
        messages['composition']['type'] = em.ERROR_TYPE
        messages['composition']['message'] = em.NO_SEGMENTS

    if image_pipeline.n_segments > 15:
        messages['composition']['type'] = em.ERROR_TYPE
        messages['composition']['message'] = em.MANY_SEGMENTS

    score = [int(image_pipeline.composition()), int(image_pipeline.harmony())]
    if score[0] < 100 and messages['composition']['type'] != em.ERROR_TYPE:
        messages['composition']['type'] = em.WARNING_TYPE
        messages['composition']['message'] = em.COMPOSITION_WARNING

    if score[1] < 100 and messages['color']['type'] != em.ERROR_TYPE:
        messages['color']['type'] = em.WARNING_TYPE
        messages['color']['message'] = em.COLOR_WARNING

    return color_palette, segments, balanced_segments, color_positions, messages, score, template


def upload_image_file(file, filename, content_type):
    """
    Upload the user uploaded file to Google Cloud Storage and retrieve
    its publicly accessible url.
    :param file: file
    :param filename: filename
    :param content_type:
    :return: public accessible url of image
    """
    if not file:
        return None

    public_url, name = storage.upload_file(file, filename, content_type)
    current_app.logger.info('Uploaded file {} as {}'.format(filename, public_url))

    return public_url, name


@crud.route('/submit', methods=['POST'])
def submit():
    """
    If an image was uploaded, update the data to point to the new image.
    :return: jsonify(request.get_data())
    """
    # Read the file stream first so multiple functions can process the stream
    # filename = request.files.get('file').filename
    # content_type = request.files.get('file').content_type
    file_stream = request.files.get('file').read()

    # image_url, name = upload_image_file(file_stream, filename, content_type)
    print(get_vision_labels(file_stream))



    # Datapoints (x, y, value, radius)
    # where radius, x, y are proportional
    # to the size of the screen

    color_palette, datapoints, datapoints_balanced, color_positions, messages, score, color_template = \
        process_image(file_stream, sigma=500, n_colors=5)


    # Create data for database
    data = jsonify(color_palette=color_palette, datapoints=datapoints,
                   datapoints_balanced=datapoints_balanced,
                   messages=messages, score=score,
                   color_positions=color_positions,
                   color_template=color_template)

    # Post to database
    # database.create(data)

    return data
