from model import storage, database
from flask import Blueprint, current_app, redirect, render_template, request, url_for, jsonify
from model.aiartbase.base import BaseTransformer
from model.aiartbase import image_utils

crud = Blueprint('crud', __name__)


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

    # Color Palette
    image = image_utils.string_to_image(file_stream)
    image_pipeline = BaseTransformer(image)
    image_pipeline.calculate_colors(4)
    color_palette = image_pipeline.get_palette()

    # Image segments
    image_pipeline.segment()
    segments = image_pipeline.get_segments()

    # Datapoints (x, y, value, radius)
    # where radius, x, y are proportional
    # to the size of the screen
    datapoints = [
                (0.1, 0.2, 100, 0.1),
                (0.4, 0.9, 50, 0.2),
                (0.5, 0.2, 80, 0.15),
                (0.5, 0.3, 20, 0.1),
                (0.8, 0.3, 80, 0.1)
                ]
    datapoints_balanced = [
                (0.1, 0.2, 100, 0.1),
                (0.4, 0.9, 50, 0.2),
                (0.5, 0.2, 80, 0.15),
                (0.5, 0.3, 20, 0.1),
                (0.8, 0.3, 80, 0.1),
                (0.7, 0.8, 80, 0.2)
            ]

    # Create data for database
    data = jsonify(color_palette=color_palette, datapoints=datapoints, datapoints_balanced=datapoints_balanced)

    # Post to database
    # database.create(data)

    return data
